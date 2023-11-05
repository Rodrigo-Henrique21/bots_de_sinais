# importações
import numpy as np
import requests as rq
import datetime as dt
import pytz
import time
import os
import dotenv
from telegram import *


# variaveis
status = 0
cont = 0
perdas = 0
acertos = 0
hora_5m = 0

# constante
hora_fechamento = 8
dotenv.load_dotenv(dotenv.find_dotenv())

dicionarioDeConstantes = {
    "TOKEN": os.getenv('TOKEN'),
    "ID_CHAT": os.getenv('ID_CHAT')
}

# instancias
obj_telegram = telegram(dicionarioDeConstantes['TOKEN'],dicionarioDeConstantes['ID_CHAT'])


class double:
    '''
        Comtempla todos os metodos usados para geração dos sinais a serem enviados para salas vip

        Arguments:
            None           
            
        Keyword Arguments:
            None
        Returns:
            {String} - String com a indicação de entrada
        See:
            funcao acionada: 
                None
            chamada pela funcao:
                None

    '''

    def __init__(self,cont,acertos,perdas,status):
        self.cont = cont
        self.acertos = acertos
        self.perdas = perdas
        self.status = status

    def definicao_criterios(self):

        dt_inicio = (dt.datetime.now(pytz.timezone('Europe/London')) - dt.timedelta(seconds=180)).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
        dt_fim = dt.datetime.now(pytz.timezone('Europe/London')).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]

        return dt_inicio,dt_fim


    def requisicao_api(self,dt_inicio,dt_fim):

        url = f'https://blaze-4.com/api/roulette_games/history?startDate={dt_inicio}Z&endDate={dt_fim}Z&page=1'

        chamada = rq.get(url)
        retorno = chamada.json()

        dados_json = retorno['records']

        lista_historico = list(map(lambda x:x['color'],dados_json))
        data_criacao = list(map(lambda x:x['created_at'],dados_json))


        return lista_historico,data_criacao

    def verifica_tempo(self,data_criacao):

        hora_5m = (dt.datetime.strptime(data_criacao[0][:-1],"%Y-%m-%dT%H:%M:%S.%f") + dt.timedelta(seconds=300)).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-7]
        self.status = 1

        return hora_5m,status

    def ultima_operacao(self,data_criacao):
        operacao_atual = (dt.datetime.strptime(data_criacao[0][:-1],"%Y-%m-%dT%H:%M:%S.%f")).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-7]

        return operacao_atual


    def estrategia_inverso(self,lista_historico,dt_inicio,dt_fim):

        self.status = 0
        sinal_enviado = []
        sequencia_preto = False
        sequencia_vermelho = False
        
        if lista_historico[0] == 'red':
            if lista_historico[1] == 'red' and lista_historico[1 + 1] == 'red' and\
                lista_historico[1 + 2] == 'red' and lista_historico[1 + 3] == 'red':
                sequencia_vermelho = True
            if sequencia_vermelho:
                obj_telegram.enviar_mensagem('Aguarde, estamos uma sequencia de vermelhos')
            else:
                obj_telegram.enviar_mensagem('🕑 Oportunidade encontrada! 🕑 \n🎰 JOGO: DOUBLE \n💸 ENTRAR: BLACK \n🔴 Ate um gale - Cobrir o branco \n\n🔥 Entrar após: VERMELHO')
                sinal_enviado.append('black')

        elif lista_historico[0] == 'black':
            if lista_historico[1] == 'black' and lista_historico[1 + 1] == 'black' and\
                lista_historico[1 + 2] == 'black' and lista_historico[1 + 3] == 'black':
                sequencia_preto = True
            if sequencia_preto:
                obj_telegram.enviar_mensagem('Aguarde, estamos uma sequencia de pretos')
            else:
                obj_telegram.enviar_mensagem('🕑 Oportunidade encontrada! 🕑 \n🎰 JOGO: DOUBLE \n💸 ENTRAR: RED \n⚫ Ate um gale - Cobrir o branco \n\n🔥 Entrar após: PRETO')
                sinal_enviado.append('red')
        else:
            obj_telegram.enviar_mensagem('Aguarde, analisando')
        
        lista_historico,data_criacao = self.requisicao_api(dt_inicio,dt_fim)

        return status,sinal_enviado,lista_historico


    def estrategia_gale(self,sinal_enviado,lista_historico,dt_inicio,dt_fim):

            time.sleep(30)
            if len(sinal_enviado) > 0:
                if sinal_enviado[0] == lista_historico[0]:
                    self.acertos += 1
                elif sinal_enviado[0] != lista_historico[0]:
                    obj_telegram.enviar_mensagem('🛡 Estrategia gale 1 - repita o sinal nessa rodada')

                    time.sleep(30)
                    lista_historico,data_criacao = self.requisicao_api(dt_inicio,dt_fim)

                    if sinal_enviado[0] == lista_historico[0]:
                        self.acertos += 1
                    else:
                        self.perdas += 1
