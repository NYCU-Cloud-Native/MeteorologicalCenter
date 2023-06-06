FROM python:3.11-alpine3.18

WORKDIR /app

COPY ./apps/taipower .

RUN pip install -r requirements.txt

EXPOSE 50051

CMD ["python", "server.py"]