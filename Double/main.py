# importações

from bot import *

# instancias

if __name__ == "__main__":

    obj_double = double(cont,acertos,perdas,status)


# codigo

while True:

    if (dt.datetime.now()).strftime('%H') == hora_fechamento:
        break
    else:
        obj_double.cont += 1
        dt_inicio,dt_fim = obj_double.definicao_criterios()
        lista_historico,data_criacao = obj_double.requisicao_api(dt_inicio,dt_fim)
        operacao_atual = obj_double.ultima_operacao(data_criacao)

        print(f'rodada:{obj_double.cont}, rodada atual: {operacao_atual}, rodada alvo: {hora_5m}')

        if obj_double.status == 0:
            hora_5m,status = obj_double.verifica_tempo(data_criacao)

        elif obj_double.status == 1 and hora_5m == operacao_atual:
            status,sinal_enviado,lista_historico = obj_double.estrategia_inverso(lista_historico,dt_inicio,dt_fim)
            obj_double.estrategia_gale(sinal_enviado,lista_historico,dt_inicio,dt_fim)
