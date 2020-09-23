import socket
import time
print('Client Server...')
time.sleep(1)
client_soc = socket.socket()
shost = socket.gethostname()
ip = socket.gethostbyname(shost)
print(shost, '({})'.format(ip))
server_host = input('Enter server\'s IP address: ')
name = input('Enter Client\'s name: ')
port = 4780
print('Trying to connect to the server: {}, ({})'.format(server_host, port))
time.sleep(1)
client_soc.connect((server_host, port))
print("Connected To The Server...\n")
client_soc.send(name.encode())
server_name = client_soc.recv(1024)
server_name = server_name.decode()
print('{} has joined...'.format(server_name))
print('Enter Bye to exit.')
while True:
    message = client_soc.recv(1024)
    message = message.decode()
    print(server_name, ": ", message)
    message = input(str("Me : "))
    if message == "Bye":
        message = "Leaving the Chat room"
        client_soc.send(message.encode())
        print("\n")
        break
    client_soc.send(message.encode())
