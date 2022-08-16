# default to python 3.10
ARG PYTHON_VERSION=3.10

# specify a version
FROM python:${PYTHON_VERSION}
LABEL maintainer="Mirko Mälicke"

# build the structure
RUN mkdir -p /src/geostat_api
RUN mkdir -p /src/data
RUN mkdir -p /src/logs

# copy the sources
COPY ./geostat_api /src/geostat_api
COPY ./requirements.txt /src/requirements.txt
COPY ./setup.py /src/setup.py
COPY ./README.md /src/README.md
COPY ./LICENSE /src/LICENSE
COPY ./start.sh /src/start.sh

# install
RUN pip install --upgrade pip
RUN cd /src && pip install -e .

# install gunicorn for production use
RUN pip install gunicorn

# create the streamlit entrypoint
WORKDIR /src
CMD [ "bash", "start.sh" ]
