from typing import Iterable
from datetime import date, datetime, timedelta, timezone

from agenda.models import Agendamento
import requests
from agenda.libs import brasil_api

def get_horarios_disponiveis(data: date) -> Iterable[datetime]:
    """
    Retorna uma lista de objetos do tipo datetime cujas as datas são os mesmo dias passados (data)
    e os horários são os horários disponiveis para aquele dia, conforme outros agendamentos existam.
    """

    if brasil_api.is_feriado(data):
        return []

    start = datetime(year=data.year, month=data.month, day=data.day, hour=9, minute=0, tzinfo=timezone.utc)
    end = datetime(year=data.year, month=data.month, day=data.day, hour=18, minute=0, tzinfo=timezone.utc)
    delta = timedelta(minutes=30)
    horarios_disponiveis = set()
    while start < end:
        if not Agendamento.objects.filter(data_horario=start).exists():
            horarios_disponiveis.add(start)
        start = start + delta
    
    return horarios_disponiveis