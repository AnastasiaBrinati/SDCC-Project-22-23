from flask import Flask, redirect, render_template, request, session, jsonify
from flask_session import Session
from loginRPC import sendLoginInfo
from searchRPC import sendCityInfo

app = Flask(__name__)
app.debug = False
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Defining the home page of our site
@app.route("/") 
def menu():
	return render_template("home.html")  # some basic inline html

@app.route("/<string:username>/home", methods=('GET','POST'))
def home(username):
    try:
        diz = session.pop(username)
        session[username] = username
    except Exception as e:
        return redirect("/loginpage")

    # sarebbe carino se ad ogni avvio venisse mostrato il clima in una città diversa, ma on so se questo impatta le prestazion,
    # meglio farlo un altro momento
    #response = sendCityInfo("Roma")
    return render_template("Home.html")


# redirecting login button
@app.route('/loginpage')
def loginpage():
    return render_template("login.html")

@app.route('/login', methods=('GET','POST'))
def login():

    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if(username == "" or password== ""):
            # campi non riempiti
            return jsonify({"correct": False, "username": ""})
        
        response = sendLoginInfo(username, password)
        if(response==True):
            return jsonify({"correct": True, "username": username})
        
    except Exception as e:
        return jsonify({"message": "Si è verificato un errore: " + str(e)})

    redirect("/")
    return jsonify({"correct": False, "username": ""})


# redirecting search button
@app.route('/search', methods=('GET','POST'))
def search():

    try:
        data = request.get_json()
        city = data.get('city')

        if(city == ""):
            # campi non riempiti
            redirect("/")
            return jsonify({"correct": False, "city": ""})
        
        response = sendCityInfo(city)

        #if(response==True):
        # per ora sempre True
        return jsonify({"correct": True, "city": city, "temperature": str(response[0]), "humidity":str(response[1]), "cloudiness":str(response[2])})
        
    except Exception as e:
        return jsonify({"message": "Si è verificato un errore: " + str(e)})


    #redirect("/")
    #return jsonify({"city": str(city), "temperature": str(response[0]), "humidity":str(response[1]), "cloudiness":str(response[2])})



#logout
@app.route("/logout/<input_parameter>", methods=('GET','POST'))
def logout(username):
    if session.get(username) is None:
        stringa = "ERRORE NELLA GESTIONE DELLA SESSIONE."
        return render_template("errore.html", errore=stringa, username=None)

    fp = open("what_is_going_on.txt", "a")
    fp.write("\n wtf: username: " + username)
    fp.close()
    #termino la sessione relativa all'utente loggato
    session.pop(username)
    return

if __name__ == "__main__":
    app.run()