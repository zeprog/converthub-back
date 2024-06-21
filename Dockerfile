FROM python:3.10.7-slim as test-stage

WORKDIR /app

RUN apt-get update && apt-get install -y \
  libicu-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app

# Run tests
RUN pytest --maxfail=1 --disable-warnings -v

FROM python:3.10.7-slim as app

WORKDIR /app

RUN apt-get update && apt-get install -y \
  libicu-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app

CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]