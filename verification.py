import datetime
import dask.dataframe as dd
import re


class Verification:
    @staticmethod
    def verify_numero_etudiant(numero_etudiant):
        return len(numero_etudiant) == 8 and numero_etudiant.isdigit()

    @staticmethod
    def verify_code_postal(numero_code_postal):
        return len(numero_code_postal) == 5 and numero_code_postal.isdigit()

    @staticmethod
    def verify_numero_telephone_france(numero_telephone):
        premier_format = (numero_telephone.startswith("+33")
                          and len(numero_telephone) == 12
                          and numero_telephone[4:].isdigit())
        deuxieme_format = (numero_telephone.startswith("0")
                           and len(numero_telephone) == 10
                           and numero_telephone[1:].isdigit())
        troisieme_format = (numero_telephone.startswith("0033")
                            and len(numero_telephone) == 13
                            and numero_telephone[4:].isdigit())
        return premier_format or deuxieme_format or troisieme_format

    @staticmethod
    def verify_email_etudiant(email_etudiant):
        return (email_etudiant.count("@") == 1
                and email_etudiant.count(".") > 0
                and "etu.u-bordeaux.fr" in email_etudiant)

    @staticmethod
    def verify_email_personnel(email_personnel):
        return (email_personnel.count("@") == 1
                and email_personnel.count(".") > 0)

    @staticmethod
    def verify_nom(nom_etudiant):
        return re.fullmatch(r'[A-Za-z\s]+', nom_etudiant) is not None

    @staticmethod
    def verify_prenom(prenom_etudiant):
        return re.fullmatch(r'[A-Za-z\s]+', prenom_etudiant) is not None

    @staticmethod
    def verify_date_validite(date_validite):
        return datetime.date.today() < datetime.datetime.strptime(date_validite, '%Y-%m-%d').date()

    @staticmethod
    def verify_date_periode_stage(date_debut, date_fin):
        a = Verification.verify_date_validite(date_debut)
        b = date_debut < date_fin
        return a and b

    @staticmethod
    def verify_format_nombre_heure_hebdomadaire(nombre_heure_hebdomadaire):
        return (len(nombre_heure_hebdomadaire) == 5
                and nombre_heure_hebdomadaire[2] == ".")

    @staticmethod
    def verify_format_montant_gratification(montant_gratification):
        return (len(montant_gratification) == 6
                and montant_gratification[3] == "."
                and montant_gratification[:3].isdigit()
                and montant_gratification[4:].isdigit())
    @staticmethod     
    def verify_siren_ou_siret(Siren_Siret):
        # Chemin vers le fichier CSV contenant tous les informations des entreprises
        fichier_csv = 'StockEtablissement_utf8.csv'
        
        if len(Siren_Siret) == 9:
            column_name = "siren"
        elif len(Siren_Siret) == 14:
            column_name = "siret"
        else:
            return False
        
        # Charger le fichier CSV en utilisant Dask en spécifiant les types de données
        ddf = dd.read_csv(fichier_csv, dtype={column_name : str}, low_memory=False, usecols=[column_name])

        ligne_siren_recherche = ddf[ddf[column_name] == Siren_Siret]

        if len(ligne_siren_recherche.index) != 0:
            return True
        else:
            return False

