from __future__ import annotations

import asyncio
import re
import urllib.parse
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable

import pandas as pd
from playwright.async_api import Browser, Page, async_playwright


LogFn = Callable[[str], None]


@dataclass(frozen=True)
class ScraperOptions:
    headless: bool = True
    include_shopee: bool = False
    delay_seconds: float = 2.0
    timeout_ms: int = 45_000


@dataclass(frozen=True)
class ProductResult:
    product: str
    target_price: float | None
    mercado_livre_price: float | None
    mercado_livre_max_price: float | None
    shopee_price: float | None
    shopee_max_price: float | None
    lowest_price: float | None
    lowest_store: str | None
    highest_price: float | None
    highest_store: str | None
    best_price: float | None
    best_store: str | None
    below_target: str | None
    status: str


def load_products(path: str | Path) -> pd.DataFrame:
    input_path = Path(path)
    if not input_path.exists():
        raise FileNotFoundError(f"Planilha nao encontrada: {input_path}")

    df = pd.read_excel(input_path)
    required = {"Produto", "Preco_Alvo"}
    missing = required.difference(df.columns)
    if missing:
        missing_list = ", ".join(sorted(missing))
        raise ValueError(f"Planilha precisa conter as colunas: {missing_list}")

    df = df.copy()
    df["Produto"] = df["Produto"].astype(str).str.strip()
    df = df[df["Produto"] != ""]
    if df.empty:
        raise ValueError("Planilha nao contem produtos validos.")

    return df


def write_results(input_df: pd.DataFrame, results: Iterable[ProductResult], output_path: str | Path) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    result_rows = []
    for result in results:
        result_rows.append(
            {
                "Produto": result.product,
                "Preco_Alvo": result.target_price,
                "Menor_Preco_ML": result.mercado_livre_price,
                "Maior_Preco_ML": result.mercado_livre_max_price,
                "Menor_Preco_Shopee": result.shopee_price,
                "Maior_Preco_Shopee": result.shopee_max_price,
                "Menor_Preco_Geral": result.lowest_price,
                "Onde_Menor_Preco": result.lowest_store,
                "Maior_Preco_Geral": result.highest_price,
                "Onde_Maior_Preco": result.highest_store,
                "Melhor_Preco": result.best_price,
                "Onde_Comprar": result.best_store,
                "Abaixo_do_Alvo": result.below_target,
                "Status": result.status,
            }
        )

    result_df = pd.DataFrame(result_rows)
    extra_columns = [column for column in input_df.columns if column not in result_df.columns]
    if extra_columns:
        result_df = pd.concat([input_df[extra_columns].reset_index(drop=True), result_df], axis=1)

    result_df.to_excel(output, index=False)
    return output


async def search_mercado_livre(page: Page, product_name: str, timeout_ms: int) -> list[float]:
    query = urllib.parse.quote(product_name.replace(" ", "-"))
    url = f"https://lista.mercadolivre.com.br/{query}"
    await page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
    await page.wait_for_timeout(2_000)

    cards = await page.query_selector_all(".ui-search-result__wrapper")
    prices: list[float] = []
    for card in cards[:12]:
        price = parse_mercado_livre_card_price(await card.inner_text())
        if price is not None:
            prices.append(price)

    if prices:
        return prices

    fallback = parse_brl_price(await page.inner_text("body"))
    return [fallback] if fallback is not None else []


async def search_shopee(page: Page, product_name: str, timeout_ms: int) -> list[float]:
    query = urllib.parse.quote(product_name)
    url = f"https://shopee.com.br/search?keyword={query}"
    await page.goto(url, wait_until="networkidle", timeout=timeout_ms)
    await page.wait_for_timeout(8_000)
    return extract_brl_prices(await page.inner_text("body"))[:12]


