FROM ubuntu
USER root

WORKDIR /app

RUN apt-get update && apt-get install -y python3.10
# RUN apt-get install -y python3.10
RUN apt-get install -y python3-distutils python3-pip python3-apt

COPY . .

RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP App.py

EXPOSE 5000
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]