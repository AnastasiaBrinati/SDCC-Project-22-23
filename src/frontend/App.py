from flask import Flask, redirect, render_template, request, session, jsonify
from flask_session import Session
from loginRPC import sendLoginInfo
from searchRPC import weatherNow, weatherPast, weatherForecast

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
        fp=open("errorilogin.txt", "a")
        fp.write("\necco la response: "+str(days))
        fp.close()
        return jsonify({"message": "Si è verificato un errore: " + str(e)})

    redirect("/")
    return jsonify({"correct": False, "username": ""})


# redirecting search button
@app.route('/search_now', methods=('GET','POST'))
def search_now():

    try:
        data = request.get_json()
        city = data.get('city')

        if(city == ""):
            # campi non riempiti
            redirect("/")
            return jsonify({"correct": False, "city": ""})
        
        response = weatherNow(city)
        fp=open("errorinow.txt", "a")
        fp.write("ecco la response: "+str(response))
        fp.close()
        return jsonify({"correct": True, "city": city, "temperature": str(response[0]), "humidity":str(response[1]), "cloudiness":str(response[2])})
        
    except Exception as e:
        fp=open("errorinow.txt", "a")
        fp.write("\necco la response: "+str(days))
        fp.close()
        return jsonify({"message": "Si è verificato un errore: " + str(e)})

# redirecting past search button
@app.route('/search_past', methods=('GET','POST'))
def search_past():

    try:
        data = request.get_json()
        city = data.get('city')

        if(city == ""):
            # campi non riempiti
            redirect("/")
            return jsonify({"correct": False, "city": ""})
        
        response = weatherPast(city)

        fp = open("errori.txt", "a")
        fp.write("dentro search_past: "+str(response))
        fp.close()
        return jsonify({"correct": True, "city": city, "max_temperature": str(response[0]), "min_temperature":str(response[1]), "avg_temperature":str(response[2]), "max_humidity": str(response[3]), "min_humidity":str(response[4]), "avg_humidity":str(response[5]),  "avg_cloudcover":str(response[6])})
        
    except Exception as e:
        fp=open("erroripast.txt", "a")
        fp.write("\necco la response: "+str(days))
        fp.close()
        return jsonify({"correct": False, "message": "Si è verificato un errore: " + str(e)})
    
# redirecting forecast search button
@app.route('/search_forecast', methods=('GET','POST'))
def search_forecast():

    try:
        data = request.get_json()
        city = data.get('city')

        fp=open("erroriforecast.txt", "a")
        fp.write("ecco la city: "+city)
        fp.close()

        if(city == ""):
            # campi non riempiti
            redirect("/")
            return jsonify({"correct": False, "city": ""})
        
        days = weatherForecast(city)
        fp=open("erroriforecast.txt", "a")
        fp.write("\necco la response: "+str(days))
        fp.close()
        return jsonify({"correct": True, "city": city, "day1": days[0], "day2": days[1], "day3": days[2], "day4": days[3], "day5": days[4]})
        
    except Exception as e:
        fp=open("erroriforecast.txt", "a")
        fp.write("\necco l' exception: "+str(e))
        fp.close()
        return jsonify({"message": "Si è verificato un errore: " + str(e)})

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