def parse_brl_price(text: str) -> float | None:
    if not text:
        return None

    patterns = [
        r"R\$\s*([\d\.]+,\d{2})",
        r"R\$\s*([\d\.]+)",
        r"\b([\d\.]+,\d{2})\b",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if not match:
            continue
        raw = match.group(1).replace(".", "").replace(",", ".")
        try:
            return float(raw)
        except ValueError:
            continue
    return None


def parse_mercado_livre_card_price(text: str) -> float | None:
    prices = extract_brl_prices(text)
    if not prices:
        return None
    if "OFF" in text.upper() and len(prices) >= 2:
        return prices[1]
    return prices[0]


def extract_brl_prices(text: str) -> list[float]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    prices: list[float] = []

    index = 0
    while index < len(lines):
        if lines[index] != "R$":
            index += 1
            continue

        previous = lines[index - 1] if index > 0 else ""
        if previous.lower().endswith("x"):
            index += 1
            continue

        integer_part = _digits_only(lines[index + 1]) if index + 1 < len(lines) else ""
        if not integer_part:
            index += 1
            continue

        cents = "00"
        if index + 3 < len(lines) and lines[index + 2] == ",":
            cents_candidate = _digits_only(lines[index + 3])
            if cents_candidate:
                cents = cents_candidate[:2].ljust(2, "0")
                index += 4
            else:
                index += 2
        else:
            index += 2

        prices.append(float(f"{integer_part}.{cents}"))

    if prices:
        return prices

    parsed = parse_brl_price(text)
    return [parsed] if parsed is not None else []


def _digits_only(value: str) -> str:
    return re.sub(r"\D", "", value)


async def compare_products(
    products_df: pd.DataFrame,
    options: ScraperOptions,
    log: LogFn | None = None,
) -> list[ProductResult]:
    logger = log or (lambda message: None)
    results: list[ProductResult] = []

    async with async_playwright() as playwright:
        browser = await _launch_browser(playwright.chromium, options)
        context = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1366, "height": 768},
        )
        await context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        page = await context.new_page()

        try:
            for index, row in products_df.iterrows():
                product = str(row["Produto"]).strip()
                target_price = _to_float_or_none(row.get("Preco_Alvo"))
                logger(f"Buscando: {product}")

                ml_prices = await _run_search("Mercado Livre", logger, search_mercado_livre, page, product, options.timeout_ms)
                shopee_prices: list[float] = []
                if options.include_shopee:
                    shopee_prices = await _run_search("Shopee", logger, search_shopee, page, product, options.timeout_ms)

                results.append(_build_result(product, target_price, ml_prices, shopee_prices, options.include_shopee))

                if index != products_df.index[-1]:
                    await asyncio.sleep(options.delay_seconds)
        finally:
            await browser.close()

    return results


def compare_products_sync(
    input_path: str | Path,
    output_path: str | Path,
    options: ScraperOptions,
    log: LogFn | None = None,
) -> Path:
    df = load_products(input_path)
    results = asyncio.run(compare_products(df, options, log))
    return write_results(df, results, output_path)


async def _launch_browser(chromium, options: ScraperOptions) -> Browser:
    return await chromium.launch(
        headless=options.headless,
        args=["--disable-blink-features=AutomationControlled"],
    )


async def _run_search(
    store: str,
    logger: LogFn,
    search_fn,
    page: Page,
    product: str,
    timeout_ms: int,
) -> list[float]:
    try:
        prices = await search_fn(page, product, timeout_ms)
    except Exception as exc:
        logger(f"  {store}: erro ({exc})")
        return []

    if not prices:
        logger(f"  {store}: nao encontrado")
    else:
        logger(f"  {store}: menor R$ {min(prices):.2f} | maior R$ {max(prices):.2f} ({len(prices)} precos)")
    return prices


def _build_result(
    product: str,
    target_price: float | None,
    ml_prices: list[float],
    shopee_prices: list[float],
    include_shopee: bool,
) -> ProductResult:
    store_prices = {}
    if ml_prices:
        store_prices["Mercado Livre"] = ml_prices
    if shopee_prices:
        store_prices["Shopee"] = shopee_prices

    all_prices: list[tuple[str, float]] = []
    for store, prices in store_prices.items():
        all_prices.extend((store, price) for price in prices)

    lowest_store, lowest_price = min(all_prices, key=lambda item: item[1]) if all_prices else (None, None)
    highest_store, highest_price = max(all_prices, key=lambda item: item[1]) if all_prices else (None, None)
    best_store = lowest_store
    best_price = lowest_price
    below_target = None
    if best_price is not None and target_price is not None:
        below_target = "Sim" if best_price <= target_price else "Nao"

    status_parts = []
    if not ml_prices:
        status_parts.append("Mercado Livre nao encontrado")
    if include_shopee and not shopee_prices:
        status_parts.append("Shopee nao encontrado")
    if not include_shopee:
        status_parts.append("Shopee nao consultado")
    status = "; ".join(status_parts) if status_parts else "OK"

    return ProductResult(
        product=product,
        target_price=target_price,
        mercado_livre_price=min(ml_prices) if ml_prices else None,
        mercado_livre_max_price=max(ml_prices) if ml_prices else None,
        shopee_price=min(shopee_prices) if shopee_prices else None,
        shopee_max_price=max(shopee_prices) if shopee_prices else None,
        lowest_price=lowest_price,
        lowest_store=lowest_store,
        highest_price=highest_price,
        highest_store=highest_store,
        best_price=best_price,
        best_store=best_store,
        below_target=below_target,
        status=status,
    )


def _to_float_or_none(value) -> float | None:
    if pd.isna(value):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
