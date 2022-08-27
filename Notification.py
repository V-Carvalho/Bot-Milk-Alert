import os
import dotenv
import requests

dotenv.load_dotenv(dotenv.find_dotenv())

class Notification:

    def send_message(self, message):
        try:
            data = {'chat_id': os.getenv("CHAT_ID"), 'text': message}
            url = f'https://api.telegram.org/bot{os.getenv("TOKEN_BOT")}/sendMessage'
            requests.post(url, data)
        except Exception as erro:
            print("Erro no ao enviar notificacao: ", erro)
