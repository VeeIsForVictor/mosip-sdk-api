FROM python:3.12-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ADD . /code

WORKDIR /code

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN uv sync --frozen

CMD ["uv", "run", "fastapi", "run", "app/main.py", "--port", "80"]