FROM python:3.12-slim AS base
WORKDIR /app
RUN chmod 1777 /tmp
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
COPY . .

FROM base AS development
ENV PYTHONUNBUFFERED 1
CMD ["uvicorn" , "main:app" , "--host" , "0.0.0.0" , "--port", "3000" , "--reload"]