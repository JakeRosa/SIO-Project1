FROM python:3.10-slim as requirements-stage

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends 

RUN pip install --upgrade pip \
    && pip install --no-cache-dir --upgrade poetry

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-root

COPY . .

RUN poetry install

EXPOSE 5000

CMD ["poetry", "run", "flask", "--debug", "run", "-h", "0.0.0.0"]