import requests
import json


def sincronizar_colaboradores():
    try:
        url = "https://app.sgg.net.br/api/v3/funcionario/"

        payload = json.dumps({"paginador": {"pagina": 0, "tamanho": 100}})
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "••••••",
            "Cookie": "SGG=ng70cf060tskpebo6u3l8civi6",
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.text)
        pass
    except Exception as e:
        raise Exception("Erro ao sincronizar colaboradores: ", e)
