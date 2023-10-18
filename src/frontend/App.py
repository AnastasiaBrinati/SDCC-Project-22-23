from flask import Flask, redirect, render_template, url_for, request, session
from flask_session import Session
from loginRPC import sendLoginInfo

app = Flask(__name__)
app.debug = False
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Defining the home page of our site
@app.route("/") 
def menu():
	return render_template("home.html", username="")  # some basic inline html

@app.route("/<string:username>/home", methods=('GET','POST'))
def home(username):
     return render_template("home.html", username=username)  # some basic inline html


# redirecting login button
@app.route('/loginpage')
def loginpage():
    return render_template("login.html")

@app.route('/login', methods=('GET','POST'))
def login():
    if request.method == 'POST':
        """
        Estraggo i dati inseriti dall'utente per
        avviare la procedura di login.
        """
        # Username
        username = request.form.get('inputUsername')
        # Password
        password = request.form.get('inputPassword')

        response = sendLoginInfo(username, password)
        if response == True:
            # Salvataggio dello stato della sessione
            session[username] = username
            return redirect("/"+username+"/home")
    return redirect("/")


# redirecting search button
@app.route('/search')
def search():
    # qua sarebbe da fare * cerca la roba per la città richiesta * e poi ricarica homepage con dati cercati
    return f"Succesfully searched something!"

#logout
@app.route("/<string:username>/logout")
def logout(username):
    if session.get(username) is None:
        stringa = "ERRORE NELLA GESTIONE DELLA SESSIONE."
        return render_template("errore.html", errore=stringa, username=None)

    #termino la sessione relativa all'utente loggato
    session.pop(username)
    return redirect("/")

if __name__ == "__main__":
    app.run()