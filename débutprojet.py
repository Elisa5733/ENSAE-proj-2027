import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

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
    #pays absents de la base population 
    #"South Vietnam": "Vietnam", 
    #"Tibet": "China",
    
}
base1["location"] = base1["location"].replace(corrections)
base1.loc[(base1["location"] == "Yugoslavia") & (base1["year"] > 1992), "location"] = "Serbia and Montenegro"

nouvelles_lignes = pd.DataFrame(
    [{"location": "East Germany", "year": 1953, "Population": 18_390_000},#date de 1950 dans la base
     {"location": "East Germany", "year": 1989, "Population": 16_110_000}]#date de 1990
    + [{"location": "Yemen Arab Republic", "year": a, "Population": 4_880_000} for a in range(1962, 1970)] #date de 1970 (pas de surestimation de la proportion de la population)
)
pop = pd.concat([pop, nouvelles_lignes], ignore_index=True)

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
manquants = (
    merged.loc[merged["_merge"] == "left_only", ["location", "year"]]
    .drop_duplicates()
    .sort_values(["location", "year"])
)
print(manquants.to_string(index=False))
 #regarder les pays qui n'ont pas pu fusionner avec les dates

print(merged[["location", "year", "Population"]].head(20))


merged["total_part_clean"] = merged["total_part"].replace(-99, np.nan) #enlever valeurs manquantes de la participation tot

merged["pourcent_part"] = (merged["total_part_clean"] / merged["Population"]) * 100 #calcul pourcentage de pop dans mouvement

print(merged[["location", "year", "total_part_clean", "Population", "pourcent_part"]].head(10))

print(merged.loc[merged["pourcent_part"] > 20, ["id","location","camp_name", "year","total_part_clean","pourcent_part","Population"]])
#regarder les valeurs aberrantes 

masque_50 = merged["pourcent_part"] > 50 #après vérification des sources, toutes les valeurs sup à 50 % sont issues d'erreurs dans la base 2-1
merged.loc[masque_50, ["total_part_clean", "pourcent_part"]] = np.nan #on remplace ces valeurs par des valeurs manquantes


df = merged.dropna(subset=["pourcent_part", "progress"]).copy() #enlever valeurs manquantes dans progress et pourcent

recodage = {5: 0, 0: 1, 1: 2, 2: 3, 3: 4, 4: 5} #recodage car dans la variable progress, 5 : failure
df["progress2"] = df["progress"].map(recodage)

spearman_corr, p_value = stats.spearmanr( df["pourcent_part"], df["progress2"]) # corrélation de Spearman

print(f"Corr de Spearman : {spearman_corr:.4f}") #ici on regarde année par année les mouvements donc certains sont représentés plusieurs fois
print(f"P-value : {p_value:.4e}")


# une ligne par mouvement : pic de participation + succès (dernière ligne)
mouv = (
    merged.sort_values(["id", "year"])
    .groupby("id")
    .agg(
        location=("location", "first"),
        pic_pourcent=("pourcent_part", "max"),      # pic de participation
        success=("success", "last"),                # dernière ligne = résultat final
    )
    .reset_index()
)

print(mouv.shape)                      

print("Mouvements sans pic calculable :", mouv["pic_pourcent"].isna().sum())

mouv2 = mouv.dropna(subset=["pic_pourcent"]).copy()   
mouv2.to_csv("mouvements.csv", index=False)

mouv2["tranche"] = pd.qcut(mouv2["pic_pourcent"], q=10, duplicates="drop")
print(mouv2.groupby("tranche", observed=True)["success"].agg(n="count", taux="mean"))