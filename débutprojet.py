import pandas as pd

base1 = pd.read_excel("base2-1.xls")
print(base1.head())

print(base1.shape)

pop = pd.read_csv("population.csv", sep=",")


pop = pop.rename(columns={"Entity": "location", "Year":"year"})

print(pop.head())
print(pop.shape)

corrections = {
    "Myanmar/Burma": "Myanmar",
    "Palestinian Territories": "Palestine",
    "UK": "United Kingdom",
    "South Vietnam": "Vietnam", 
    "Cambodia (Kampuchea)": "Cambodia",
    "Yemen (North Yemen)" : "Yemen",
    "Yemen Arab Republic" : "Yemen",
    "Bosnia-Herzegovina" : "Bosnia and Herzegovina",
    "Yugoslavia": "Yugoslavia", 
    "Tibet": "China",
    "Ivory Coast": "Cote d'Ivoire",
    "East Germany" : "East Germany",
    "Hyderabad" : "India",
    "Swaziland": "Eswatini",
    "Princely State of Travencore" :"India", 
    "Macedonia": "North Macedonia",
}
base1["location"] = base1["location"].replace(corrections)

base1["location"] = base1["location"].str.strip() #retirer les éventuels espaces avant ou après

merged = base1.merge(
    pop[["location", "year", "Population"]],
    on=["location", "year"],
    how="left",                 
    validate="many_to_one",
    indicator=True
)

print(len(base1), len(merged)) #vérification du nombre de lignes            
print(merged["_merge"].value_counts())


print(merged[["location", "year", "Population"]].head(20))
manquants = merged.loc[merged["_merge"] == "left_only", "location"].value_counts()
print(manquants)