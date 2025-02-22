from gtts import gTTS
from google.cloud import bigquery, storage
import os
import time
import datetime
import requests

class EnviaAudio:
    def __init__(self, google_credentials, project_id, location, nome_bucket, caminho_audio, caminho_bucket, whats_numeros, service_account_json):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_credentials
        self.client = bigquery.Client(project=project_id, location=location)
        self.nome_bucket = nome_bucket
        self.caminho_audio = caminho_audio
        self.caminho_bucket = caminho_bucket
        self.whats_numeros = whats_numeros
        self.service_account_json = service_account_json

    # Função que executa a query no BigQuery e transforma o resultado em um DataFrame
    def execute_query(self, query):
        return self.client.query(query).to_dataframe()

    # Função que formata os dados da query extraída do BigQuery
    def format_frota_data(self, query):
        formatted_data = {}
        for index, row in query.iterrows():
            formatted_data = {
            }
        return formatted_data

    # Função que gera o texto que será convertido em áudio
    def generate_audio_text(self, query):
        texto = (

        )
        return texto
    
    # Função que salva o texto em áudio
    def save_audio(self, texto):
        tts = gTTS(texto, lang='pt-br')
        tts.save(self.caminho_audio)

    # Função que faz o upload do arquivo de áudio para o bucket
    def upload_to_bucket(self):
        storage_client = storage.Client()
        bucket = storage_client.bucket(self.nome_bucket)
        blob = bucket.blob(self.caminho_bucket)
        blob.upload_from_filename(self.caminho_audio)
        print(f"File {self.caminho_audio} uploaded to {self.caminho_bucket}.")

    # Função que captura o link do arquivo de áudio no bucket e envia a mensagem para o WhatsApp
    def send_whatsapp_message(self):
        storage_client = storage.Client.from_service_account_json(self.service_account_json)
        bucket = storage_client.bucket(self.nome_bucket)
        mp3_blob = bucket.blob(self.caminho_bucket)
        mp3_url_assinado = mp3_blob.generate_signed_url(
            version="v4",
            expiration=datetime.timedelta(hours=24),
            method="GET"
        )

        # Captura a parte da URL que será enviada para o WhatsApp
        parte_url = mp3_url_assinado.split('.com/')[1]

        url_auth = # URL do token de autenticação

        headers = {
            "Content-Type": "", # Tipo de conteúdo
            "Authorization": "" # Token de autenticação
        }

        data = {
            "grant_type": "", # Tipo de concessão
            "username": "", # Usuário
            "password": "" # Senha
        }

        # Requisição para obter o token de autenticação
        response = requests.post(url_auth, headers=headers, data=data)
        response_json = response.json()
        access_token = response_json.get('access_token')

        url_api = # URL da API

        headers = {
            'Content-Type': '', # Tipo de conteúdo
            'from-app': '', # Nome do aplicativo
            'category': '', # Categoria
            'Authorization': f'{access_token}', # Token de autenticação
            'Cookie': '' # Cookie
        }

        for numero in self.whats_numeros:
            data = {
                "namespace": "", # Namespace
                "mediaId": "", # ID da mídia
                "phone": numero, # Números de telefone
                "name": "", # Nome da mídia
                "link": f"{parte_url}" # Link do arquivo de áudio
            }

            # Requisição para enviar a mensagem para o WhatsApp
            response = requests.post(url_api, headers=headers, json=data)
            print(response.status_code)
            print(response.json())

        print('------------------- Mensagem enviada para o WhatsApp -------------------')

    # Função que limpa o diretório
    def limpar_diretorio(self, diretorio):
        for root, dirs, files in os.walk(diretorio):
            for file in files:
                if file.endswith(".mp3"):
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                    print(f"Arquivo removido: {file_path}")

    def run(self):
        query = '''

        '''
        executa_query = self.execute_query(query)
        formata_dados = self.format_reserva_data(executa_query)
        print('------------------- QUERY EXECUTADA -------------------')

        texto = self.generate_audio_text(formata_dados)
        self.save_audio(texto)
        self.upload_to_bucket()
        self.send_whatsapp_message()
        time.sleep(10)
        print("------------------ Processo concluido com sucesso! ------------------")

if __name__ == "__main__":
    google_credentials = # Caminho do arquivo json de credenciais do Google Cloud
    project_id = # ID do projeto no Google Cloud
    location = # Localização 
    nome_bucket = # Nome do bucket no Google Cloud
    caminho_audio = # Caminho do arquivo de audio
    caminho_bucket = # Caminho do bucket GCP
    whats_numeros = [] # Números de WhatsApp
    service_account_json = # Caminho do arquivo json de credenciais do serviço GCP

    envia_audio = EnviaAudio(google_credentials, project_id, location, nome_bucket, caminho_audio, caminho_bucket, whats_numeros, service_account_json)
    envia_audio.run()
    envia_audio.limpar_diretorio(os.path.dirname(os.path.abspath(__file__)))
    print("-------------- Limpeza concluida --------------")