FROM python:3.15.2-slim@sha256:65a65fc7b30b06cb6df4930fd4650697cb23f4c2698ab81fc87e4b031bc36928

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
