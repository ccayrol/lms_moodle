from dataclasses import dataclass

import pandas


@dataclass(frozen=True)
class Questionnaire:
    Reponse = "Réponse"
    Soumis = "Soumis le :"
    Institution = "Institution"
    Departement = "Département"
    Cours = "Cours"
    Groupe = "Groupe"
    Id = "ID"
    Nom = "Nom complet"
    NomUtilisateur = "Nom d'utilisateur"
    Q01Prenom =  "Q01_Prenom"
    Q02Nom = "Q02_Nom"
    Q03TelPortable = "Q03_TelPortable"
    Q04Email = "Q04_Email"
    Q05NomEntreprise = "Q05_NomEntreprise"
    Q06AdresseEntreprise = "Q06_AdresseEntreprise"
    Q07NumeroSiret = "Q07_NumeroSiret"
    Q08CodeAPE = "Q08_CodeAPE"
    Q09CodeIDCC = "Q09_CodeIDCC"
    Q10OPCOEntreprise = "Q10_OPCOEntreprise"
    Q11PrenomTuteur = "Q11_Prenom"
    Q12NomTuteur = "Q12_Nom"
    Q13AdressePostale = "Q13_AdressePostale"
    Q14Telephone = "Q14_Telephone"
    Q15Email = "Q15_Email"
    Q16Fonction = "Q16_Fonction"
    Q17Prenom = "Q17_Prenom"
    Q18Nom = "Q18_Nom"
    Q19TelephoneFixe = "Q19_TelephoneFixe"
    Q20Email = "Q20_Email"
    Q21TelephonePortable = "Q21_TelephonePortable"
    Q22Adresse = "Q22_Adresse"
    Q23DateDebutContrat = "Q23_DateDebutContrat"
    Q24DateFinContrat = "Q24_DateFinContrat"
    Q25ServiceAccueillant = "Q25_ServiceAccueillant"
    Q26IntituleDuPoste = "Q26_IntituleDuPoste"
    Q27Adresse = "Q27_Adresse"
    Q28HorairesHebdomadaires = "Q28_HorairesHebdomadaires"
    Q29AutresRemarques = "Q29_AutresRemarques"
    # fait moi un getter pour chaque attribut

    class Questionnaire:
        Reponse = "Réponse"
        Soumis = "Soumis le :"
        Institution = "Institution"
        Departement = "Département"
        Cours = "Cours"
        Groupe = "Groupe"
        Id = "ID"
        Nom = "Nom complet"
        NomUtilisateur = "Nom d'utilisateur"
        Q01Prenom = "Q01_Prenom"
        Q02Nom = "Q02_Nom"
        Q03TelPortable = "Q03_TelPortable"
        Q04Email = "Q04_Email"
        Q05NomEntreprise = "Q05_NomEntreprise"
        Q06AdresseEntreprise = "Q06_AdresseEntreprise"
        Q07NumeroSiret = "Q07_NumeroSiret"
        Q08CodeAPE = "Q08_CodeAPE"
        Q09CodeIDCC = "Q09_CodeIDCC"
        Q10OPCOEntreprise = "Q10_OPCOEntreprise"
        Q11PrenomTuteur = "Q11_Prenom"
        Q12NomTuteur = "Q12_Nom"
        Q13AdressePostale = "Q13_AdressePostale"
        Q14Telephone = "Q14_Telephone"
        Q15Email = "Q15_Email"
        Q16Fonction = "Q16_Fonction"
        Q17Prenom = "Q17_Prenom"
        Q18Nom = "Q18_Nom"
        Q19TelephoneFixe = "Q19_TelephoneFixe"
        Q20Email = "Q20_Email"
        Q21TelephonePortable = "Q21_TelephonePortable"
        Q22Adresse = "Q22_Adresse"
        Q23DateDebutContrat = "Q23_DateDebutContrat"
        Q24DateFinContrat = "Q24_DateFinContrat"
        Q25ServiceAccueillant = "Q25_ServiceAccueillant"
        Q26IntituleDuPoste = "Q26_IntituleDuPoste"
        Q27Adresse = "Q27_Adresse"
        Q28HorairesHebdomadaires = "Q28_HorairesHebdomadaires"
        Q29AutresRemarques = "Q29_AutresRemarques"

        def getReponse(self):
            return self.Reponse

        def getSoumis(self):
            return self.Soumis

        def getInstitution(self):
            return self.Institution

        def getDepartement(self):
            return self.Departement

        def getCours(self):
            return self.Cours

        def getGroupe(self):
            return self.Groupe

        def getId(self):
            return self.Id

        def getNom(self):
            return self.Nom

        def getNomUtilisateur(self):
            return self.NomUtilisateur

        def getQ01Prenom(self):
            return self.Q01Prenom

        def getQ02Nom(self):
            return self.Q02Nom

        def getQ03TelPortable(self):
            return self.Q03TelPortable

        def getQ04Email(self):
            return self.Q04Email

        def getQ05NomEntreprise(self):
            return self.Q05NomEntreprise

        def getQ06AdresseEntreprise(self):
            return self.Q06AdresseEntreprise

        def getQ07NumeroSiret(self):
            return self.Q07NumeroSiret

        def getQ08CodeAPE(self):
            return self.Q08CodeAPE

        def getQ09CodeIDCC(self):
            return self.Q09CodeIDCC

        def getQ10OPCOEntreprise(self):
            return self.Q10OPCOEntreprise

        def getQ11PrenomTuteur(self):
            return self.Q11PrenomTuteur

        def getQ12NomTuteur(self):
            return self.Q12NomTuteur

        def getQ13AdressePostale(self):
            return self.Q13AdressePostale

        def getQ14Telephone(self):
            return self.Q14Telephone

        def getQ15Email(self):
            return self.Q15Email

        def getQ16Fonction(self):
            return self.Q16Fonction

        def getQ17Prenom(self):
            return self.Q17Prenom

        def getQ18Nom(self):
            return self.Q18Nom

        def getQ19TelephoneFixe(self):
            return self.Q19TelephoneFixe

        def getQ20Email(self):
            return self.Q20Email

        def getQ21TelephonePortable(self):
            return self.Q21TelephonePortable

        def getQ22Adresse(self):
            return self.Q22Adresse

        def getQ23DateDebutContrat(self):
            return self.Q23DateDebutContrat

        def getQ24DateFinContrat(self):
            return self.Q24DateFinContrat

        def getQ25ServiceAccueillant(self):
            return self.Q25ServiceAccueillant

        def getQ26IntituleDuPoste(self):
            return self.Q26IntituleDuPoste

        def getQ27Adresse(self):
            return self.Q27Adresse

        def getQ28HorairesHebdomadaires(self):
            return self.Q28HorairesHebdomadaires

        def getQ29AutresRemarques(self):
            return self.Q29AutresRemarques

def lireFichierCSV(fichier):
    data = pandas.read_csv(fichier)

    print(data)
    print("len : ",  len(data))
    if 0 in data.index:
        print(data.loc[0, Questionnaire.Q01Prenom])
    else:
        print("Row with index 1 does not exist")
    return data



