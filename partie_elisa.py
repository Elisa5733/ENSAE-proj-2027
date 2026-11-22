import pandas as pd
import numpy as np
import scipy.stats as stats

# ---------- Chargement et nettoyage ----------
base = pd.read_excel("Data/base2-1.xls")
num_cols = base.select_dtypes("number").columns # sélect toutes les colonnes avec données numériques
base[num_cols] = base[num_cols].replace(-99, np.nan)
base["violente"] = (base["prim_meth"] == 0).astype(int) # utile pour calculer la moyenne après
base = base.sort_values(["id", "year"]).reset_index(drop=True) # trier les observations

# ---------- Une ligne par campagne ----------
camp = (base.groupby("id") # regrouper toutes les lignes
        .agg(camp_name=("camp_name", "first"), # récupérer la 1er valeur
             location=("location", "first"),
             debut=("start_year", "first"),
             fin=("end_year", "first"),
             duree=("camp_duration", "first"),
             nb_annees=("year", "count"),
             violente_moy=("violente", "mean"),
             intensite_max=("camp_confl_intensity", "max"),
             intensite_moy=("camp_confl_intensity", "mean"),
             repression_max=("repression", "max"))
        .reset_index())
camp["violente"] = (camp["violente_moy"] > 0.5).astype(int) # créer une variable binaire de violence
camp["mixte"] = camp["violente_moy"].between(0.01, 0.99) # plusieurs méthodes (violentes/non violentes)

# ---------- Issue de chaque campagne ----------
derniere = base.groupby("id").tail(1).set_index("id") # caract les campagnes selon l'état final : succès, échec ou situation en cours
camp["annee_finale"] = camp["id"].map(derniere["year"]) # année de la dernière observation dispo pour chaque campagne
camp["progress_final"] = camp["id"].map(derniere["progress"])
camp["status"] = camp["id"].map(derniere["status"])
camp["success"] = camp["id"].map(base.groupby("id")["success"].max()) # max de la variable success sur toutes les années observées par campagne

camp["issue"] = np.select( # np.select() permet de déf plusieurs conditions et d'attribuer une valeur à chacune
    [camp["success"] == 1, camp["status"] == 0],
    ["succes", "echec"],
    default="en_cours")

# ---------- Méthode et succès ----------
# On exclut les campagnes en cours, dont l'issue est inconnue
net = camp[camp["issue"] != "en_cours"].copy()

print("Campagnes au total :", len(camp))
print("Campagnes en cours (exclues) :", (camp["issue"] == "en_cours").sum()) # 53 campagnes exclues soit 13.8% de nos observations
print("Campagnes retenues :", len(net))
print("dont mixtes :", net["mixte"].sum())

tab = net.groupby("violente")["success"].agg(
    taux="mean", succes="sum", n="count"
    ).round(3) # regrouper les campagnes selon leur caract violent
print("\n", tab)

ct = pd.crosstab(net["violente"], net["success"]) # tableau qui croise : violente (ligne) et success (colonnes)
print("\n", ct)
odds, p = stats.fisher_exact(ct) # test exact de Fisher
print(f"\nOdds ratio = {odds:.2f}, p = {p:.2e}")

d = net.dropna(subset=["intensite_max"]) # retirer les observations pour lesquelles intensite_max manque
print("\n", pd.crosstab(d["violente"], d["intensite_max"])) # croiser violence et intensité max
print(d.groupby(["violente", "intensite_max"])["success"]
    .agg(taux="mean", n="count")
    .round(3)) # taux de succès selon la violence et l'intensité


# ---------- Graphiques ----------

import matplotlib.pyplot as plt

df = camp[camp["issue"] != "en_cours"].copy() # enlever les lignes avec valeur "en_cours" car leur résultat définitif n'est pas encore connu
df["methode"] = df["violente"].map({0: "Non violente", 1: "Violente"}) # nouvelle colonne avec la méthode (violente/non violente)

# Graph 1 : succès selon la méthode
(df.groupby("methode")["success"].mean() * 100).plot(kind="bar", color=["#7AA95C", "#A7001E"])
plt.ylabel("Taux de succès (%)")
plt.title("Taux de succès selon la méthode")
plt.xticks(rotation=0)
plt.savefig("graph1_succes_methode.png", dpi=200, bbox_inches="tight")
plt.show()