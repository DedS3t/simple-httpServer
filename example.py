from httpserver import *


app=httpServer()

@app.route("/login",methods=['GET','POST'])
def home(request):
    return sendFile("htdocs/index.html",name=request.params['name'])

@app.route("/",methods=['GET'])
def root(request):
    return "<h1>Root</h1>"

app.run()