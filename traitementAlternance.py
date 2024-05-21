from dataclasses import dataclass
from verification import Verification
import pandas as pd
from openpyxl import load_workbook
import csv
import os, shutil


def dupliquer_fichier(fichier_base, nom_etudiant):
    nom_fichier = f"Fiche_de_liaison_{nom_etudiant}.xlsx"
    if not os.path.exists(nom_fichier):
        shutil.copy(fichier_base, nom_fichier)
    return nom_fichier


def read_csv_data(csv_file):
    """Read data from a CSV file into a pandas DataFrame."""
    return pd.read_csv(csv_file)

def update_excel_file(excel_file, data, cell_mapping, sheet_name):
    """
    Update a specific sheet in an Excel file with data from a DataFrame.
    
    Parameters:
    - excel_file: Path to the Excel file.
    - data: DataFrame containing the data to be inserted.
    - cell_mapping: Dictionary mapping column names to Excel cells.
    - sheet_name: Name of the sheet to be updated.
    """
   
     
    error_report = []  
    # Iterate over the DataFrame rows
    for index, row in data.iterrows():
         # Load the Excel file
        nom_fichier = dupliquer_fichier(excel_file, row["Nom complet"])
        workbook = load_workbook(nom_fichier)

        # Get the specified sheet
        if sheet_name not in workbook.sheetnames :
            if sheet_name not in workbook.sheetnames:
                raise ValueError(f"Sheet {sheet_name} does not exist in the workbook.")
        sheet = workbook[sheet_name]
        error = []
        for column, cell in cell_mapping.items():
            if not verif_champ(row[column], column):
                msg_error = f"Invalid data : {column} - {row[column]}"
                error.append(msg_error)
            sheet[cell] = row[column]
        
        error_report.append({
            "Nom" : row["Nom complet"],
            "Email" : row["Nom d'utilisateur"],
            "error" : error })
        
        workbook.save(nom_fichier)
        
    write_error_report_to_csv(error_report)


def write_error_report_to_csv(error_report, filename="error_report.csv"):
    # Les noms des champs pour le fichier CSV
    fieldnames = ["Nom", "Email", "Erreurs"]
    
    # Dictionnaire pour stocker les rapports d'erreur actuels
    existing_reports = {}
    
    # Lire le fichier existant si disponible
    if os.path.exists(filename):
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Ajouter les lignes existantes au dictionnaire
                existing_reports[row["Email"]] = {
                    "Nom": row["Nom"],
                    "Email": row["Email"],
                    "Erreurs": row["Erreurs"].split(', ')  # Convertir la chaîne en liste
                }
    
    # Mettre à jour ou ajouter les rapports d'erreur
    for report in error_report:
        email = report["Email"]
        if email in existing_reports:
            # Mettre à jour les erreurs existantes
            existing_reports[email]["Erreurs"].extend(report["error"])
            # Supprimer les doublons
            existing_reports[email]["Erreurs"] = list(set(existing_reports[email]["Erreurs"]))
        else:
            # Ajouter un nouveau rapport
            existing_reports[email] = {
                "Nom": report["Nom"],
                "Email": email,
                "Erreurs": report["error"]
            }
    
    # Écrire les données mises à jour dans le fichier
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # Écrire l'en-tête
        writer.writeheader()
        
        # Écrire chaque ligne de rapport d'erreur
        for email, report in existing_reports.items():
            writer.writerow({
                "Nom": report["Nom"],
                "Email": report["Email"],
                "Erreurs": ', '.join(report["Erreurs"])  # Convertir la liste d'erreurs en une chaîne
            })


def verif_champ(value, column):
    
    if column.startswith("Q01_Prenom") or column.startswith("Q11_Prenom") or column.startswith("Q17_Prenom"):
        return Verification.verify_prenom(value)
    elif column.startswith("Q02_Nom") or column.startswith("Q12_Nom") or column.startswith("Q18_Nom"):
        return Verification.verify_nom(value)
    elif column == "Q03_TelPortable" or column == "Q21_TelephonePortable":
        return Verification.verify_numero_telephone_france(str(value))
    elif column.startswith("Q04_Email") or column.startswith("Q15_Email") or column.startswith("Q20_Email"):
        return Verification.verify_email_etudiant(value) or Verification.verify_email_personnel(value)
    elif column == "Q07_NumeroSiret":
        return Verification.verify_siren_ou_siret(str(value))
    elif column == "Q08_CodeAPE":
        return True
    elif column == "Q09_CodeIDCC":
        return True
    elif column == "Q10_OPCOEntreprise":
        return True
    elif column == "Q14_Telephone" or column == "Q19_TelephoneFixe":
        return Verification.verify_numero_telephone_france(str(value))
    elif column == "Q16_Fonction":
        return True
    elif column == "Q23_DateDebutContrat":
        return Verification.verify_date_validite(value)
    elif column == "Q24_DateFinContrat":
        return Verification.verify_date_validite(value)
    elif column == "Q25_ServiceAccueillant":
        return True
    elif column == "Q26_IntituleDuPoste":
        return True
    elif column == "Q28_HorairesHebdomadaires":
        return True
    elif column == "Q29_AutresRemarques":
        return True
    else:
        return True

    

def remplir_fichier_excel():
    csv_file = 'Remplissage_Fiche_de_Liaison_Alternant.csv'  # Path to your CSV file
    excel_file = 'Fiche_de_liaison_Alternant.xlsx'  # Path to your Excel template file
    sheet_name = 'CFA - Promesse Recrutement'  # Name of the sheet to update

    # Mapping of DataFrame columns to Excel cells
    cell_mapping = {
        'Q01_Prenom': 'C19',
        "Q02_Nom" :'F19',
        "Q03_TelPortable" : 'C21',
        "Q04_Email" : 'F21',
        "Q05_NomEntreprise" : 'D26',
        "Q06_AdresseEntreprise" : 'C28',
        "Q07_NumeroSiret" : 'C31',
        "Q08_CodeAPE" : 'G31',
        "Q09_CodeIDCC" : 'F33',
        "Q10_OPCOEntreprise" : 'F35',
        "Q11_Prenom" : 'C40',
        "Q12_Nom" : 'F40',
        "Q13_AdressePostale" : 'C42',
        "Q14_Telephone" : 'C45',
        "Q15_Email" : 'F45',
        "Q16_Fonction" : 'C50',
        "Q17_Prenom" : 'C52',
        "Q18_Nom" : 'F52',
        "Q19_TelephoneFixe" : 'C54',
        "Q20_Email" : 'F54',
        "Q21_TelephonePortable" : 'C56',
        "Q22_Adresse" : 'B59',
        "Q23_DateDebutContrat" : 'D69',
        "Q24_DateFinContrat" : 'D71',
        "Q25_ServiceAccueillant" : 'D76',
        "Q26_IntituleDuPoste" : 'B79',
        "Q27_Adresse" : 'B102',
        "Q28_HorairesHebdomadaires" : 'B104',
        "Q29_AutresRemarques" : 'B115'
    }

    # Read data from the CSV file
    data = read_csv_data(csv_file)

    # Update the specified sheet in the Excel file with the CSV data
    update_excel_file(excel_file, data, cell_mapping, sheet_name)




