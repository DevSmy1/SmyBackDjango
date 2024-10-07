import requests
import json
import base64
from decouple import config


url = f"{config('URL_SGG')}/transferencia/"

payload = json.dumps(
    {
        "id_funcionario": "149.241.808-07",
        "id_empresa": "764",
        "id_empresa_destino": "764",
        "id_cargo": "8967",
        "id_setor": "17318",
        "data_transferencia": "2024-12-01",
        "nome": "teste",
        "empresa_rh": "Teste",
    }
)


username = config("URL_SGG_TOKEN")
password = ""

# Concatena username e password com dois pontos
credentials = f"{username}:{password}"

# Codifica as credenciais em Base64
encoded_credentials = base64.b64encode(credentials.encode()).decode()

# Cria o cabeçalho de autorização
auth_header = f"Basic {encoded_credentials}"

print(auth_header)

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": f"Basic {encoded_credentials}",
}


response = requests.post(url, headers=headers, data=payload)

print(response.text)
