#!/usr/bin/env python3
"""
SETUP APP Script
"""

import os
import subprocess
from datetime import datetime
from contextlib import suppress


class Settings:
    FIRST_RUN_FILENAME = ".setup_app_done"
    REQUIREMENTS_FILENAME = "requirements.txt"

    def __init__(self):
        # Read env vars with defaults
        self.app_name = os.getenv("APP_NAME", "python-docker")
        self.git_repository = os.getenv("GIT_REPOSITORY")
        self.git_branch = os.getenv("GIT_BRANCH")  # optional

        if not self.git_repository:
            raise Exception("GIT_REPOSITORY environment variable is required")

        self.base_dir = os.path.expanduser("~")
        self.first_run_file = self.join_home(self.FIRST_RUN_FILENAME)
        self.app_dir = self.join_home(self.app_name)
        self.requirements_file = self.join_app(self.REQUIREMENTS_FILENAME)

    def join_home(self, path):
        return os.path.join(self.base_dir, path)

    def join_app(self, path):
        return os.path.join(self.app_dir, path)


def log(message):
    """Print log line with current datetime"""
    print(f"[{datetime.now().strftime('%y/%m/%d %H:%M:%S')}] {message}", flush=True)


def is_first_run(settings):
    """Return True if this is the first time the container runs"""
    return not os.path.isfile(settings.first_run_file)


def save_setup_done(settings):
    """Store a file to mark setup complete"""
    open(settings.first_run_file, "w").close()
    log("Saved 'App installed' status")


def clear_output_dir(settings):
    """Clear output directories"""
    with suppress(FileNotFoundError):
        if os.path.isdir(settings.app_dir):
            subprocess.run(["rm", "-rf", settings.app_dir], check=False)
            log("Cleared old app directory")


def clone(settings):
    """Clone the app through Git"""
    log("Cloning app through Git...")
    branch_settings = ["--branch", settings.git_branch] if settings.git_branch else []

    os.makedirs(os.path.dirname(settings.app_dir), exist_ok=True)

    try:
        subprocess.run(
            ["git", "clone", *branch_settings, settings.git_repository, settings.app_dir],
            check=True,
            capture_output=True,
            text=True
        )
        log("App cloned successfully!")
    except subprocess.CalledProcessError as e:
        log("Git clone failed!")
        log("stdout:\n" + e.stdout)
        log("stderr:\n" + e.stderr)
        raise Exception("Git Clone failed!") from e


def install_requirements(settings):
    """Install Python package requirements from requirements.txt"""
    if os.path.isfile(settings.requirements_file):
        log("Installing requirements via pip...")
        result = subprocess.call(["pip", "install", "--user", "-r", settings.requirements_file])
        if result != 0:
            raise Exception("Pip install failed!")
        log("Requirements installed!")
    else:
        log("No requirements.txt file found — skipping install")


def run():
    """Main run function"""
    try:
        settings = Settings()
        if is_first_run(settings):
            log("This is container first run, running setup...")
            clear_output_dir(settings)
            clone(settings)
            install_requirements(settings)
            save_setup_done(settings)
            log("✅ Setup completed successfully! App ready.")
        else:
            log("App already installed — skipping setup.")

    except Exception as ex:
        log(f"❌ Error during setup: {ex}")
        exit(1)


if __name__ == "__main__":
    run()
