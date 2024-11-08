import socket as sock
import threading


# Função para recebimento de mensagem do cliente
def recebe_dados(sock_cliente, endereco):
    nome = sock_cliente.recv(50).decode()
    print(f"Conexão bem sucedida com {nome} via endereço {endereco}")
    while True:
        try:
            mensagem = sock_cliente.recv(1024).decode()
            if not mensagem:
                print(f"{nome} saiu do chat.")
                break
            print(f"{nome} >> {mensagem}")
        except:
            print("Erro ao receber mensagem... fechando")
            break
        sock_cliente.close()


def broadcast(lista_clientes):
    pass


def unicast(cliente):
    pass


def remover(cliente):
    pass


HOST = "127.0.0.1"
PORTA = 9999

lista_clientes = []
sock_server = sock.socket(sock.AF_INET, sock.SOCK_STREAM)

# Fazemos o bind -> LINK do IP:PORTA
sock_server.bind((HOST, PORTA))
# Abrimos o servidor para o modo de escuta
sock_server.listen()
print(f"O servidor {HOST}:{PORTA} está aguardando conexões...")

# Vamos criar um loop para o servidor acertar várias conexões
while True:
    sock_conn, ender = sock_server.accept()
    print(f"Conexão com sucesso do cliente: {ender}")
    # Conexão com sucesso, vamos receber dados
    # Criamos uma thread para a função recebe_dados(sock_conn, ender)
    thread_cliente = threading.Thread(target=recebe_dados, args=[sock_conn, ender])
    thread_cliente.start()
