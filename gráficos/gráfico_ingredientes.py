import matplotlib.pyplot as plt
import pandas as pd

# ler planilha
df_50 = pd.read_excel('dados.xlsx', sheet_name='ingredientes top 50')
df_100 = pd.read_excel('dados.xlsx', sheet_name='ingredientes top 100')

# gráfico top 50
plt.figure(figsize=(10,12))
bars_50 = plt.barh(df_50['Ingredient'], df_50['Quantity'])
for bar in bars_50:
    width = bar.get_width()              # agora é o width
    y = bar.get_y() + bar.get_height()/2 # centralizar no eixo y
    plt.text(
        width + 0.5,                     # desloca para direita da barra
        y,
        f'{int(width)}',
        ha='left',
        va='center',
        fontsize=8
    )
    '''height = bar.get_height()
    plt.text(
        bar.get_y() + bar.get_width() / 2,
        height + 0.5,   # desloca para fora da barra
        f'{int(height)}',
        ha='center',
        va='bottom',
        fontsize=8
    )'''
plt.xticks(rotation=45, ha='right')
plt.title(f'Frequency of ingredients top 50 most rated\nTotal unique ingredients: {58}')
plt.tight_layout()
plt.show()

# gráfico top 100
plt.figure(figsize=(13,12))
bars_100 = plt.barh(df_100['Ingredient'], df_100['Quantity'])
plt.xticks(rotation=45, ha='right')
for bar in bars_100:
    width = bar.get_width()              # agora é o width
    y = bar.get_y() + bar.get_height()/2 # centralizar no eixo y
    plt.text(
        width + 0.5,                     # desloca para direita da barra
        y,
        f'{int(width)}',
        ha='left',
        va='center',
        fontsize=8
    )
    '''height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height + 0.5,   # desloca para fora da barra
        f'{int(height)}',
        ha='center',
        va='bottom',
        fontsize=8
    )'''
plt.title(f'Frequency of ingredients top 100 most rated\nTotal unique ingredients: {79}')
plt.tight_layout()
plt.show()