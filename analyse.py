import sqlite3
import pandas as pd

# Connexion à la base de données
conn = sqlite3.connect("ventes.db")

# Requête 1 : Top 5 des clients par chiffre d'affaires
requete1 = """
SELECT c.nom, c.ville,
       SUM(p.prix * co.quantite) AS chiffre_affaires
FROM commandes co
JOIN clients c ON co.id_client = c.id_client
JOIN produits p ON co.id_produit = p.id_produit
GROUP BY c.id_client
ORDER BY chiffre_affaires DESC
LIMIT 5;
"""

df1 = pd.read_sql_query(requete1, conn)
print("=== Top 5 clients ===")
print(df1)

# Requête 2 : Chiffre d'affaires par catégorie
requete2 = """
SELECT p.categorie,
       SUM(p.prix * co.quantite) AS chiffre_affaires
FROM commandes co
JOIN produits p ON co.id_produit = p.id_produit
GROUP BY p.categorie
ORDER BY chiffre_affaires DESC;
"""

df2 = pd.read_sql_query(requete2, conn)
print("\n=== CA par catégorie ===")
print(df2)

conn.close()
