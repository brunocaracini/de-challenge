# Use the specified Python version as the base image.
ARG PYTHON_VERSION=3.9.5
FROM python:${PYTHON_VERSION}-slim as base

# Set environment variables to configure Python behavior.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create a non-privileged user to run the application.
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/app" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Set the directory where the virtual environment will be created.
ENV VIRTUAL_ENV=/venv
RUN python -m venv $VIRTUAL_ENV

# Update PATH to include the virtual environment.
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Create necessary directories with correct permissions.
RUN mkdir -p /app/.cache/pypoetry/cache/repositories/PyPI/_http \
    && chown -R appuser:appuser /app /venv

# Install Poetry to manage Python dependencies.
# This step leverages Docker's caching for faster builds.
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install poetry

# Switch to the non-privileged user to run the application.
USER root

# Copy the source code and dependency configuration files into the container.
COPY ./de_challenge/pyproject.toml ./de_challenge/poetry.lock ./
COPY ./de_challenge/ .

# Install system-level dependencies (e.g., libraries) as needed.
RUN apt-get update && apt-get install -y gcc
RUN apt-get update && apt-get install -y libpq-dev

# Install Python dependencies within the virtual environment.
RUN poetry install --no-root

# Expose the port that the application listens on.
EXPOSE 8000

# Define the command to run the application using Uvicorn.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]