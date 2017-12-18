FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y python python-pip python-virtualenv nginx gunicorn supervisor

# Setup flask application
RUN mkdir -p /deploy/neural_net
COPY net/service /deploy/neural_net
RUN mkdir -p /deploy/neural_api
COPY api/core /deploy/neural_api
COPY requirements.txt /deploy
RUN pip install -r /deploy/requirements.txt --no-cache-dir

# Setup nginx
RUN rm /etc/nginx/sites-enabled/default
COPY flask.conf /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/flask.conf /etc/nginx/sites-enabled/flask.conf
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

# Setup supervisord
RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY gunicorn.conf /etc/supervisor/conf.d/gunicorn.conf

# Start processes
CMD ["/usr/bin/supervisord"]
