##### More features coming soon... feel free to fork it and make it better!
A simple flaskish http server library. Meant for learning purposes to learn how a web server works.

Flaskish?
The library supports a similar to flask syntax style
```
# example code
from httpserver import *

app=httpServer()

@app.route("/login",methods=['GET','POST'])
def home(request):
    return sendFile("htdocs/index.html",name=request.params['name'])

@app.route("/",methods=['GET'])
def root(request):
    return "<h1>Root</h1>"

app.run()
```

What it currently supports
- Configurable Routes
- Able to receive GET,POST,UPDATE,DELETE requests
- Able to get "GET" request params and x-www-form-urlencoded "POST" request params 
- Send html files back
- Comes with simple templating builtin (only supports variables)



### Documentation
##### If you would like to see an example checkout the example.py file 

Start of by creating an instance of httpserver optionally specifying the host and port
``` 
from httpserver import *
app=httpServer()
```
Now you are able to start adding routes. For routes the library uses decorators just like in flask.
```
# Setting route for /login which accepts both GET and POST requests
@app.route('/login',methods=["GET","POST"])
def login(request):
    # specify function which will get executed. A argument will be passed with an object "requestObj" which contains the property "method" 
    # which is the request method and "params" which is a dict with the parameters that are passed with either GET or POST
    return "This is the login page!"

```
You can also redirect the user using redirect().
```
@app.route("/",methods=['GET'])
def root(request):
    return redirect("/login?name=John") # redirect takes in 1 argument which is the url. 
    # The url can be on the same server or anywhere on the internet, eg. "http://www.google.com" would also work
```


You are also able to send back a file 
```
# Creating root route which accepts only GET
@app.route('/',methods=["GET"])
def root(request):
    return sendFile("index.html") # render html file to 
```
The library comes with simple built in templating system. The system allows you to pass variables to html files using "%% varname %%""
```
@app.route('/test',methods=["GET"])
def test(request):
    return sendFile("index.html", name=request.params['name']) # params['name'] = the GET parameter 'name'. 
    # This will change all the occurences '%% name %%' to whatever the passed in argument would be. 
    # Eg. yourHost:port/test?name=john. This will then change '%%name%%'to John in the index.html file.
```



