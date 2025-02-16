import socket
import subprocess
import os
import json

HOST = '127.0.0.1'
PORT = 9000
CERT_DIR = "./certs"
CA_KEY_FILE = os.path.join(CERT_DIR, "ca_private.key")  # Chave privada da CA

def gerar_certificado(cert_info):
    """Gera um novo certificado SSL usando os dados recebidos do servidor"""
    key_file = os.path.join(CERT_DIR, "server.key")
    cert_file = os.path.join(CERT_DIR, "server.crt")

    if not os.path.exists(CERT_DIR):
        os.makedirs(CERT_DIR)

    print("[CA] Gerando chave privada...")
    subprocess.run(["openssl", "genpkey", "-algorithm", "RSA",
                    "-out", key_file, "-pkeyopt", "rsa_keygen_bits:2048"], check=True)
    print("[CA] Chave privada gerada com sucesso.")

    print("[CA] Gerando certificado com os dados recebidos...")

    subject = (
        f"/C={cert_info['C']}"
        f"/ST={cert_info['ST']}"
        f"/L={cert_info['L']}"
        f"/O={cert_info['O']}"
        f"/OU={cert_info['OU']}"
        f"/CN={cert_info['CN']}"
        f"/emailAddress={cert_info['email']}"
    )

    subprocess.run([
        "openssl", "req", "-new", "-x509", "-key", key_file, "-out", cert_file,
        "-days", "365", "-subj", subject
    ], check=True)

    print(f"[CA] Certificado gerado com sucesso: {cert_file}")


def iniciar_ca():
    """Inicia a Autoridade Certificadora como um servidor TCP"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"[CA] Autoridade Certificadora rodando em {HOST}:{PORT}")

        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"[CA] Pedido recebido de {addr}")
                data = conn.recv(1024).decode()

                try:
                    cert_info = json.loads(data)  # Decodifica os dados do servidor
                    gerar_certificado(cert_info)
                    conn.sendall(b"CERTIFICADO_GERADO")
                except Exception as e:
                    print(f"[CA] Erro ao processar requisição: {e}")
                    conn.sendall(b"ERRO")
            break
        conn.close()
        server_socket.close()

if __name__ == "__main__":
    iniciar_ca()
