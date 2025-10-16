# syntax=docker/dockerfile:1
ARG FROM_IMAGE=python:3.12-slim
FROM ${FROM_IMAGE}

# Common environment variables
ENV APP_NAME="python-docker" \
    GIT_REPOSITORY="https://github.com/dileep123321/python-docker.git" \
    GIT_BRANCH="" \
    PYTHONUNBUFFERED=1

ARG USERNAME=user

# Conditional dependency install (apt or apk)
RUN set -eux; \
    if command -v apt-get >/dev/null; then \
        apt-get update -y && apt-get install -y git && rm -rf /var/lib/apt/lists/*; \
    elif command -v apk >/dev/null; then \
        apk add --no-cache git; \
    else \
        echo "No supported package manager found!"; exit 1; \
    fi

# Create user and directories safely
RUN useradd -ms /bin/bash ${USERNAME} 2>/dev/null || adduser -D ${USERNAME}
RUN mkdir -p /home/${USERNAME}/scripts

USER ${USERNAME}
WORKDIR /home/${USERNAME}

# Copy script and fix permissions
COPY scripts/setup_app.py /home/${USERNAME}/scripts/setup_app.py
RUN chmod +x /home/${USERNAME}/scripts/setup_app.py

CMD ["python", "-u", "/home/user/scripts/setup_app.py"]
