FROM python:3.12

ENV PYTHONUNBUFFERED=1

ARG WORKDIR=/wd
ARG USER=user

WORKDIR ${WORKDIR}

RUN useradd --system ${USER} && \
    chown --recursive ${USER} ${WORKDIR}

RUN apt update && apt upgrade --yes

RUN pip install poetry


COPY --chown=${USER} pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry config cache-dir /tmp/poetry-cache && \
    poetry install --no-interaction --no-ansi --no-root

RUN mkdir -p /var/cache/fontconfig && chmod -R 777 /var/cache/fontconfig
COPY --chown=${USER} run.sh /run.sh
RUN chmod +x /run.sh

COPY --chown=${USER} . .

USER ${USER}

EXPOSE 8000


CMD ["/run.sh"]
