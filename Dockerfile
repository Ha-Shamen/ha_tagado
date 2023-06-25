# Dockerfile

# Creating a python base with shared environment variables
FROM python:3.11.4-bullseye
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
	PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential

# renovate: datasource=pypi depName=poetry versioning=semver
ENV POETRY_VERSION 1.5.1

RUN set -ex; pip install --no-cache-dir poetry==$POETRY_VERSION;

# We copy our Python requirements here to cache them
# and install only runtime deps using poetry
COPY . .
WORKDIR $POETRY_HOME/bin
CMD ["poetry", "shell"] 