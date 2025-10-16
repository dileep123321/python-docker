# syntax=docker/dockerfile:1
ARG FROM_IMAGE=python:3.12-slim
FROM ${FROM_IMAGE}

# Environment setup
ENV APP_NAME="python-docker" \
    GIT_REPOSITORY="https://github.com/dileep123321/python-docker.git" \
    GIT_BRANCH="" \
    PYTHONUNBUFFERED=1

# Add dependencies
RUN apt-get update -y && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Add non-root user
ARG USERNAME=user
RUN useradd -ms /bin/bash ${USERNAME}

USER ${USERNAME}
WORKDIR /home/${USERNAME}

# Copy the setup script
COPY scripts/setup_app.py /home/${USERNAME}/scripts/setup_app.py
RUN chmod +x /home/${USERNAME}/scripts/setup_app.py

# Default command
CMD ["python", "-u", "/home/user/scripts/setup_app.py"]
