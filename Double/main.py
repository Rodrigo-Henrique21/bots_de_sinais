import numpy as np
import requests as rq
import datetime as dt
import pytz
import time

status = 0
cont = 0
operacao_atual = 0
hora_5m = 0

while True:

    print(f'Rodada {cont} e status {status}')
    print(f'varivel hora operacao atual {operacao_atual} e variavel 5m {hora_5m}')

    dt_inicio = (dt.datetime.now(pytz.timezone('Europe/London')) - dt.timedelta(seconds=180)).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
    dt_fim = dt.datetime.now(pytz.timezone('Europe/London')).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]

    url = f'https://blaze-4.com/api/roulette_games/history?startDate={dt_inicio}Z&endDate={dt_fim}Z&page=1'

    chamada = rq.get(url)
    retorno = chamada.json()

    dados_json = retorno['records']

    lista_historico = list(map(lambda x:x['color'],dados_json))
    data_criacao = list(map(lambda x:x['created_at'],dados_json))
    operacao_atual = (dt.datetime.strptime(data_criacao[0][:-1],"%Y-%m-%dT%H:%M:%S.%f")).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-7]

    if status == 0:

        hora_5m = (dt.datetime.strptime(data_criacao[0][:-1],"%Y-%m-%dT%H:%M:%S.%f") + dt.timedelta(seconds=300)).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-7]
        status = 1
        cont += 1


    elif status == 1 and hora_5m == operacao_atual:
        cont += 1
        if lista_historico[0] == 'red':
            for i in range(1,5):
                if lista_historico[i] == 'red':
                    print('Aguarde tem muitos vermelhos')
                    status = 0
                else:
                    print('Aposte preto')
                    status = 0
        elif lista_historico[0] == 'black':
            for i in range(1,5):
                if lista_historico[i] == 'black':
                    print('Aguarde tem muitos pretos')
                    status = 0
                else:
                    print('Aposte vermelho')
                    status = 0
        else:
            print('Aguarde, analisando')
            status = 0
    else:
        cont += 1
        pass

