#! curl http://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx -o retail.xlsx

import pandas as pd
df = pd.read_excel('http://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx')



df['Description'] = df['Description'].str.strip()
df.dropna(axis = 0, subset=['InvoiceNo'], inplace = True)
df['InvoiceNo'] = df['InvoiceNo'].astype('str')
df = df[~df['InvoiceNo'].str.contains('C')]

df.groupby('Country').count().reset_index().sort_values('InvoiceNo', ascending = False).head()


basket_fr = (df[df['Country']=="France"].groupby(['InvoiceNo', 'Description'])['Quantity'].sum().unstack().reset_index().fillna(0).set_index('InvoiceNo'))


def sum_to_boolean(x):
    if x<=0:
        return 0
    else:
        return 1
basket_fr_final = basket_fr.applymap(sum_to_boolean)
basket_fr_final.head(10)

#! pip install mlxtend

from mlxtend.frequent_patterns import association_rules
from mlxtend.frequent_patterns import apriori

frequent_itemsets_fr = apriori(basket_fr_final, min_support = 0.06, use_colnames = True)
frequent_itemsets_fr.sort_values('support', ascending = False).head()

a_rules = association_rules(frequent_itemsets_fr, metric = "lift", min_threshold = 1)
a_rules.sort_values('lift',ascending = False)

print( basket_fr_final['CHILDRENS CUTLERY SPACEBOY'].sum())
print( basket_fr_final['CHILDRENS CUTLERY DOLLY GIRL'].sum())

basket_fr_final['SET/20 RED RETROSPOT PAPER NAPKINS'].sum()

basket_uk = (df[df['Country']=="United Kingdom"].groupby(['InvoiceNo', 'Description'])['Quantity'].sum().unstack().reset_index().fillna(0).set_index('InvoiceNo'))
basket_final_uk = basket_uk.applymap(sum_to_boolean)
frequent_itemsets_uk = apriori(basket_final_de, min_support = 0.06, use_colnames = True)
a_rules_uk = association_rules(frequent_itemsets_uk, metric = "lift", min_threshold = 1)
a_rules_uk.sort_values('lift',ascending = False).head()