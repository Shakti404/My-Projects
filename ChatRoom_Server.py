import socket
serv_soc = socket.socket()
host_name = socket.gethostname()
ip = socket.gethostbyname(host_name)
port = 4780
serv_soc.bind((host_name, port))
print(host_name, '{}'.format(ip))
name = input("Enter name: ")
serv_soc.listen(5)
print('Waiting For Connections...')
connection, addr = serv_soc.accept()
print("Recieved Connection From ", addr[0], "(", addr[1], ")\n")
print("Connection Established. Connected from : {}, {}".format(addr[0], addr[0]))
client_name = connection.recv(1024)
client_name = client_name.decode()
print(client_name + ' has connected.')
print('Enter [Bye] to leave the chat room.')
connection.send(name.encode())
while True:
    message = input('Me : ')
    if message == '[Bye]':
        message = 'Good Night'
        connection.send(message.encode())
        print('\n')
        break
    # else:
    connection.send(message.encode())
    message = connection.recv(1024)
    message = message.decode()
    print(client_name, ': ', message)