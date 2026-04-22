import pandas as pd

# Create some sample data
data = {
    'Produto': ['Smartphone Samsung Galaxy S23', 'Controle PS5 DualSense', 'Monitor Dell 24'],
    'Preco_Alvo': [3500.00, 350.00, 800.00]
}

df = pd.DataFrame(data)
df.to_excel('produtos.xlsx', index=False)
print("Created produtos.xlsx")
