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

    fp = open("conn.txt","a")
    fp.write("select username okkk\n")
    fp.close()

    for row in c:
        user = {
            'username': row[0]
        }
        users.append(user)
    c.close()

    if len(users)==0:
        return False
    return True