from __future__ import annotations

import pandas as pd
import pytest

from price_app.core import ProductResult, load_products, parse_brl_price, parse_mercado_livre_card_price, write_results


def test_parse_brl_price() -> None:
    assert parse_brl_price("R$ 1.234,56") == 1234.56
    assert parse_brl_price("R$ 279") == 279.0
    assert parse_brl_price("sem preco") is None


def test_parse_mercado_livre_discount_card_price() -> None:
    text = "\n".join(["Produto", "R$", "279", "R$", "174", ",", "34", "37% OFF", "5x", "R$", "34", ",", "87"])

    assert parse_mercado_livre_card_price(text) == 174.34


def test_load_products_requires_columns(tmp_path) -> None:
    path = tmp_path / "produtos.xlsx"
    pd.DataFrame({"Nome": ["Produto"]}).to_excel(path, index=False)

    with pytest.raises(ValueError, match="Produto"):
        load_products(path)


def test_write_results(tmp_path) -> None:
    output = tmp_path / "resultado.xlsx"
    input_df = pd.DataFrame({"Produto": ["A"], "Preco_Alvo": [10.0]})
    result = ProductResult(
        "A",
        10.0,
        9.0,
        15.0,
        None,
        None,
        9.0,
        "Mercado Livre",
        15.0,
        "Mercado Livre",
        9.0,
        "Mercado Livre",
        "Sim",
        "Shopee nao consultado",
    )

    write_results(input_df, [result], output)

    df = pd.read_excel(output)
    assert df.loc[0, "Melhor_Preco"] == 9.0
    assert df.loc[0, "Onde_Comprar"] == "Mercado Livre"
    assert df.loc[0, "Menor_Preco_Geral"] == 9.0
    assert df.loc[0, "Maior_Preco_Geral"] == 15.0
