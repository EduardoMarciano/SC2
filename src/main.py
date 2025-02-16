from servidor import iniciar_servidor
from autoridade_certificadora import iniciar_ca
from cliente import https_client

import time
import threading

if __name__ == "__main__":
    # Thread para a Autoridade Certificadora
    ca_thread = threading.Thread(target=iniciar_ca, daemon=True)
    ca_thread.start()

    # Aguarde a inicialização da CA antes de solicitar o certificado
    time.sleep(2)

    # Thread para o Servidor HTTPS
    server_thread = threading.Thread(target=iniciar_servidor, daemon=True)
    server_thread.start()

    # Aguarde o servidor iniciar antes do cliente conectar
    time.sleep(5)

    # Executando o cliente HTTPS
    https_client()
