import grpc
import sys
import logging
import time

from security import Security
from proto import Registration_pb2
from proto import Registration_pb2_grpc
from proto import Discovery_pb2
from proto import Discovery_pb2_grpc


ADDR_PORT = ''
DISCOVERY_SERVER = 'code_discovery_2:50060'


class Output:
    def __init__(self, storedType, isCorrect):
        self.isCorrect = isCorrect
        self.storedType = storedType




"""
Ha il compito di recuperare la porta su cui
il microservizio registration è in ascolto.
"""
def discovery_registration():
    global ADDR_PORT
    """
    Si tenta di contattare il discovery server registrato
    per ottenere la porta su cui il servizio di registration è in
    ascolto. Se la chiamata dovesse fallire, si attendono 5
    secondi per poi eseguire nuovamente il tentativo di connessione.
    """
    while(True):
        try:
            # Provo a connettermi al server.
            channel = grpc.insecure_channel(DISCOVERY_SERVER)
            stub = Discovery_pb2_grpc.DiscoveryServiceStub(channel)
            # Ottengo la porta su cui il microservizio di Registration è in ascolto.
            res = stub.get(Discovery_pb2.GetRequest(serviceName="frontend" , serviceNameTarget="registration"))
            if (res.port == -1):
                # Il discovery server ancora non è a conoscenza della porta richiesta.
                time.sleep(5)
                continue            
            ADDR_PORT = res.serviceName + ':' + res.port
            break
        except:
            # Problema nella connessione con il server.
            time.sleep(5)
            continue




"""
Instanzia un canale di comunicazione con il
microservizio che gestisce le iscrizioni per
l'applicazione. Viene passato in input un
messaggio contenente tutte le informazioni
necessarie per l'iscrizione.
"""
def sendSignUpInfo(username, password, passwordConfirm, userType, airline, cartaDiCredito):
    """
    Verifico se il frontend già è a conoscenza della porta
    su cui contattare il micorservizio di registration.
    """
    if (ADDR_PORT == ''):
        discovery_registration()

    channel = grpc.insecure_channel(ADDR_PORT)
    stub = Registration_pb2_grpc.UsersInfoStub(channel)

    """
    Implemento meccanismi di sicurezza:
    - Cifratura: Cifratura dei dati utilizzando AES-128
    """
    cipher = Security(b"mysecretpassword")

    # Password
    ciphertextPassword, iv = cipher.encryptData(bytes(password, 'utf-8'))

    # Password conferma
    ciphertextPasswordConf, iv = cipher.encryptData(bytes(passwordConfirm, 'utf-8'))

    # Username
    ciphertextUsername, iv = cipher.encryptData(bytes(username, 'utf-8'))

    # Carta di credito
    ciphertextCartaDiCredito, iv = cipher.encryptData(bytes(cartaDiCredito, 'utf-8'))

    # Tipologia utente
    ciphertextUserType, iv = cipher.encryptData(bytes(userType, 'utf-8'))

    if airline is not None:
        """
        L'utente ha specificato una compagnia
        aerea. Ossia, non sarà un utente di tipo
        Turista.
        """
        ciphertextAirline, iv = cipher.encryptData(bytes(airline, 'utf-8'))
    else:
        ciphertextAirline = None

    """
    Invio della richiesta di iscrizione dell'utente.
    Il valore di output sarà TRUE se è andata a buon
    fine; altrimenti, sarà FALSE.

    I parametri di input sono dati cifrati. Poiché
    queste informazioni sono sensibili, esse viaggiano
    cifrate tra i microservizi. Inoltre, abbiamo anche
    i vari digest per controllare l'integrità dei messaggi.
    """

    output = stub.SignUp(Registration_pb2.SignUpInfo(username=ciphertextUsername, password=ciphertextPassword, passwordConfirm=ciphertextPasswordConf, userType=ciphertextUserType, airline=ciphertextAirline, cartaDiCredito=ciphertextCartaDiCredito))

    return output




"""
Instanzia un canale di comunicazione con il
microservizio che gestisce il login per
l'applicazione. Viene passato in input un
messaggio contenente tutte le informazioni
necessarie per effettuare il login.
"""
def sendCredentials(username, password):
    """
    Verifico se il fronted già è a conoscenza della porta
    su cui contattare il micorservizio di registration.
    """
    if (ADDR_PORT == ''):
        discovery_registration()

    channel = grpc.insecure_channel(ADDR_PORT)
    stub = Registration_pb2_grpc.UsersInfoStub(channel)

    """
    Implemento meccanismi di sicurezza:
    - Cifratura: Cifratura dei dati utilizzando AES-128
    """
    cipher = Security(b"mysecretpassword")

    # Username
    ciphertextUsername, iv = cipher.encryptData(bytes(username, 'utf-8'))

    # Password
    ciphertextPassword, iv = cipher.encryptData(bytes(password, 'utf-8'))
    
    output = stub.SignIn(Registration_pb2.Credentials(username=ciphertextUsername, password=ciphertextPassword))

    storedTypeString = cipher.decryptData(output.storedType).decode()

    out = Output(storedTypeString, output.isCorrect)
    
    return out