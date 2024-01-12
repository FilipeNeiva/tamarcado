from datetime import date
import requests
from django.conf import settings

def is_feriado(data: date) -> bool:
    if settings.TESTING == True:
        if data.month == 12 and data.day == 25:
            return True
        return False

    ano = data.year
    r = requests.get(f"https://brasilapi.com.br/api/feriados/v1/{ano}")
    if r.status_code != 200:
        raise ValueError("Não foi possível consultar os feriados!")
    feriados = r.json()
    for feriado in feriados:
        data_feriado_as_str = feriado["date"]
        data_feriado = date.fromisoformat(data_feriado_as_str)
        if data == data_feriado:
            return True
    return False