FROM python:3

WORKDIR /application

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "/usr/local/bin/flask", "run", "--host=0.0.0.0" ]

