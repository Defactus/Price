from __future__ import annotations

import argparse
from pathlib import Path

from price_app.core import ScraperOptions, compare_products_sync


def main() -> int:
    parser = argparse.ArgumentParser(description="Compara precos a partir de uma planilha Excel.")
    parser.add_argument("input", help="Caminho do produtos.xlsx")
    parser.add_argument("-o", "--output", help="Arquivo de saida .xlsx")
    parser.add_argument("--show-browser", action="store_true", help="Abre o navegador durante a busca")
    parser.add_argument("--include-shopee", action="store_true", help="Tenta consultar Shopee (experimental)")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output) if args.output else input_path.with_name("resultado_comparacao.xlsx")
    options = ScraperOptions(headless=not args.show_browser, include_shopee=args.include_shopee)

    result = compare_products_sync(input_path, output_path, options, print)
    print(f"Resultado salvo em: {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

