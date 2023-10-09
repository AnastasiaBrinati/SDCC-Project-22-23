import boto3
from boto3.dynamodb.types import Binary
import sys



DYNAMODB = 'dynamodb'
REGIONE = 'us-east-1'
TABELLA_UTENTE = 'Utente'



class LoggedUser:
    def __init__(self, username, storedType, isCorrect):
        # Username dell'utente (cifrato)
        self.username = username
        # Tipologia dell'utente (cifrato)
        self.storedType = storedType
        # Esito del processo di iscrizione
        self.isCorrect = isCorrect



"""
Registra il nuovo utente con le informazioni passate
come parametri.
"""
def storeUser(username, password, userType_d, airline, cartaDiCredito, userType):

    if userType_d == 'Turista':
        """
        Il check viene fatto sul valore decodficato
        mentre la scrittura nel DB è codificata.
        """
        typeToStore = userType
    else:
        """
        Se l'utente che richiede l'iscrizione
        non è un Turista, allora il suo tipo
        corrisponde alla compagnia aerea.
        """
        typeToStore = airline
    
    try:
        dynamodb = boto3.resource(DYNAMODB, REGIONE)
        table = dynamodb.Table(TABELLA_UTENTE)
        table.put_item(
            Item = {
                'Username': Binary(username),
                'Password': Binary(password),
                'Tipo': Binary(typeToStore),
                'Carta di credito': Binary(cartaDiCredito)
            }
        )
    except Exception:
        return False
    
    return True



"""
Verifica se esiste già un utente iscritto nel
sistema che ha lo username inserito come parametro
per il processo di iscrizione.

Ritorna TRUE se non c'è già alcun utente
che ha lo username richiesto; altrimenti,
ritorna FALSE.
"""
def isNewUser(username):
    try:
        dynamodb = boto3.resource(DYNAMODB,REGIONE)
        table = dynamodb.Table(TABELLA_UTENTE)
        response = table.get_item(
            Key = {
                'Username': username,
            }
        )
    except Exception:
        return False

    if 'Item' in response:
        return False
    else:
        return True



"""
Verifica se esiste nel sistema un
utente che corrisponde alle credenziali
inserite.
"""
def retrieveUser(username, password):
    dynamodb = boto3.resource(DYNAMODB, REGIONE)
    table = dynamodb.Table(TABELLA_UTENTE)

    #read from 'Utente' table in DynamoDB
    response = table.get_item(
        Key = {
            'Username': username,
        }
    )

    if not ('Item' in response):
        """
        Se lo username inserito dall'utente non esiste,
        allora la procedura di Login termina senza successo.
        """
        user = LoggedUser(None, None, False)
        return user
    
    item = response['Item']
    actualPassword = item['Password']

    """
    Verifco se la password inserita dall'utente
    insieme allo username coincide con la password
    memorizzata nel Database. Viene fatto un confronto
    tra valori cifrati.
    """
    if actualPassword != password:
        """
        Se la password inserita dall'utente non corrisponde
        con quella memorizzata all'interno del Database, 
        allora la procedura di Login termina senza successo.
        """
        user = LoggedUser(None, None, False)
        return user

    """
    Le credenziali inserite corrispondono
    effettivamente ad un utente che in passato
    si è registrato al sistema. Di ocnseguenza,
    la procedura di Login termina con successo.
    """
    usernameField = item['Username']            # Valore cifrato.
    userType = item['Tipo']                     # Valore cifrato.
    user = LoggedUser(usernameField, userType, True)

    return user