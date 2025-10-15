#!/bin/sh
set -ex

# Clone repo if missing
if [ ! -d "$APP_NAME" ]; then
    git clone "$GIT_REPOSITORY" "$APP_NAME"
fi

# Run setup only once
SETUP_MARKER=~/.setup_app_done
if [ ! -f "$SETUP_MARKER" ]; then
    python -u ~/scripts/setup_app.py
    touch "$SETUP_MARKER"
fi

# Run the repo folder (requires __main__.py)
exec python -u ~/$APP_NAME "$@"
