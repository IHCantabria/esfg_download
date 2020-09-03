# set base image (host OS)
FROM python:3.7.6

RUN mkdir -p /code
RUN mkdir -p /code/ESFG
# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
ADD ESFG /code/ESFG
COPY setup.py .
COPY Ejemplo.py .
COPY Execute.sh .

# install dependencies
RUN ls -la /code/*
RUN pip install -e. 
RUN pip install MyProxyClient
RUN chmod +x Execute.sh

# copy the content of the local src directory to the working directory
#COPY src/ .

# command to run on container start
CMD /bin/bash Execute.sh