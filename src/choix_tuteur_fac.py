# Classe Tuteur
class Tuteur:
    def __init__(self, nom, prenom, telephone, fonction, mail):
        """Initialise un objet Tuteur avec un nom, prénom, téléphone, fonction et email."""
        self.nom = nom
        self.prenom = prenom
        self.telephone = telephone
        self.fonction = fonction
        self.mail = mail

    def __str__(self):
        """Renvoie une représentation sous forme de chaîne de caractères de l'objet Tuteur."""
        return f"{self.prenom} {self.nom}, {self.fonction}, Tel: {self.telephone}, Email: {self.mail}"

# Dictionnaire des tuteurs
tuteurs = {
    1: Tuteur("BAILLETTE", "Pamela", None, None, "pamela.baillette@u-bordeaux.fr"),
    2: Tuteur("BENOIS PINEAU", "Jenny", None, None, "jenny.benois-pineau@u-bordeaux.fr"),
    3: Tuteur("BERGER", "Mikael", None, None, "mikaelberger@gmail.com"),
    4: Tuteur("CATAPOULE KICHENASSAMY", "Agastya", None, None, "agastya.catapoule-kichenassamy@u-bordeaux.fr"),
    5: Tuteur("DUFFAUT", "Marie", None, None, "marie.duffaut@orange.fr"),
    6: Tuteur("DUFFAUT", "Philippe", None, None, "philippe-duffaut@orange.fr"),
    7: Tuteur("DUSSAUX", "Valère", None, None, "valere.dussaux@gmail.com"),
    8: Tuteur("FAVRE BERTIN", "Christine", None, None, "christine.favre-bertin@u-bordeaux.fr"),
    9: Tuteur("GUEDES", "Gilles", None, None, "gilgdsuniv@free.fr"),
    10: Tuteur("HAMET", "Joanne", None, None, "joanne.hamet@u-bordeaux.fr"),
    11: Tuteur("LABRUQUERE", "Marie-Laurence", None, None, "mlabruquere@gmail.com"),
    12: Tuteur("LOURME", "Alexandre", None, None, "alexandre.lourme@u-bordeaux.fr"),
    13: Tuteur("MAABOUT", "Sofian", None, None, "maabout@u-bordeaux.fr"),
    14: Tuteur("MAILLET", "Christophe", None, None, "c.maillet@adacis.net"),
    15: Tuteur("MASSÉ", "Renaud", None, None, "renaud.masse@atos.net"),
    16: Tuteur("NICOLAS", "Henri", None, None, "henri.nicolas@u-bordeaux.fr"),
    17: Tuteur("PAILLEY", "Philippe", None, None, "philippe.pailley@gmail.com"),
    18: Tuteur("TREVISOL", "Gilbert", None, None, "gilberttrevisiol@gmail.com")
}

# Fonction pour choisir un Tuteur
def choisir_Tuteur(tuteurs, etudiant):
    """
    Permet de choisir un tuteur parmi une liste pour un étudiant donné.
    Affiche la liste des tuteurs et demande à l'utilisateur de choisir un tuteur par son identifiant.
    
    Arguments:
    tuteurs -- dictionnaire des tuteurs disponibles
    etudiant -- nom de l'étudiant pour lequel le tuteur est choisi
    """
    print(f"Veuillez choisir un tuteur parmi la liste suivante pour l'étudiant {etudiant} :")
    for id_tuteur, tuteur in tuteurs.items():
        print(f"{id_tuteur}: {tuteur}")

    while True:
        try:
            id = int(input("Entrez l'identifiant du tuteur que vous choisissez: ").strip())
            if id in tuteurs:
                tuteur = tuteurs[id]
                print(f"Vous avez choisi : {tuteur}")
                return tuteur
            else:
                print("Identifiant invalide ou non trouvé. Veuillez réessayer.")
        except ValueError:
            print("Veuillez entrer un numéro valide.")
