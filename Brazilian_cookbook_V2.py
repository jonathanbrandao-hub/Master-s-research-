import pandas as pd
from collections import Counter
import re
from collections import defaultdict
# load the dataset

df = pd.read_excel("ingredients_braziliancookbook.xlsx")

all_ingredients = []
units_dict = defaultdict(list)

for _, row in df.iterrows():
    
    if pd.isna(row['Ingredients']) or pd.isna(row['units']):
        continue
    
    ingredients = row['Ingredients'].split('\n')
    amounts = row['units'].split('\n')
    
    for ing, amt in zip(ingredients, amounts):
        ing = ing.strip().lower()
        amt = amt.strip()
        
        if ing:
            all_ingredients.append(ing)
            units_dict[ing].append(amt)

# count ingredients
ingredient_counts = Counter(all_ingredients)

# final table
final_table = pd.DataFrame({
    "Ingredient": ingredient_counts.keys(),
    "frequency": ingredient_counts.values(),
    "units_list": [", ".join(units_dict[ing]) for ing in ingredient_counts.keys()]
})
print(final_table)
final_table.to_excel("ingredients_cookbook.xlsx")