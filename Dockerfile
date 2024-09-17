FROM ubuntu:18.04

# Maintainer of the docker image, not the code!
MAINTAINER "Ian Hinder <ian.hinder@manchester.ac.uk>"

RUN apt-get update -y && \
    apt-get install -y python3 python3-pip python3-requests graphviz libgraphviz-dev curl && \
    rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

ARG last_update
ENV LAST_UPDATE=$last_update

ENTRYPOINT [ "python3" ]

CMD [ "application.py" ]

# TODO: in docker 25 and later, we should use --start-interval and
# --start-period to perform more frequent checks on startup to speed
# up tests
HEALTHCHECK --interval=10s CMD curl --fail http://localhost:5000 || exit 1   
