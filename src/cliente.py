import ssl
import socket

# Configuração do cliente HTTPS
def https_client(host='127.0.0.1', port=8443):
    context = ssl.create_default_context()
    context.check_hostname = False  # Ignora verificação de hostname
    context.verify_mode = ssl.CERT_NONE  # Ignora verificação do certificado

    with socket.create_connection((host, port)) as sock:
        with context.wrap_socket(sock, server_hostname=host) as secure_socket:
            print(f"Conectado ao servidor HTTPS em {host}:{port}")
            
            for _ in range(5):
                response = secure_socket.recv(1024)
                print(f"Resposta do servidor:\n{response.decode()}")
                secure_socket.sendall(b"Recebido com sucesso")