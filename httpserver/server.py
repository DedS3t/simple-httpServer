import socket
from threading import Thread 
import re 
from .request import requestObj

"""Parses expression into (if condition, content)
"""
def _parse_expression(expression):
    # isolate if statement
    isolate_if=re.findall(r"if\([\s\S]+?\)",expression)
    isolate_if=re.sub(r"\s",'',isolate_if[0])
    return isolate_if[3:-1], re.sub(r"\(%[\s\S]*?%\)",'',expression)

"""Returns content of file after templating
"""
def sendFile(path,*args,**kwargs):
    # read file
    f=open(path)
    content = f.read()
    # loop through sent variables and change approriate values
    for key,value in kwargs.items():
        content=re.sub(r"(\%\%\s*{key}\s*\%\%)".format(key=key),value,content)
    # find all if statements
    statements=re.findall(r"(\(%[ \t]*if\(\s*[\s\S]+?[ \t]*\)\s*%\)[\s\S]*?\(%[ \t]*endif[ \t]*%\))",content)
   
    # parse each if statement and eval
    for expression in statements:
        cond,cont=_parse_expression(expression)
        if eval(cond,kwargs): content=content.replace(expression,cont)
        else: content=content.replace(expression,'')
        
    return content

class redirect:
    def __init__(self,path):
        self.path=path


class httpServer:
    """A simple http server library which allows simple actions. Meant to show how a simple http server works

    """
    def __init__(self,host='127.0.0.1',port=8000):
        self.SERVER_HOST=host
        self.SERVER_PORT=port
        self.threads=0
        self.routes={}
    
    def run(self):
        """Starts the server with the current routes

        """

        # sets server socket config
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.SERVER_HOST, self.SERVER_PORT))
        self.server_socket.listen(1)
        
        print(f'Listening on port {self.SERVER_PORT} ...')
        Thread(target=self.listen_for_connections).start()

    """Handles the incoming request, sends output to socket
    """
    def handle_request(self,client_connection):
        self.threads+=1
        # parse header
        request = client_connection.recv(1024).decode()
        headers = request.split('\n')
        requestedRoute = headers[0].split()[1]
        method=headers[0].split()[0]

        params={}
        if method=='GET':
            # parse get request
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
            # parse other requests, eg POST
            paramstr=headers[-1]
            arrParams=paramstr.split("&")
            for pair in arrParams:
                key,value=pair.split("=")
                params[key]=value
        print(f"{method} request to {requestedRoute}")
        response='HTTP/1.0 404 NOT FOUND\n\nRoute Not Found'
        # executes corresponding route function and sets response
        if requestedRoute in self.routes.keys():
            if method in self.routes[requestedRoute]["methods"]:
                try:
                    req=requestObj(params,method)
                    content=self.routes[requestedRoute]["function"](req)
                    if isinstance(content,redirect):
                        response=f'HTTP/1.0 301 Moved Permanently\nLocation: {content.path}'
                    else:
                        response = 'HTTP/1.0 200 OK\n\n' + content
                except FileNotFoundError:
                    response = 'HTTP/1.0 404 NOT FOUND\n\nFile Not Found'
        client_connection.sendall(response.encode())
        client_connection.close()
        self.threads-=1

    """Decorator for adding routes
    """
    def route(self,*args,**kwargs):        
        def inner(func):
            self.routes[args[0]]={"methods":kwargs["methods"],"function":func}
            return func
        return inner
    """Waits for incoming connections, when connection is established the connection is handled in another thread
    """
    def listen_for_connections(self,verbose=0):
        while True:
                client_connection,client_address = self.server_socket.accept()
                if verbose==1: print(f"Client: {client_address[0]} requested, current threads: {self.threads}")
                Thread(target=self.handle_request,args=(client_connection,)).start() 