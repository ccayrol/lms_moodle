# Guide d'installation

1. **Télécharger les résultats des questionnaires sur Moodle**:
   Sur le cours Moodle nommé "MIAGE Inscription professionnelle", téléchargez les résultats des deux fichiers CSV provenant des deux premiers questionnaires :
   - `Remplissage_Fiche_de_Liaison_Stage`
   - `Remplissage_Fiche_de_Liaison_Alternant`
   Placez ces fichiers dans le dossier Fichier_Entrant du projet sans les renommer.

2. **Installer Python et pip en local via PowerShell**:
 a. Téléchargez le programme d'installation de Python 3.12.3 à partir du site officiel de Python : [Python Downloads](https://www.python.org/downloads/). 
 b. Exécutez le programme d'installation et cochez l'option "Add Python to PATH". Cliquez sur "Install Now". 
 c. Vérifiez l'installation en ouvrant PowerShell et en tapant les commandes :
   ```powershell
   python --version
   pip --version

3. **Cloner le projet depuis GitHub**: 
 a. Installez Git depuis Git Downloads : https://git-scm.com/
 b. Ouvrez PowerShell.
 c. Naviguez vers le répertoire de destination : cd C:\Users\VotreNomUtilisateur\Projets
 d. Clonez le projet avec la commande : git clone https://github.com/ccayrol/lms_moodle.git
 e. Vérifiez le clonage : cd lms_moodle

4. **Créer et activer un environnement Python avec VENV**:
   Positionnez-vous dans le dossier src du projet avec cd src à partir du dossier principal
 a. Créez l'environnement virtuel : python -m venv Nom_environnement
 b. Activez l'environnement virtuel : .\Nom_environnement\Scripts\Activate

6. **Installer les librairies Python nécessaires pour le projet**:
 a. Utilisez pip pour installer toutes les dépendances listées dans le fichier requirements.txt :
    --> pip install -r requirements.txt

7. **Exécuter pour constater la complétude des librairies**:
 a. Assurez-vous que l'environnement virtuel est activé : .\Nom_environnement\Scripts\Activate
 b. Exécutez le script controle_coherence_fiche_liaison.py : python controle_coherence_fiche_liaison.py

#Si tout est configuré correctement, le script controle_coherence_fiche_liaison.py devrait s'exécuter sans problème.
