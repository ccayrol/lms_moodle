import requests
import base64

# Fonction pour obtenir un token d'authentification de l'API INSEE
def obtenir_token(consumer_key, consumer_secret):
    # URL de l'API pour obtenir le token
    auth_url = "https://api.insee.fr/token"
    # En-têtes de la requête
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic " + base64.b64encode(f"{consumer_key}:{consumer_secret}".encode()).decode(),
    }
    # Données à envoyer avec la requête
    data = {
        "grant_type": "client_credentials"
    }
    
    # Faire la requête POST pour obtenir le token
    response = requests.post(auth_url, headers=headers, data=data)
    if response.status_code == 200:
        # Si la requête réussit, extraire le token de la réponse JSON
        token = response.json().get("access_token")
        return token
    else:
        print("Échec de la requête pour obtenir le token d'authentification sur l'api SIREN.")
        return None

# Fonction pour vérifier l'existence d'une entreprise à partir de son numéro SIREN ou SIRET
def verifier_existence_entreprise(id_numero, token, numero_type):
    # Construire l'URL de l'API en fonction du type de numéro (SIREN ou SIRET)
    if numero_type == "siren":
        api_url = f"https://api.insee.fr/entreprises/sirene/V3.11/siren/{id_numero}"
    else:  # siret
        api_url = f"https://api.insee.fr/entreprises/sirene/V3.11/siret/{id_numero}"
    
    # En-têtes de la requête avec le token d'authentification
    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Faire la requête GET pour vérifier l'existence de l'entreprise
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return True
    else:
        print("Échec de la requête pour vérifier l'existence de l'entreprise.")
        return False

# Fonction principale pour vérifier la validité d'un numéro SIREN ou SIRET
def verifier_siren_siret_api(siret_siren):
    # Vérifier la longueur et le format du numéro pour déterminer s'il s'agit d'un SIREN ou d'un SIRET
    if len(siret_siren) == 14 and siret_siren.isdigit():
        numero_type = "siret"
    elif len(siret_siren) == 9 and siret_siren.isdigit():
        numero_type = "siren"
    else:
        print("Format de SIRET/SIREN invalide.")
        return False
    
    # Clés d'API pour l'authentification
    consumer_key = "AuTlf6ooeIztpaezqgSn4nhNAK0a"
    consumer_secret = "TGXYz_XgcwPCHnW31vKo9TBbe4ka"
    # Obtention du token d'authentification
    token = obtenir_token(consumer_key, consumer_secret)
    if token:
        # Vérifier l'existence de l'entreprise avec le token obtenu
        return verifier_existence_entreprise(siret_siren, token, numero_type)
    else:
        return False
