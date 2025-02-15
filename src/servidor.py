import ssl
import socket

# Configuração do servidor HTTPS
def start_https_server(host='127.0.0.1', port=8443):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")

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

            try:
                with open("./../resource/html.html", "r", encoding="utf-8") as file:
                    html_content = file.read()
            except FileNotFoundError:
                html_content = "<html><body><h1>Erro 404: Arquivo não encontrado</h1></body></html>"
            
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{html_content}"
            for _ in range(5):
                conn.sendall(response.encode())
                ack = conn.recv(1024).decode()
                print(f"Confirmação recebida do cliente: {ack}")
            conn.close()