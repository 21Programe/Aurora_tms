import requests

API_URL = "http://127.0.0.1:8000"


def api_get(path: str, timeout: int = 5):
    try:
        res = requests.get(f"{API_URL}{path}", timeout=timeout)
        if res.status_code == 200:
            return res.json(), None
        try:
            body = res.json()
            return None, body.get("detail", "Erro de API")
        except Exception:
            return None, f"Erro HTTP {res.status_code}"
    except requests.RequestException as e:
        return None, str(e)


def api_post(path: str, payload: dict, timeout: int = 10):
    try:
        res = requests.post(f"{API_URL}{path}", json=payload, timeout=timeout)
        if res.status_code in (200, 201):
            return res.json(), None
        try:
            body = res.json()
            return None, body.get("detail", "Erro de API")
        except Exception:
            return None, f"Erro HTTP {res.status_code}"
    except requests.RequestException as e:
        return None, str(e)