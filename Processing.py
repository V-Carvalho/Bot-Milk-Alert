from Notification import Notification

notification = Notification()


class Processing:

    def data_processing(self, extracted_data):
        try:
            for item in extracted_data:
                if float(item['Preço Atual']) <= float('5.00'):
                    notification.send_message(
                        f'{item["Marca"]} \n Preço Antigo: {item["Preço Antigo"]} \n Preço Atual: {item["Preço Atual"]} \n Link: {item["Link"]}'
                    )
        except Exception as erro:
            print("Erro ao processar os dados: ", erro)
