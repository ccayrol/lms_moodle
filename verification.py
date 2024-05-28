import datetime
import re
from verifier_siren_siret_api import verifier_siren_siret_api
import dask.dataframe as dd


class Verification:
    @staticmethod
    def verify_numero_etudiant(numero_etudiant):
        """
        Vérifie si le numéro d'étudiant est valide.
        Un numéro d'étudiant valide contient 8 chiffres.
        """
        return len(numero_etudiant) == 8 and numero_etudiant.isdigit()

    @staticmethod
    def verify_code_postal(numero_code_postal):
        """
        Vérifie si le code postal est valide.
        Un code postal valide en France contient 5 chiffres.
        """
        return len(numero_code_postal) == 5 and numero_code_postal.isdigit()

    @staticmethod
    def verify_numero_telephone_france(numero_telephone):
        """
        Vérifie si le numéro de téléphone est valide en France.
        Le numéro de téléphone peut être au format international (+33), national (0) ou autre format reconnu (0033).
        """
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
        """
        Vérifie si l'adresse email de l'étudiant est valide.
        Un email étudiant valide contient un '@', un '.' et le domaine 'etu.u-bordeaux.fr'.
        """
        return (email_etudiant.count("@") == 1
                and email_etudiant.count(".") > 0
                and "etu.u-bordeaux.fr" in email_etudiant)

    @staticmethod
    def verify_email_personnel(email_personnel):
        """
        Vérifie si l'adresse email personnelle est valide.
        Un email personnel valide contient un '@' et un '.'.
        """
        return (email_personnel.count("@") == 1
                and email_personnel.count(".") > 0)

    @staticmethod
    def verify_nom(nom_etudiant):
        """
        Vérifie si le nom est valide.
        Un nom valide ne contient que des lettres et des espaces.
        """
        return re.fullmatch(r'[A-Za-z\s]+', nom_etudiant) is not None

    @staticmethod
    def verify_prenom(prenom_etudiant):
        """
        Vérifie si le prénom est valide.
        Un prénom valide ne contient que des lettres et des espaces.
        """
        return re.fullmatch(r'[A-Za-z\s]+', prenom_etudiant) is not None

    @staticmethod
    def verify_date_validite(date_validite):
        """
        Vérifie si la date de validité est dans le futur.
        La date de validité doit être au format 'YYYY-MM-DD'.
        """
        return datetime.date.today() < datetime.datetime.strptime(date_validite, '%Y-%m-%d').date()

    @staticmethod
    def verify_date_periode_stage(date_debut, date_fin):
        """
        Vérifie si la période de stage est valide.
        La date de début doit être dans le futur et antérieure à la date de fin.
        """
        a = Verification.verify_date_validite(date_debut)
        b = date_debut < date_fin
        return a and b

    @staticmethod
    def verify_format_nombre_heure_hebdomadaire(nombre_heure_hebdomadaire):
        """
        Vérifie si le format du nombre d'heures hebdomadaires est valide.
        Le format valide est 'XX.XX' où X est un chiffre.
        """
        return (len(nombre_heure_hebdomadaire) == 5
                and nombre_heure_hebdomadaire[2] == ".")

    @staticmethod
    def verify_format_montant_gratification(montant_gratification):
        """
        Vérifie si le format du montant de la gratification est valide.
        Les formats valides sont 'XXX.XX' ou 'XXXX.XX' où X est un chiffre.
        """
        return ((len(montant_gratification) == 6
                 and montant_gratification[3] == "."
                 and montant_gratification[:3].isdigit()
                 and montant_gratification[4:].isdigit())
                or
                (len(montant_gratification) == 7
                 and montant_gratification[4] == "."
                 and montant_gratification[:4].isdigit()
                 and montant_gratification[5:].isdigit()))

    @staticmethod
    def verify_siren_ou_siret(Siren_Siret):
        """
        Vérifie si le SIREN ou SIRET est valide en consultant un fichier CSV.
        Le fichier CSV contient les informations des entreprises.
        """
        fichier_csv = 'StockEtablissement_utf8.csv'

        if len(Siren_Siret) == 9:
            column_name = "siren"
        elif len(Siren_Siret) == 14:
            column_name = "siret"
        else:
            return False

        # Charger le fichier CSV en utilisant Dask en spécifiant les types de données
        ddf = dd.read_csv(fichier_csv, dtype={column_name: str}, low_memory=False, usecols=[column_name])

        ligne_siren_recherche = ddf[ddf[column_name] == Siren_Siret]

        # Vérifier si le SIREN ou SIRET existe dans le fichier
        if len(ligne_siren_recherche.index) != 0:
            return True
        else:
            return False
        
    @staticmethod
    def verify_siren_ou_siret_api(Siren_Siret):
        """
        Vérifie si le SIREN ou SIRET est valide en utilisant une API.
        """
        return verifier_siren_siret_api(Siren_Siret)
    
    
    @staticmethod
    def nombre_heure_hebdomadaire(nombre_heure_hebdomadaire) :
        nb_heure_int = float(nombre_heure_hebdomadaire)
        if nb_heure_int > 48 : # max autorisé en France
            return False
        else :
            return True
      
    @staticmethod    
    def nombre_jour_travail_hebdomadaire(nb_jour) :
        nb_jour_int = int(nb_jour)
        if nb_jour_int > 6 :
            return False
        else :
            return True
    