import socket
from threading import Thread 
import re 
from .request import requestObj

def sendFile(path,*args,**kwargs):
    f=open(path)
    content = f.read()
    for key,value in kwargs.items():
        content=re.sub(r"(\%\%\s*{key}\s*\%\%)".format(key=key),value,content)
    return content




class httpServer:
    """A simple http server library which allows simple actions. Meant to show how a simple http server works

    """
    def __init__(self,host='127.0.0.1',port=8000):
        self.SERVER_HOST=host
        self.SERVER_PORT=port
        self.routes={}
    
    def run(self):
        """Starts the server with the current routes

        """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.SERVER_HOST, self.SERVER_PORT))
        self.server_socket.listen(1)
        
        print(f'Listening on port {self.SERVER_PORT} ...')
        Thread(target=self.listen_for_connections).start()


    def handle_request(self,client_connection):
        request = client_connection.recv(1024).decode()
        headers = request.split('\n')
        requestedRoute = headers[0].split()[1]
        method=headers[0].split()[0]

        params={}
        if method=='GET':
            paramstr=requestedRoute.split("?")[-1]
            requestedRoute=requestedRoute.split("?")[0]
            if paramstr==requestedRoute:
                params={}
            else:
                arrParams=paramstr.split("&")
                for pair in arrParams:
                    key,value=pair.split("=")
                    params[key]=value
        else:
            paramstr=headers[-1]
            arrParams=paramstr.split("&")
            for pair in arrParams:
                key,value=pair.split("=")
                params[key]=value
        print(f"{method} request to {requestedRoute}")
        response='HTTP/1.0 404 NOT FOUND\n\nRoute Not Found'
        if requestedRoute in self.routes.keys():
            if method in self.routes[requestedRoute]["methods"]:
                try:
                    req=requestObj(params,method)
                    response = 'HTTP/1.0 200 OK\n\n' + self.routes[requestedRoute]["function"](req)
                except FileNotFoundError:
                    response = 'HTTP/1.0 404 NOT FOUND\n\nFile Not Found'
        client_connection.sendall(response.encode())
        client_connection.close()

    def route(self,*args,**kwargs):        
        def inner(func):
            self.routes[args[0]]={"methods":kwargs["methods"],"function":func}
            return func
        return inner
    def listen_for_connections(self):
        while True:
                client_connection,client_address = self.server_socket.accept()
                Thread(target=self.handle_request,args=(client_connection,)).start() 