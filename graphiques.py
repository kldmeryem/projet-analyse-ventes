import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect("ventes.db")

# Graphique 1 : CA par catégorie (barres)
df_cat = pd.read_sql_query("""
SELECT p.categorie,
       SUM(p.prix * co.quantite) AS chiffre_affaires
FROM commandes co
JOIN produits p ON co.id_produit = p.id_produit
GROUP BY p.categorie
ORDER BY chiffre_affaires DESC;
""", conn)

plt.figure(figsize=(8, 5))
plt.bar(df_cat["categorie"], df_cat["chiffre_affaires"], color="steelblue")
plt.title("Chiffre d'affaires par catégorie")
plt.xlabel("Catégorie")
plt.ylabel("Chiffre d'affaires (MAD)")
plt.tight_layout()
plt.savefig("ca_par_categorie.png")
plt.close()

# Graphique 2 : CA par mois (courbe)
df_mois = pd.read_sql_query("""
SELECT strftime('%Y-%m', co.date_commande) AS mois,
       SUM(p.prix * co.quantite) AS chiffre_affaires
FROM commandes co
JOIN produits p ON co.id_produit = p.id_produit
GROUP BY mois
ORDER BY mois;
""", conn)

plt.figure(figsize=(10, 5))
plt.plot(df_mois["mois"], df_mois["chiffre_affaires"], marker="o", color="darkorange")
plt.title("Évolution mensuelle du chiffre d'affaires")
plt.xlabel("Mois")
plt.ylabel("Chiffre d'affaires (MAD)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("ca_par_mois.png")
plt.close()

conn.close()
print("Graphiques créés avec succès !")