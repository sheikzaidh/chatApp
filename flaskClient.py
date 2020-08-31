from flask import Flask,request,jsonify
import socket
import select
import errno

app = Flask(__name__)
my_username = 'SheikZaidh'

@app.route('/',methods=['POST'])
def newFunc():
    data = request.get_json()
    global my_username
    my_username = data['name']
    username = my_username.encode('utf-8')
    username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(username_header + username)
    return 'successuful sended the username'

@app.route('/sendChat',methods=['POST'])
def chatFun():
    data = request.get_json()
    message = data['message']
    toAddr = data['to']
    message = message.encode('utf-8')
    toAddr = toAddr.encode('utf-8')
    To_header = f"{len(toAddr):<{HEADER_LENGTH}}".encode('utf-8')
    message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(To_header+toAddr+message_header + message)
    return f'{my_username} > {message.decode("utf-8")}'

@app.route('/recvMess')
def recMes():
    # Receive our "header" containing username length, it's size is defined and constant
    username_header = client_socket.recv(HEADER_LENGTH)

    # If we received no data, server gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
    if not len(username_header):
        print('Connection closed by the server')
        return 'Connection closed by the server'

    # Convert header to int value
    username_length = int(username_header.decode('utf-8').strip())

    # Receive and decode username
    username = client_socket.recv(username_length).decode('utf-8')

    # Now do the same for message (as we received username, we received whole message, there's no need to check if it has any length)
    message_header = client_socket.recv(HEADER_LENGTH)
    message_length = int(message_header.decode('utf-8').strip())
    message = client_socket.recv(message_length).decode('utf-8')

    # Print message
    return f'{username} > {message}'

if __name__ == "__main__":
    HEADER_LENGTH = 10

    IP = "127.0.0.1"
    PORT = 1234

    # Create a socket
    # socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
    # socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to a given ip and port
    client_socket.connect((IP, PORT))

    # Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
    client_socket.setblocking(False)
    app.run(port=5000)