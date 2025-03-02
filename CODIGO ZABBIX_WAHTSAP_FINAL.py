# -*- coding: utf-8 -*-
"""Untitled3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/16d9I8rqxkGJUa9ky8QoepjvwzUQ-9q4a
"""

from zabbix_api import ZabbixAPI
import requests
import json
from twilio.rest import Client

# Credenciais do Zabbix
zabbix_url = 'https://zabbix.grupojet.com.br/api_jsonrpc.php'
zabbix_user = 'Ruan'
zabbix_password = 'dUcfak-pymfo9-pencoz'

# Credenciais do Twilio (WhatsApp)
account_sid = "AC2bc7ffb4a3b41f20f722682262f0ef8d"
auth_token = "9d15197cc516be2c1f169a4b1ccc7dcb"
twilio_number = '+13046991208'
seu_numero_whatsapp = '+5562993227433'

# Função para enviar mensagem do WhatsApp
def enviar_mensagem_whatsapp(mensagem):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=mensagem,
        from_=twilio_number,
        to=seu_numero_whatsapp
    )
    print(f"Mensagem enviada: {message.sid}")
# Função para fazer login na API e obter o token de autenticação
def obter_gatilhos_com_problemas(token):
    headers = {'Content-Type': 'application/json-rpc'}
    payload = {
        "jsonrpc": "2.0",
        "method": "trigger.get",
        "params": {
            'filter': {'value': 1},
            'output': ['triggerid', 'description', 'lastchange'],
            'expandDescription': True,
            'sortfield': 'lastchange',
            'sortorder': 'DESC'
        },
        "auth": token,
        "id": 2
    }
    response = requests.post(zabbix_url, data=json.dumps(payload), headers=headers)

    if response.status_code == 200:
        try:
            json_response = response.json()
            if 'result' in json_response:
                return json_response['result']
            else:
                print(f"Erro ao obter gatilhos: {json_response}")
                return None
        except json.JSONDecodeError:
            print(f"Erro ao decodificar resposta JSON: {response.text}")
            return None
    else:
        print(f"Erro na requisição: {response.status_code}")
        return None

# Obter token de autenticação
token = zabbix_login(zabbix_url, zabbix_user, zabbix_password)

if token:
    # Obter gatilhos com problemas
    gatilhos_com_problemas = obter_gatilhos_com_problemas(token)

    # Imprimir detalhes dos gatilhos
    if gatilhos_com_problemas:
        print("Gatilhos com problemas:")
        for trigger in gatilhos_com_problemas:
            print(f"  ID: {trigger['triggerid']}")
            print(f"  Descrição: {trigger['description']}")
            print(f"  Última mudança: {trigger['lastchange']}")
            print("-" * 30)