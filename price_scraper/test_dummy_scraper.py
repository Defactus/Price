import unittest
import pandas as pd
import os
import dummy_scraper

class TestDummyScraper(unittest.TestCase):
    def setUp(self):
        # Create a test input file
        data = {
            'Produto': ['Test Product 1'],
            'Preco_Alvo': [100.0]
        }
        df = pd.DataFrame(data)
        df.to_excel('produtos.xlsx', index=False)

    def tearDown(self):
        # Clean up files
        if os.path.exists('produtos.xlsx'):
            os.remove('produtos.xlsx')
        if os.path.exists('resultado_comparacao.xlsx'):
            os.remove('resultado_comparacao.xlsx')

    def test_scraper_generates_output(self):
        dummy_scraper.scrape_prices()

        # Check if output file exists
        self.assertTrue(os.path.exists('resultado_comparacao.xlsx'))

        # Check if columns are added and data is present
        result_df = pd.read_excel('resultado_comparacao.xlsx')
        self.assertIn('Preco_ML', result_df.columns)
        self.assertIn('Preco_Shopee', result_df.columns)
        self.assertIn('Melhor_Preco', result_df.columns)

        # Values should be populated
        self.assertIsNotNone(result_df.loc[0, 'Preco_ML'])
        self.assertIsNotNone(result_df.loc[0, 'Preco_Shopee'])
        self.assertIsNotNone(result_df.loc[0, 'Melhor_Preco'])

if __name__ == '__main__':
    unittest.main()
