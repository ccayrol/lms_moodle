import csv
import tkinter as tk
from tkinter import filedialog
import PyPDF2

def controle_coherence(fichier_csv) :
    try : 
        with open(fichier_csv,'r') as file :
            reader = csv.reader(file, delimiter=';')
            for row in reader :
                print(row)
    except FileNotFoundError:
        print("Le fichier spécifié n'a pas été trouvé.")
    except Exception as e:
        print("Une erreur s'est produite :", e)
        
def choisir_fichier():
    # Ouvrir une boîte de dialogue pour choisir le fichier CSV
    chemin_fichier = filedialog.askopenfilename(filetypes=[("Fichiers CSV", "*.csv")])

    # Si un fichier a été sélectionné, lire son contenu
    if chemin_fichier:
        controle_coherence(chemin_fichier)


    

if __name__ == "__main__":
    # Créer une fenêtre principale
    fenetre = tk.Tk()
    fenetre.title("Lire un fichier CSV")

    # Créer un bouton pour choisir le fichier CSV
    bouton_choisir = tk.Button(fenetre, text="Choisir un fichier CSV", command=choisir_fichier)
    bouton_choisir.pack(pady=10)

    # Lancer la boucle principale de l'interface graphique
    fenetre.mainloop()
    
    
    
# BASE D UTILISATION DE LIBRAIRIE PyPDF2 POUR ECRIRE DU TEXTE A DES COORDONNEES BIEN PRECISES.
# OBJECTIF :
#    - Pour chaque champs à remplir, identifier les coordonnees sur le pdf
#    - Créer une liste qui se compose 
#          . En 1er élément le texte à mettre dans le pdf
#          . En 2eme une paire qui correspond aux coordonnées où il faut inserer le texte

# EXEMPLE : liste_texte_coordonnees : 
# liste_de_paires[] 
# liste_de_paires.append(("test_Prenom", (10, 20)))
# liste_de_paires.append(("test_Nom", (30, 40)))


def write_on_existing_pdf(input_pdf, text, x, y, output_pdf):
    
    try : 
        # Ouvre le fichier PDF existant en mode lecture binaire ('rb')
        with open(input_pdf, 'rb') as file:
            # Crée un objet PdfReader pour lire le fichier PDF
            reader = PyPDF2.PdfReader(file)

            # Crée un objet PdfWriter pour écrire dans le fichier PDF
            writer = PyPDF2.PdfWriter()

            # Parcours toutes les pages du fichier PDF
            for page in reader.pages:
                # Crée un objet PageObject pour la page actuelle
                page_obj = writer.add_page(page)

                # Crée un objet TextObject pour le texte à ajouter
                text_obj = page_obj.getContents().getTextObject()

                # Définit la position du texte
                text_obj.setTextOrigin(x, y)

                # Ajoute le texte à la position spécifiée
                text_obj.textLine(text)

            try :
                # Écrit le contenu dans le fichier de sortie
                with open(output_pdf, 'wb') as output_file:
                    writer.write(output_file)
            except FileNotFoundError:
                print("Le fichier spécifié n'a pas été trouvé.")
            except Exception as e:
                print("Une erreur s'est produite :", e)    
    except FileNotFoundError:
        print("Le fichier spécifié n'a pas été trouvé.")
    except Exception as e:
        print("Une erreur s'est produite :", e)
        

# Appel de la fonction avec le nom du fichier PDF existant, le texte à écrire, les coordonnées x et y spécifiques, et le nom du fichier de sortie
write_on_existing_pdf("input.pdf", "Ceci est du texte ajouté à des coordonnées précises.", 100, 750, "output.pdf")
