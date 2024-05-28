import requests
import base64

def obtenir_token(consumer_key, consumer_secret):
    auth_url = "https://api.insee.fr/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic " + base64.b64encode(f"{consumer_key}:{consumer_secret}".encode()).decode(),
    }
    data = {
        "grant_type": "client_credentials"
    }
    
    response = requests.post(auth_url, headers=headers, data=data)
    if response.status_code == 200:
        token = response.json().get("access_token")
        return token
    else:
        print("Échec de la requête pour obtenir le token d'authentification sur l'api SIREN.")
        return None

def verifier_existence_entreprise(id_numero, token, numero_type):
    if numero_type == "siren":
        api_url = f"https://api.insee.fr/entreprises/sirene/V3.11/siren/{id_numero}"
    else:  # siret
        api_url = f"https://api.insee.fr/entreprises/sirene/V3.11/siret/{id_numero}"
    
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return True
    else:
        print("Échec de la requête pour vérifier l'existence de l'entreprise.")
        return False

def verifier_siren_siret_api(siret_siren):
    if len(siret_siren) == 14 and siret_siren.isdigit():
        numero_type = "siret"
    elif len(siret_siren) == 9 and siret_siren.isdigit():
        numero_type = "siren"
    else:
        print("Format de SIRET/SIREN invalide.")
        return False
    
    consumer_key = "AuTlf6ooeIztpaezqgSn4nhNAK0a"
    consumer_secret = "TGXYz_XgcwPCHnW31vKo9TBbe4ka"
    # Obtention du token d'authentification
    token = obtenir_token(consumer_key, consumer_secret)
    if token:
        return verifier_existence_entreprise(siret_siren, token, numero_type)
    else:
        return False

