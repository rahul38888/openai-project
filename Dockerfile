FROM python:3.10.2-slim-buster AS builder

RUN apt-get -y update
RUN apt-get -y install curl

RUN curl -sSL https://install.python-poetry.org | python3 -
RUN export PATH="/root/.local/bin:$PATH"

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1

WORKDIR /app

COPY pyproject.toml .

RUN /root/.local/bin/poetry install --no-interaction

FROM python:3.10.2-slim-buster AS runtime

WORKDIR app

ENV VIRTUAL_ENV="/app/.venv"
ENV PATH="/app/.venv/bin:$PATH"


COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY ./commons commons
COPY ./media media
COPY ./scripts scripts
COPY ./system_prompts system_prompts
COPY ./resources resources

COPY ./bot.py bot.py

EXPOSE 8080

CMD ["python3", "bot.py"]
