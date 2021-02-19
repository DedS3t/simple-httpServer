from httpserver import *


app=httpServer(port=7000)

@app.route("/test",methods=['GET','POST'])
def home(request):
    return sendFile("htdocs/index.html",name=request.params['name'])

@app.route("/",methods=['GET'])
def root(request):
    return "<h1>Hello World!</h1>"

app.run()