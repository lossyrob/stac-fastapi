FROM python:3.8-slim

# Any python libraries that require system libraries to be installed will likely
# need the following packages in order to build
RUN apt-get update && apt-get install -y build-essential git

RUN pip install pipenv
ENV PIPENV_NOSPIN=true
ENV PIPENV_HIDE_EMOJIS=true
ENV CURL_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

ARG install_dev_dependencies=true

WORKDIR /app

COPY Pipfile Pipfile.lock setup.py ./
RUN pipenv install --pre --deploy --ignore-pipfile ${install_dev_dependencies:+--dev}

# Use a lock of stac-pydantic which pins to this fork's version and
# has some fixes.
# This will go away with this fork once we move to the new refactored codebase.
RUN pipenv install   --pre git+https://github.com/lossyrob/stac-pydantic@v1.3.8-PC-BETA#egg=stac-pydantic

COPY . ./

ENV APP_HOST=0.0.0.0
ENV APP_PORT=80
ENV RELOAD=""

ENTRYPOINT ["pipenv", "run"]
CMD if [ "$RELOAD" ]; then uvicorn stac_api.app:app --host=${APP_HOST} --port=${APP_PORT} --reload ; \
    else gunicorn stac_api.app:app --preload -k uvicorn.workers.UvicornWorker --bind ${APP_HOST}:${APP_PORT} --log-level info; fi