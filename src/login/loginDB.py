import mysql.connector


# who is the db?
PORT = '3306'

"""
Recupera un
utente che corrisponde alle credenziali
inserite.
"""
def checkCredentials(username, password):

    fp = open("connection.txt", "a")
    fp.write("mi sto connettendo..\n")
    fp.close()
    con = mysql.connector.connect(user='root',password='a',host='mysql',database='users')
    fp = open("connection.txt", "a")
    fp.write(username+" connessa..\n")
    fp.close()
    c = con.cursor()

    users = []    
    c.execute(f"""SELECT username FROM Users WHERE username='{username}' AND password='{password}'""")

    for row in c:
        user = {
            'username': row[0]
        }
        users.append(user)
    c.close()

    if len(users)==0:
        return False
    return True