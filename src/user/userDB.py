import mysql.connector


# who is the db?
PORT = '3306'

"""
Recupera un
utente che corrisponde alle credenziali
inserite.
"""
def checkCredentials(username, password):

    con = mysql.connector.connect(user='root',password='a',host='mysql',database='users')
    c = con.cursor()

    fp = open("conn.txt","a")
    fp.write("connection open, but there is no table\n")
    fp.close()

    users = []    
    c.execute(f"""SELECT username FROM Users WHERE username='{username}' AND password='{password}'""")

    for row in c:
        user = {
            'username': row[0]
        }
        users.append(user)

    if len(users)==0:
        ans = False
    else:
        ans = True

    favs = []    
    c.execute(f"""SELECT city FROM Favourites WHERE username='{username}'""")
    for row in c:
        city = {
            'city': row[0]
        }
        favs.append(city['city'])
    
    c.close()

    return ans,favs

def addToFav(username, city):
    con = mysql.connector.connect(user='root',password='a',host='mysql',database='users')
    c = con.cursor()
    
    # insert into Users una lista(?)
    #oppure devo creare una nuova tabella
    c.execute(f"""INSERT INTO Favourites VALUES('{username}','{city}')""")
    c.close()

    # se è andata a buon fine
    return True
