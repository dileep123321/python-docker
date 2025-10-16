# syntax=docker/dockerfile:1
ARG FROM_IMAGE=python:3.12-slim
FROM ${FROM_IMAGE}

ENV APP_NAME="python-docker" \
    GIT_REPOSITORY="https://github.com/dileep123321/python-docker.git" \
    GIT_BRANCH="" \
    PYTHONUNBUFFERED=1

ARG USERNAME=user

# Ensure git installed regardless of base image
RUN set -eux; \
    if command -v apt-get >/dev/null 2>&1; then \
        apt-get update -y && apt-get install -y git && rm -rf /var/lib/apt/lists/*; \
    elif command -v apk >/dev/null 2>&1; then \
        apk add --no-cache git bash; \
    elif command -v yum >/dev/null 2>&1; then \
        yum install -y git; \
    else \
        echo "No supported package manager found!" && exit 1; \
    fi

# Create user and working dir safely
RUN useradd -ms /bin/bash ${USERNAME} 2>/dev/null || adduser -D ${USERNAME}
RUN mkdir -p /home/${USERNAME}/scripts

WORKDIR /home/${USERNAME}

# Copy setup script
COPY scripts/setup_app.py ./scripts/setup_app.py

# Fix permissions (do as root for all images)
USER root
RUN chmod 755 /home/${USERNAME}/scripts/setup_app.py

USER ${USERNAME}
CMD ["python", "-u", "/home/user/scripts/setup_app.py"]
