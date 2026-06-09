import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd

#read the data

df = pd.read_excel('Tudo Gostoso.xlsx', sheet_name='analysis')

ingredients = df['Ingredient']
carbon = df['CF total (gCO2e)']
weight = df['Total g']
frequency = df['frequency']

x_maximum = 4100
y_maximum = 40000

colors = []
empty_values =[]
for i in range(len(ingredients)):
    if carbon[i] == 0:
        empty_values.append(ingredients[i])
    if carbon[i] > y_maximum or weight[i] > x_maximum:
        plt.text(weight[i], carbon[i], ingredients[i], 
            fontsize=8)
        if carbon[i] > y_maximum:
            color = 'red' 
            colors.append(color)
        if weight[i] > x_maximum:
            color = 'blue'
            colors.append(color)
    else:
        color = 'gray'
        colors.append(color)

plt.scatter(weight, carbon, c=colors, s=frequency*10, alpha=0.5)


# Labels 
plt.xlabel('Weight (g)')
plt.ylabel('Carbon footprint (gCO2e)')

legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='Carbon footprint above 40Kg',
           markerfacecolor='red', markersize=8),
    Line2D([0], [0], marker='o', color='w', label='Total weight above 4.1 Kg',
           markerfacecolor='blue', markersize=8),       
    Line2D([0], [0], marker='o', color='w', label='Other ingredients',
           markerfacecolor='gray', markersize=8)
]

plt.legend(handles=legend_elements)
plt.title('Carbon footprint of ingridients vs weight')
plt.show()
print(f'The number of ingredients without CF value is {len(empty_values)}, and the list is:{empty_values}')


