import socket as sock
import threading


def recebe_dados(sock_cliente):
    while True:
        try:
            mensagem = sock_cliente.recv(1024).decode()
            print("\n" + mensagem)
        except:
            print("Erro, encerrando conexão com o servidor")
            sock_cliente.close()
            break


HOST = "26.32.208.255"
PORTA = 9999

socket_cliente = sock.socket(sock.AF_INET, sock.SOCK_STREAM)

socket_cliente.connect((HOST, PORTA))
print(5 * "-" + " Chat Iniciado " + 5 * "-")
while True:
    username = input("Insira o seu nome: ")
    if " " in username:
        print("Nome inválido, não é permitido haver espaços no seu nome")
        continue
    else:
        break
    
socket_cliente.sendall(username.encode())

thread_receber = threading.Thread(target=recebe_dados, args=[socket_cliente])
thread_receber.start()

while True:
    mensagem = input("")
    socket_cliente.sendall(mensagem.encode())
