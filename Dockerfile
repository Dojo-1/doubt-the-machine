FROM python:3.15.0-slim@sha256:f5b92f2a669a4c347044f29367f31983280b648250ca94dea66f98c53bc87e58

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
