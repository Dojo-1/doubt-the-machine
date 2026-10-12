FROM python:3.14.8-slim@sha256:a2b82f3c48559aa0a8446d9af49826b6e2b2016f4cd2afabfe6013ec53729170

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
