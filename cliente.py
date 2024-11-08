import socket as sock


def recebe_dados(sock_cliente, endereco):
    while True:
        sock_conn, ender = sock_cliente.accept()
        print(f"Conexão com sucesso do cliente: {ender}")
        while True:
            try:
                mensagem = sock_conn.recv(1024).decode()
                print(f"Cliente >> {mensagem}")
            except:
                print("Erro ao receber mensagem... fechando")
                sock_conn.close()
                break


HOST = "127.0.0.1"
PORTA = 9999

socket_cliente = sock.socket(sock.AF_INET, sock.SOCK_STREAM)

socket_cliente.connect((HOST, PORTA))
print(5 * "-" + " Chat Iniciado " + 5 * "-")
username = input("Insira o seu nome: ")
socket_cliente.sendall(username.encode())

while True:
    mensagem = input("")
    socket_cliente.sendall(mensagem.encode())
