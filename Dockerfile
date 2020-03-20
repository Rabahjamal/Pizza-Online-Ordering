FROM ubuntu:18.04

RUN apt update && apt install -y git python3-dev libffi-dev libssl-dev python3-pip

ENV DEBIAN_FRONTEND=noninteractive 

RUN apt-get install -y postgresql python-psycopg2 libpq-dev

RUN pip3 install psycopg2

USER postgres

RUN    /etc/init.d/postgresql start &&\
    psql --command "CREATE USER admin2 WITH SUPERUSER PASSWORD 'admin2';" && psql --command "CREATE DATABASE pizza_orders;" && psql --command "ALTER ROLE admin2 SET client_encoding TO 'utf8';" && psql --command "ALTER ROLE admin2 SET default_transaction_isolation TO 'read committed';" && psql --command "ALTER ROLE admin2 SET timezone TO 'UTC';" && psql --command "GRANT ALL PRIVILEGES ON DATABASE pizza_orders TO admin2;" && psql --command "\q"

# Expose the PostgreSQL port
EXPOSE 5432

# Add VOLUMEs to allow backup of config, logs and databases
VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]

# Set the default command to run when starting the container
CMD ["/usr/lib/postgresql/9.3/bin/postgres", "-D", "/var/lib/postgresql/9.3/main", "-c", "config_file=/etc/postgresql/9.3/main/postgresql.conf"]

USER root

#RUN /etc/init.d/postgresql start
CMD ["/etc/init.d/postgresql", "start"]
RUN cd /opt && git clone https://github.com/Rabahjamal/Pizza-Online-Ordering.git && cd Pizza-Online-Ordering && pip3 install -r requirements.txt && python3 manage.py migrate && python3 manage.py makemigrations && python3 manage.py runserver
