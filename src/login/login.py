import grpc
import time
import logging
import sys

from concurrent import futures
from proto import Registration_pb2
from proto import Registration_pb2_grpc

from loginDB import *
from loginDiscovery import *


# ------------------------------------------------------ DISCOVERY -----------------------------------------------------
"""
La seguente lista contiene inizialmente solo il
default discovery server per il microservizio di Registration.
Tuttavia, nel momento in cui si registra, all'interno possono
essere inserite le informazioni relative all'altro
discovery server.
"""
all_discovery_servers = ['code_discovery_2:50060']
# ------------------------------------------------------ DISCOVERY -----------------------------------------------------

CHUNK_DIM = 1000
numByteTrasmessiMod = 0
numIterazioniMassimo = 0
MAX = 1000


class UsersInfoServicer(Registration_pb2_grpc.UsersInfoServicer):


    """
    Implementa la procedura di Login.
    """
    def login(self, Credentials, context):

        username_d = Credentials.username
        password_d = Credentials.password

        logger.info("Richiesta procedura di accesso: [" + username_d + "," + password_d + "]")

        """
        Verifico se l'utente che sta tentando di eseguire
        il Login effettivamente è presente all'interno del
        sistema. I parametri passati sono dati cifrati.
        """
        user = retrieveUser(Credentials.username, Credentials.password)

        if user.isCorrect:
            logger.info("Procedura di accesso conclusa con successo: [" + username_d + "," + password_d + "]")
            value = user.storedType.__bytes__()
            output = Registration_pb2.SignInResponse(storedType=value, isCorrect=user.isCorrect)
        else:
            logger_warnings.warning("Procedura di accesso conclusa senza successo: [" + username_d + "," + password_d + "]")
            output = Registration_pb2.SignInResponse(storedType=bytes(0), isCorrect=False)
        
        return output



"""
Costruisco un file di LOG in cui andare ad
inserire le richieste che giungono dagli altri
microservizi. Inoltre, inserisco delle informazioni
di warnings nel momento in cui le richieste falliscono.
"""
logging.basicConfig(filename="registration.log", format=f'%(levelname)s - %(asctime)s - %(message)s')
logger = logging.getLogger("registrationInfo")
logger_warnings = logging.getLogger("registrationWarnings")
logger.setLevel(logging.INFO)
logger_warnings.setLevel(logging.WARNING)

#create gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
Registration_pb2_grpc.add_UsersInfoServicer_to_server(UsersInfoServicer(), server)

logger.info('Avvio del server in ascolto sulla porta 50051...')
server.add_insecure_port('[::]:50051')
server.start()
logger.info('Server avviato con successo.')



# ------------------------------------------- DISCOVERY -------------------------------------------------------------------------------------------

"""
Registrazione del microservizio al Discovery Server di default.
Inizialmente il microservizio di registration è a conoscenza solamente
del discovery server 2
"""
logger.info('[DISCOVERY SERVER] Richiesta registrazione del microservizio sul discovery server...')
discovery_servers = put_discovery_server(all_discovery_servers, logger)
logger.info('[DISCOVERY SERVER] Registrazione del microservizio sul discovery server ' + all_discovery_servers[0] + ' avvenuta con successo.')



# Registro l'eventuale altro discovery server
for item in discovery_servers:
    try:
        all_discovery_servers.index(item)
    except:
        # Inserisco il Discovery Server mancante all'interno della lista.
        all_discovery_servers.append(item)


logger.info('[DISCOVER SERVERS LIST] I discovery servers noti sono:\n')
for item in all_discovery_servers:
    logger.info(item + '\n')
logger.info('\n\n')

# ------------------------------------------- DISCOVERY -------------------------------------------------------------------------------------------

# ???

try:
    while True:
        time.sleep(86400)   #86400 seconds == 24 hours
except KeyboardInterrupt:
    server.stop(0)