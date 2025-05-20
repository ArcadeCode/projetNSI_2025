#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 19 21:28:17 2025

@author: fettoulmohamed2007
"""

import sqlite3
from datetime import datetime

# --- Création de la base et des tables ---
def create_tables():
    conn = sqlite3.connect('sportify.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS utilisateur (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT,
            email TEXT UNIQUE NOT NULL,
            mot_de_passe TEXT NOT NULL,
            date_creation DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activite (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_utilisateur INTEGER,
            type_activite TEXT CHECK(type_activite IN ('course', 'trail', 'marche')),
            date_activite DATETIME NOT NULL,
            duree INTEGER,
            distance REAL,
            calories INTEGER,
            bpm_moyen INTEGER,
            FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS segment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_activite INTEGER,
            numero_segment INTEGER,
            distance REAL,
            vitesse_moyenne REAL,
            bpm_moyen INTEGER,
            FOREIGN KEY (id_activite) REFERENCES activite(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recommendation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_utilisateur INTEGER,
            texte TEXT NOT NULL,
            type TEXT CHECK(type IN ('entrainement', 'recuperation')),
            date_recommandation DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS badge (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            description TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS utilisateur_badge (
            id_utilisateur INTEGER,
            id_badge INTEGER,
            date_obtention DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id),
            FOREIGN KEY (id_badge) REFERENCES badge(id),
            PRIMARY KEY (id_utilisateur, id_badge)
        )
    ''')

    conn.commit()
    conn.close()
    print("Tables créées avec succès.")

# --- Fonctions pour manipuler les données ---

def ajouter_utilisateur(nom, prenom, email, mot_de_passe):
    """Ajoute un nouvel utilisateur"""
    conn = sqlite3.connect('sportify.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO utilisateur (nom, prenom, email, mot_de_passe)
            VALUES (?, ?, ?, ?)
        ''', (nom, prenom, email, mot_de_passe))
        conn.commit()
        print(f"Utilisateur {nom} ajouté.")
    except sqlite3.IntegrityError:
        print("Erreur : cet email existe déjà.")
    finally:
        conn.close()

def ajouter_activite(id_utilisateur, type_activite, date_activite, duree, distance, calories, bpm_moyen):
    """Ajoute une activité sportive"""
    conn = sqlite3.connect('sportify.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO activite (id_utilisateur, type_activite, date_activite, duree, distance, calories, bpm_moyen)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (id_utilisateur, type_activite, date_activite, duree, distance, calories, bpm_moyen))
    conn.commit()
    conn.close()
    print("Activité ajoutée.")

def get_activites_utilisateur(id_utilisateur):
    """Récupère toutes les activités d’un utilisateur"""
    conn = sqlite3.connect('sportify.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, type_activite, date_activite, duree, distance, calories, bpm_moyen
        FROM activite
        WHERE id_utilisateur = ?
        ORDER BY date_activite DESC
    ''', (id_utilisateur,))
    result = cursor.fetchall()
    conn.close()
    return result

def test():
    """Script de test simple"""
    create_tables()

    # Ajout utilisateur
    ajouter_utilisateur("Dupont", "Jean", "jean.dupont@example.com", "motdepasse123")

    # Récupérer ID utilisateur (ici le premier)
    conn = sqlite3.connect('sportify.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM utilisateur WHERE email = ?", ("jean.dupont@example.com",))
    id_user = cursor.fetchone()[0]
    conn.close()

    # Ajout d’une activité
    ajouter_activite(
        id_utilisateur=id_user,
        type_activite='course',
        date_activite=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        duree=3600,
        distance=10.5,
        calories=600,
        bpm_moyen=140
    )

    # Afficher activités
    activites = get_activites_utilisateur(id_user)
    print("Activités de l’utilisateur :")
    for act in activites:
        print(act)

if __name__ == "__main__":
    test()
