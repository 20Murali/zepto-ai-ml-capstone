FROM python:3.12-slim

WORKDIR /app

COPY support_assistant/requirements.txt /app/support_assistant/requirements.txt

RUN pip install --no-cache-dir -r support_assistant/requirements.txt

COPY support_assistant /app/support_assistant

EXPOSE 8000

CMD ["uvicorn", "support_assistant.main:app", "--host", "0.0.0.0", "--port", "8000"]