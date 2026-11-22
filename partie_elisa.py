import pandas as pd
import numpy as np
import scipy.stats as stats

# ---------- Chargement et nettoyage ----------
base = pd.read_excel("base2-1.xls")
num_cols = base.select_dtypes("number").columns
base[num_cols] = base[num_cols].replace(-99, np.nan)
base["violente"] = (base["prim_meth"] == 0).astype(int)
base = base.sort_values(["id", "year"]).reset_index(drop=True)

# ---------- Une ligne par campagne ----------
camp = (base.groupby("id")
        .agg(camp_name=("camp_name", "first"),
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
camp["violente"] = (camp["violente_moy"] > 0.5).astype(int)
camp["mixte"] = camp["violente_moy"].between(0.01, 0.99)

# ---------- Issue de chaque campagne ----------
derniere = base.groupby("id").tail(1).set_index("id")
camp["annee_finale"] = camp["id"].map(derniere["year"])
camp["progress_final"] = camp["id"].map(derniere["progress"])
camp["status"] = camp["id"].map(derniere["status"])
camp["success"] = camp["id"].map(base.groupby("id")["success"].max())

camp["issue"] = np.select(
    [camp["success"] == 1, camp["status"] == 0],
    ["succes", "echec"],
    default="en_cours")


# ---------- Méthode et succès ----------
# On exclut les campagnes en cours, dont l'issue est inconnue
net = camp[camp["issue"] != "en_cours"].copy()

print("Campagnes au total :", len(camp))
print("Campagnes en cours (exclues) :", (camp["issue"] == "en_cours").sum())
print("Campagnes retenues :", len(net))
print("dont mixtes :", net["mixte"].sum())

tab = net.groupby("violente")["success"].agg(taux="mean", succes="sum", n="count").round(3)
print("\n", tab)

ct = pd.crosstab(net["violente"], net["success"])
print("\n", ct)
odds, p = stats.fisher_exact(ct)
print(f"\nOdds ratio = {odds:.2f}, p = {p:.2e}")

d = net.dropna(subset=["intensite_max"])
print("\n", pd.crosstab(d["violente"], d["intensite_max"]))
print(d.groupby(["violente", "intensite_max"])["success"].agg(taux="mean", n="count").round(3))