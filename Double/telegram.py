import telebot

class telegram:
    def __init__(self, api_token, id_chat):
        self.api_token = api_token
        self.id_chat = id_chat
        self.bot = telebot.TeleBot(self.api_token)
        self.mensagens_enviadas = list()

    def enviar_mensagem(self, texto):
        msg_obj = self.bot.send_message(self.id_chat, texto)
        self.mensagens_enviadas.append(msg_obj)
        return msg_obj
