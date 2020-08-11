FROM python:3.7-slim
WORKDIR /code
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV POETRY_VERSION=1.0.3
ENV LOGGING_LEVEL="DEBUG"
RUN apt-get update && apt-get install -y build-essential
RUN pip install "poetry==$POETRY_VERSION"
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-interaction --no-dev --no-ansi
RUN poetry run python -m spacy download en_core_web_md
EXPOSE 5000
COPY . .
RUN rm -rf tests
CMD ["poetry", "run", "flask", "run"]