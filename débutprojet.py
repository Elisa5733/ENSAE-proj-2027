import pandas as pd

base1 = pd.read_excel("base2-1.xls")
print(base1.head())

print(base1.shape)

pop = pd.read_csv("population.csv", sep=",")
print(pop.head())
print(pop.shape)

