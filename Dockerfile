# Base Python image
FROM python:3.12-slim

# Arguments
ARG APP_NAME=python-docker
ARG GIT_REPOSITORY=https://github.com/dileep123321/python-docker.git
ARG USERNAME=user

# Install git and upgrade pip as root
RUN apt-get update && apt-get install -y git && pip install --upgrade pip

# Create non-root user
RUN useradd -ms /bin/bash ${USERNAME}

# Copy scripts folder (contains setup_app.py and entrypoint.sh) as root
COPY scripts ./scripts
COPY scripts/entrypoint.sh /home/${USERNAME}/entrypoint.sh

# Make entrypoint executable as root
RUN chmod +x /home/${USERNAME}/entrypoint.sh

# Switch to non-root user after all root-level operations
USER ${USERNAME}
WORKDIR /home/${USERNAME}

# Environment variables
ENV APP_NAME=${APP_NAME} \
    GIT_REPOSITORY=${GIT_REPOSITORY}

# Entrypoint
ENTRYPOINT ["/home/user/entrypoint.sh"]
