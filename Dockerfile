FROM arquiteturansj/flask:2.2

WORKDIR /var/www/html

COPY . /var/www/html

EXPOSE 5000

RUN python3 -m pip install -r /var/www/html/requirements.txt --no-cache-dir

CMD python3 /var/www/html/nasajon/wsgi.py
