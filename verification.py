import datetime


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
        return nom_etudiant.isalpha()

    @staticmethod
    def verify_prenom(prenom_etudiant):
        return prenom_etudiant.isalpha()

    @staticmethod
    def verify_date_validite(date_validite):
        return datetime.date.today() < datetime.datetime.strptime(date_validite, '%Y-%m-%d').date()

    @staticmethod
    def verify_siren_ou_siret(siren_ou_siret):
        a = (len(siren_ou_siret) == 9
             and siren_ou_siret.isdigit())
        b = (len(siren_ou_siret) == 14
             and siren_ou_siret.isdigit())
        return a or b
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

