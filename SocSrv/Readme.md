this module is for Socket Service

SocSrvMain: 
1. runs SocketServer that allow to communicate other modules and send messages in telegram bot
2. runs Admin client

Socket Server: 
1. handling messages on port(1977) and forwarding messages(dict) to clients by name
2. listen sockets for clients and matching them with names.
3. every new client send hello message to server

Admin Client:
1. just a client, that send and receive messages and answer them

