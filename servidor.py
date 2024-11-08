import socket as sock
import threading

lista_clientes = {}


# Função para recebimento de mensagem do cliente
def recebe_dados(sock_cliente, endereco):
    nome = sock_cliente.recv(50).decode()
    lista_clientes[nome] = sock_cliente
    print(f"Conexão bem sucedida com {nome} via endereço {endereco}")
    broadcast(f"{nome} entrou no servidor", "")
    while True:
        try:
            mensagem = sock_cliente.recv(1024).decode()
            if not mensagem or mensagem == "/sair":
                print(f"{nome} saiu do chat.", "")
                break
            elif mensagem == "/clientes":
                sock_cliente.send(
                    f"Clientes conectados: {', '.join(lista_clientes.keys())}".encode()
                )
            elif mensagem.startswith("/"):
                unicast(mensagem, nome, sock_cliente)
            else:
                print(f"{nome} >> {mensagem}")
                broadcast(mensagem, nome)
        except:
            print(f"Erro, encerrando conexão com o cliente {nome}.")
            break
    broadcast(f"{nome} saiu do chat.", "")
    remover(nome)
    sock_cliente.close()


# Função para mandar mensagem para todos, menos para quem mandou a mensagem
# remetente é o socket de quem mandou a mensagem
def broadcast(mensagem, remetente):
    for nome, cliente in lista_clientes.items():
        if nome != remetente:
            try:
                cliente.sendall(f"{remetente} >> {mensagem}".encode())
            except:
                remover(nome)


# Função para mandar mensagem privada para outro cliente
def unicast(mensagem, nome, sock_cliente):
    try:
        destinatario, texto = mensagem[1:].split(" ", 1)
        # Envia a mensagem apenas para o destinatário
        if destinatario in lista_clientes:
            lista_clientes[destinatario].send(f"Mensagem de {nome}: {texto}".encode())
        else:
            sock_cliente.send("Destinatário não encontrado.".encode())
    except ValueError:
        sock_cliente.send("Formato inválido. Use '/destinatário mensagem'".encode())

#remove nomes da lista_clientes
def remover(nome):
    if nome in lista_clientes:
        lista_clientes[nome].close()
        del lista_clientes[nome]


HOST = "26.32.208.255"
PORTA = 9999

sock_server = sock.socket(sock.AF_INET, sock.SOCK_STREAM)

# Fazemos o bind -> LINK do IP:PORTA
sock_server.bind((HOST, PORTA))
# Abrimos o servidor para o modo de escuta
sock_server.listen()
print(f"O servidor {HOST}:{PORTA} está aguardando conexões...")

# Vamos criar um loop para o servidor acertar várias conexões
while True:
    sock_conn, ender = sock_server.accept()
    # Conexão com sucesso, vamos receber dados
    # Criamos uma thread para a função recebe_dados(sock_conn, ender)
    thread_cliente = threading.Thread(target=recebe_dados, args=[sock_conn, ender])
    thread_cliente.start()
