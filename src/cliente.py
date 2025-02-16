import ssl
import socket
from time import sleep

# Configuração do cliente HTTPS
def https_client(host='127.0.0.1', port=8443):
    context = ssl.create_default_context()
    context.check_hostname = False  # Ignora verificação de hostname
    context.verify_mode = ssl.CERT_NONE  # Ignora verificação do certificado

    with socket.create_connection((host, port)) as sock:
        with context.wrap_socket(sock, server_hostname=host) as secure_socket:
            print(f"Conectado ao servidor HTTPS em {host}:{port}")
            
            for i in range(10):
                file_name = f"html_{i}.html"
                request = f"GET /{file_name} HTTP/1.1\r\nHost: {host}\r\n\r\n"
                secure_socket.sendall(request.encode())

                response = secure_socket.recv(4096)
                print(f"Resposta do servidor ({file_name}):\n{response.decode()}\n")
                sleep(1)
            
            secure_socket.close()
