FROM python:3.14.7-slim@sha256:cad9a2c871761c413caa6fdd6441c783451e740a48aaeba60ae62a8b53525ef6

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN addgroup --system gengatewai && adduser --system --ingroup gengatewai gengatewai

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=gengatewai:gengatewai api ./api
COPY --chown=gengatewai:gengatewai experiments ./experiments

USER gengatewai

EXPOSE 8000

CMD ["uvicorn", "api.gengatewai.app:app", "--host", "0.0.0.0", "--port", "8000", "--no-server-header"]
