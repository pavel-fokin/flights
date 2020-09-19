FROM python:3.8.5

ENV SERVICE_DIR="/app"

COPY requirements/prod.txt /
COPY requirements/dev.txt /

RUN pip install -r /prod.txt
RUN pip install -r /dev.txt

RUN groupadd -g 999 appuser && \
    useradd -u 999 -m -g appuser -s /bin/bash appuser && \
    mkdir -p ${SERVICE_DIR}

WORKDIR ${SERVICE_DIR}

COPY --chown=appuser:appuser . ${SERVICE_DIR}
RUN chown appuser:appuser ${SERVICE_DIR}

USER appuser

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["run"]
