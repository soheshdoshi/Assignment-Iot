FROM python:3.8-slim

ENV PYTHONUNBUFFERED 1
EXPOSE 8000

ARG SECRET_KEY
ENV SECRET_KEY=$SECRET_KEY

WORKDIR /app

COPY ./src/project_files/requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./src/project_files .

CMD ["uvicorn", "--host", "0.0.0.0","--port","8000","main:app"]

