from servidor import start_https_server
from cliente import https_client

if __name__ == "__main__":
    import threading
    
    # Executando o servidor em uma thread separada
    server_thread = threading.Thread(target=start_https_server, daemon=True)
    server_thread.start()
    
    # Aguarde o servidor iniciar antes do cliente conectar
    import time
    time.sleep(2)
    
    # Executando o cliente HTTPS
    https_client()
