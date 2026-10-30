import pandas as pd
import numpy as np
import scipy.stats as stats

base1 = pd.read_excel("base2-1.xls")
print(base1.head())

print(base1.shape)

pop = pd.read_csv("population.csv", sep=",")
pop = pop.rename(columns={"Entity": "location", "Year":"year"})

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
    "Yemen (North Yemen)" : "Yemen Arab Republic"
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


merged["total_part_clean"] = merged["total_part"].replace(-99, np.nan) #enlever valeurs manquantes de la participation tot

merged["pourcent_part"] = (merged["total_part_clean"] / merged["Population"]) * 100 #calcul pourcentage de pop dans mouvement

print(merged[["location", "year", "total_part_clean", "Population", "pourcent_part"]].head(10))


df = merged.dropna(subset=["pourcent_part", "progress"]).copy() #enlever valeurs manquantes dans progress et pourcent

recodage = {5: 0, 0: 1, 1: 2, 2: 3, 3: 4, 4: 5} #recodage car dans la variable progress, 5 : failure
df["progress2"] = df["progress"].map(recodage)

spearman_corr, p_value = stats.spearmanr( df["pourcent_part"], df["progress2"]) # corrélation de Spearman

print(f"Corr de Spearman : {spearman_corr:.4f}")
print(f"P-value : {p_value:.4e}")