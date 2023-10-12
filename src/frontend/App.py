from flask import Flask, redirect, render_template, url_for
from loginRPC import *


app = Flask(__name__)

# Defining the home page of our site
@app.route("/") 
def home():
	return render_template("home.html")  # some basic inline html

@app.route("/<name>")  # this sets the route to this page
def user(name):
    return f"Hello {name}!"

# The url_for function takes an argument that is the name of the function that you want to redirect to.
# Now whenever we visit /admin we will be redirected home.
@app.route("/admin")
def admin():
	return redirect(url_for("home"))

# redirecting login button
@app.route('/loginpage')
def loginpage():
    # asking loginRPC
    response = sendLoginInfo("Giulio")

    #print(response)
    return f"Hello {response}!"
    #return render_template("login.html")

# redirecting search button
@app.route('/search')
def search():
    # qua sarebbe da fare * cerca la roba per la città richiesta * e poi ricarica homepage con dati cercati
    return f"Succesfully searched something!"

if __name__ == "__main__":
    app.run()