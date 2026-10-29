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
    "Cambodia (Kampuchea)": "Cambodia",
    "Bosnia-Herzegovina": "Bosnia and Herzegovina",
    "Ivory Coast": "Cote d'Ivoire",
    "Swaziland": "Eswatini",
    "Macedonia": "North Macedonia",
    "Hyderabad": "India",
    "Princely State of Travencore": "India",
    #problème pour ceux d'après car pas de vraie correspondance mais j'arrive pas à fusionner sans
    #"South Vietnam": "Vietnam", 
    #"Yemen (North Yemen)": "Yemen",
    #"Yemen Arab Republic": "Yemen",
    #"Yugoslavia": "Serbia", 
    #"Tibet": "China",
    #"East Germany": "Germany",
    
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
manquants = merged.loc[merged["_merge"] == "left_only", "location"].value_counts()
print(manquants) #regarder les pays qui n'ont pas pu fusionner

print(merged[["location", "year", "Population"]].head(20))
