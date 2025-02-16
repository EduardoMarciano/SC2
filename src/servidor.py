import ssl
import socket
import os
import time
import json

HOST_CA = '127.0.0.1'  # Endereço da CA
PORT_CA = 9000  # Porta da CA
CERT_DIR = "./certs"
CERT_FILE = os.path.join(CERT_DIR, "server.crt")
KEY_FILE = os.path.join(CERT_DIR, "server.key")

CERT_INFO = {
    "C": "BR",
    "ST": "Distrito Federal",
    "L": "Brasília",
    "O": "SC2",
    "OU": "departamento de ciências da computação unb",
    "CN": "localhost",
    "email": "e.marciano.meneses@gmail.com"
}

def solicitar_certificado():
    """Solicita à CA a geração do certificado com os dados enviados"""
    print("[Servidor] Solicitando certificado à CA...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST_CA, PORT_CA))
        mensagem = json.dumps(CERT_INFO)
        sock.sendall(mensagem.encode())

        resposta = sock.recv(1024).decode()
        if resposta == "CERTIFICADO_GERADO":
            print("[Servidor] Certificado gerado com sucesso.")

        else:
            print("[Servidor] Erro ao solicitar certificado.")

    sock.close()

def iniciar_servidor():
    """Solicita o certificado e inicia o servidor HTTPS"""
    solicitar_certificado()
    time.sleep(2)
    start_https_server()

# Configuração do servidor HTTPS
def start_https_server(host='127.0.0.1', port=8443):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="./certs/server.crt", keyfile="./certs/server.key")

    # Definir que apenas cifras com AES serão usadas
    context.set_ciphers("AES256-GCM-SHA384")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Servidor HTTPS rodando em {host}:{port}")

        with context.wrap_socket(server_socket, server_side=True) as secure_socket:
            conn, addr = secure_socket.accept()
            print(f"Conexão recebida de {addr}")

            cipher_info = conn.cipher()
            print(f"Protocolo TLS usado: {conn.version()}")
            print(f"Cipher suite utilizada: {cipher_info[0]}")
            print(f"Tamanho da chave: {cipher_info[2]} bits")

            while True:
                request = conn.recv(1024).decode()
                if not request:
                    break
                
                # Captura o nome do arquivo solicitado na requisição
                lines = request.split("\r\n")
                if lines and "GET" in lines[0]:
                    file_name = lines[0].split(" ")[1].strip("/")
                else:
                    file_name = "html_0.html"  # Padrão caso a requisição esteja malformada

                try:
                    with open(f"./../resource/{file_name}", "r", encoding="utf-8") as file:
                        html_content = file.read()
                except FileNotFoundError:
                    html_content = "<html><body><h1>Erro 404: Arquivo não encontrado</h1></body></html>"

                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{html_content}"
                conn.sendall(response.encode())

            conn.close()
            print(f"Conexão encerrada com {addr}")


if __name__ == "__main__":
    iniciar_servidor()