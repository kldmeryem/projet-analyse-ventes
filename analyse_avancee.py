import sqlite3
import pandas as pd

conn = sqlite3.connect("ventes.db")

# Requête 1 : Classement des clients par CA avec RANK()
requete1 = """
SELECT c.nom,
       c.ville,
       SUM(p.prix * co.quantite) AS chiffre_affaires,
       RANK() OVER (ORDER BY SUM(p.prix * co.quantite) DESC) AS rang
FROM commandes co
JOIN clients c ON co.id_client = c.id_client
JOIN produits p ON co.id_produit = p.id_produit
GROUP BY c.id_client
ORDER BY rang
LIMIT 10;
"""
print("=== Classement des clients (RANK) ===")
print(pd.read_sql_query(requete1, conn))

# Requête 2 : CA mensuel + CA cumulé (SUM OVER)
requete2 = """
WITH ca_mensuel AS (
    SELECT strftime('%Y-%m', co.date_commande) AS mois,
           SUM(p.prix * co.quantite) AS ca
    FROM commandes co
    JOIN produits p ON co.id_produit = p.id_produit
    GROUP BY mois
)
SELECT mois,
       ca,
       SUM(ca) OVER (ORDER BY mois) AS ca_cumule
FROM ca_mensuel
ORDER BY mois;
"""
print("\n=== CA mensuel et cumulé ===")
print(pd.read_sql_query(requete2, conn))

# Requête 3 : Meilleur produit de chaque catégorie (PARTITION BY)
requete3 = """
WITH ventes_produit AS (
    SELECT p.categorie,
           p.nom AS produit,
           SUM(p.prix * co.quantite) AS ca
    FROM commandes co
    JOIN produits p ON co.id_produit = p.id_produit
    GROUP BY p.id_produit
)
SELECT categorie, produit, ca
FROM (
    SELECT *,
           RANK() OVER (PARTITION BY categorie ORDER BY ca DESC) AS rang
    FROM ventes_produit
)
WHERE rang = 1;
"""
print("\n=== Meilleur produit par catégorie ===")
print(pd.read_sql_query(requete3, conn))

conn.close()