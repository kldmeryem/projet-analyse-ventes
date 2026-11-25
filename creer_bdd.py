import sqlite3
import random
from datetime import date, timedelta

# 1. Connexion (le fichier ventes.db sera créé automatiquement)
conn = sqlite3.connect("ventes.db")
cur = conn.cursor()

# 2. Création des tables
cur.executescript("""
DROP TABLE IF EXISTS commandes;
DROP TABLE IF EXISTS produits;
DROP TABLE IF EXISTS clients;

CREATE TABLE clients (
    id_client INTEGER PRIMARY KEY,
    nom TEXT,
    ville TEXT
);

CREATE TABLE produits (
    id_produit INTEGER PRIMARY KEY,
    nom TEXT,
    categorie TEXT,
    prix REAL
);

CREATE TABLE commandes (
    id_commande INTEGER PRIMARY KEY,
    id_client INTEGER,
    id_produit INTEGER,
    quantite INTEGER,
    date_commande TEXT,
    FOREIGN KEY (id_client) REFERENCES clients(id_client),
    FOREIGN KEY (id_produit) REFERENCES produits(id_produit)
);
""")

# 3. Données de départ
villes = ["Casablanca", "Rabat", "Marrakech", "Fès", "Tanger", "Agadir"]
noms = ["Sara", "Youssef", "Imane", "Omar", "Salma", "Hamza", "Nada",
        "Anas", "Meryem", "Yassine", "Hajar", "Reda", "Kenza", "Ayoub",
        "Lina", "Mehdi", "Aya", "Zakaria", "Ghita", "Walid"]

produits = [
    ("Laptop", "Informatique", 6500),
    ("Souris", "Informatique", 120),
    ("Clavier", "Informatique", 250),
    ("Casque", "Audio", 450),
    ("Enceinte", "Audio", 600),
    ("Smartphone", "Téléphonie", 3500),
    ("Chargeur", "Téléphonie", 90),
    ("Montre connectée", "Accessoires", 800),
]

# 4. Insertion
for i, nom in enumerate(noms, start=1):
    cur.execute("INSERT INTO clients VALUES (?, ?, ?)",
                (i, nom, random.choice(villes)))

for i, (nom, cat, prix) in enumerate(produits, start=1):
    cur.execute("INSERT INTO produits VALUES (?, ?, ?, ?)",
                (i, nom, cat, prix))

debut = date(2025, 1, 1)
for i in range(1, 301):
    d = debut + timedelta(days=random.randint(0, 364))
    cur.execute("INSERT INTO commandes VALUES (?, ?, ?, ?, ?)",
                (i,
                 random.randint(1, len(noms)),
                 random.randint(1, len(produits)),
                 random.randint(1, 5),
                 d.isoformat()))

conn.commit()
conn.close()
print("Base de données créée avec succès !")