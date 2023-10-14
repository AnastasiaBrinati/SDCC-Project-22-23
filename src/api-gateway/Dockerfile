FROM ubuntu
USER root

# Setto la working directory.
WORKDIR /app


# Installo la  versione necessaria di Python 3.
RUN apt-get update && apt-get install -y python3.10
# RUN apt-get install -y python3.10
RUN apt-get install -y python3-distutils python3-pip python3-apt

# Copio i file necessari per il setup e per il microservizio da eseguire nel container.
COPY . .
COPY ./credentials /root/.aws/

RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Mi consente di poter utilizzare il comando DIG per risolvere gli indirizzi IP necessari.
RUN apt-get install -y dnsutils

# Devo modificare i permessi di accesso per poter eseguire il file bash
RUN chmod a+x setup.sh

EXPOSE 50060

# Lancio il file di configurazione.
CMD ["./setup.sh"]