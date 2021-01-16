from httpserver import *


app=httpServer()

@app.route("/login",methods=['GET','POST'])
def home(params):
    return sendFile("htdocs/index.html",name=params['name'])

@app.route("/",methods=['GET'])
def root(params):
    return "<h1>Root</h1>"

app.run()