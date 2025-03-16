FROM python:3.12-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ADD . /code

WORKDIR /code

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 git -y

RUN uv sync --frozen

ENV CONFIG_PATH="/run/secrets/config"

EXPOSE 80

CMD ["uv", "run", "fastapi", "run", "--port", "80"]