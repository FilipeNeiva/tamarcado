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
        User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')

        self.client.login(username='temporary', password='temporary')
        response = self.client.get("/api/agendamentos/?username=temporary")
        data = json.loads(response.content)
        self.assertEqual(data, [])

    def test_listagem_de_agendamentos_criados(self):
        User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')

        self.client.login(username='temporary', password='temporary')
        prestador = Prestador.objects.first()
        Agendamento.objects.create(
            data_horario=datetime(2023, 12, 30, tzinfo=timezone.utc), 
            nome_cliente="Nananda", 
            email_cliente="nananda@codar.me", 
            telefone_cliente="+5586999999999",
            prestador=prestador
        )
        agendamento_serializado = {
            "id": 1,
            "cancelado": False,
            "data_horario": "2023-12-30T00:00:00Z",
            "nome_cliente": "Nananda",
            "email_cliente": "nananda@codar.me",
            "telefone_cliente": "+5586999999999",
            "prestador": "temporary"
        }
        response = self.client.get("/api/agendamentos/?username=temporary")
        data = json.loads(response.content)
        self.assertDictEqual(data[0], agendamento_serializado)


class TestDetalhesAgendamentos(APITestCase):
    def setUp(self):
        User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')

    def test_exibir_agendamento(self):
        self.client.login(username="temporary", password="temporary")
        prestador = Prestador.objects.first()
        Agendamento.objects.create(
            data_horario=datetime(2023, 12, 30, tzinfo=timezone.utc), 
            nome_cliente="Nananda", 
            email_cliente="nananda@codar.me", 
            telefone_cliente="+5586999999999",
            prestador=prestador
        )
        agendamento_serializado = {
            "id": 1,
            "cancelado": False,
            "data_horario": "2023-12-30T00:00:00Z",
            "nome_cliente": "Nananda",
            "email_cliente": "nananda@codar.me",
            "telefone_cliente": "+5586999999999",
            "prestador": "temporary"
        }
        response = self.client.get("/api/agendamentos/1/")
        data = json.loads(response.content)
        self.assertDictEqual(data, agendamento_serializado)


class TestListagemPrestadores(APITestCase):
    def setUp(self):
        User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        User.objects.create_superuser('temporarystaff', 'temporarystaff@gmail.com', 'temporarystaff')

    def test_listagem_de_prestadores_sem_autentificacao(self):
        response = self.client.get("/api/prestadores/")
        data = json.loads(response.content)
        responseExpeted = {
            "detail": "Authentication credentials were not provided."
        }
        self.assertDictEqual(data, responseExpeted)

    def test_listagem_prestadores_autentificacao_sem_staff(self):
        self.client.login(username="temporary", password="temporary")
        response = self.client.get("/api/prestadores/")
        data = json.loads(response.content)
        responseExpeted = {
            "detail": "You do not have permission to perform this action."
        }
        self.assertDictEqual(data, responseExpeted)

    def test_listagem_pretadores(self):
        self.client.login(username="temporarystaff", password="temporarystaff")
        response = self.client.get("/api/prestadores/")
        data = json.loads(response.content)
        responseExpeted = [
            {
                "id": 1,
                "username": "temporary",
                "agendamentos": []
            },
            {
                "id": 2,
                "username": "temporarystaff",
                "agendamentos": []
            }
        ]
        self.assertEqual(data, responseExpeted)


class TestGetHorarios(APITestCase):
    @mock.patch("agenda.libs.brasil_api.is_feriado", return_value=True)
    def test_quando_data_e_feriado_retorna_lista_vazia(self, _):
        response = self.client.get("/api/horarios/?data=2024-12-25")
        data = json.loads(response.content)
        self.assertEqual(data, [])

    @mock.patch("agenda.libs.brasil_api.is_feriado", return_value=False)
    def test_quando_data_e_dia_comum_retorna_lista_com_horarios(self, _):
        response = self.client.get("/api/horarios/?data=2024-10-03")
        data = json.loads(response.content)
        self.assertNotEqual(data, [])
        self.assertEqual(data[0], datetime(2024, 10, 3, 9, tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:00Z"))
        self.assertEqual(data[-1], datetime(2024, 10, 3, 17, 30, tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:00Z"))