import csv
from tamarcado.celery import app
from io import StringIO
from django.contrib.auth.models import User

from agenda.serializers import PrestadorSerializer
from django.core.mail import EmailMessage

def gera_relatorio():
    output = StringIO()
    writer = csv.writer(output)

    # Escrevendo cabeçalho
    writer.writerow([
        "prestador",
        "nome_cliente",
        "email_clinte",
        "telefone_cliente",
        "data_horario",
    ])

    # Escrevendo linhas
    prestadores = User.objects.all()
    serializer = PrestadorSerializer(prestadores, many=True)
    for prestador in serializer.data:
        agendamentos = prestador["agendamentos"]
        for agendamento in agendamentos:
            writer.writerow([
                agendamento["prestador"],
                agendamento["nome_cliente"],
                agendamento["email_cliente"],
                agendamento["telefone_cliente"],
                agendamento["data_horario"],
            ])

    return output.getvalue()


@app.task
def envia_email_relatorio():
    output = gera_relatorio()
    email = EmailMessage(
        'tamarcado - Relatório de prestatores',
        'Em anexo o relatório solicitado.',
        'docs@codar.me',
        ['admin@exemple.com'],
    )

    email.attach("relatorio.csv", output, "text/csv")
    email.send()

    return email
