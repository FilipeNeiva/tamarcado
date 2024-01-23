import json
from rest_framework.test import APITestCase

from agenda.models import Agendamento
from django.contrib.auth.models import User as Prestador
from datetime import datetime, timezone
from django.contrib.auth.models import User

from unittest import mock

# Create your tests here.
class TestListagemAgendamentos(APITestCase):
    
    
    def test_listagem_vazia(self):
        return True

    def test_listagem_de_agendamentos_criados(self):
        return True


class TestDetalhesAgendamentos(APITestCase):

    def test_exibir_agendamento(self):
        return True


class TestListagemPrestadores(APITestCase):

    def test_listagem_de_prestadores_sem_autentificacao(self):
        return True

    def test_listagem_prestadores_autentificacao_sem_staff(self):
        return True

    def test_listagem_pretadores(self):
        return True


class TestGetHorarios(APITestCase):
    # @mock.patch("agenda.libs.brasil_api.is_feriado", return_value=True)
    def test_quando_data_e_feriado_retorna_lista_vazia(self):
        return True

    # @mock.patch("agenda.libs.brasil_api.is_feriado", return_value=False)
    def test_quando_data_e_dia_comum_retorna_lista_com_horarios(self):
        return True