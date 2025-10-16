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
        self.app_name = os.getenv("APP_NAME", "python-docker")
        self.git_repository = os.getenv("GIT_REPOSITORY")
        self.git_branch = os.getenv("GIT_BRANCH")

        if not self.git_repository:
            raise Exception("Environment variable GIT_REPOSITORY is required")

        self.base_dir = os.path.expanduser("~")
        self.first_run_file = os.path.join(self.base_dir, self.FIRST_RUN_FILENAME)
        self.app_dir = os.path.join(self.base_dir, self.app_name)
        self.requirements_file = os.path.join(self.app_dir, self.REQUIREMENTS_FILENAME)


def log(message):
    print(f"[{datetime.now().strftime('%y/%m/%d %H:%M:%S')}] {message}", flush=True)


def is_first_run(settings):
    return not os.path.isfile(settings.first_run_file)


def save_setup_done(settings):
    os.mknod(settings.first_run_file)
    log("Saved 'App installed' status")


def clear_output_dir(settings):
    with suppress(FileNotFoundError):
        os.rmdir(settings.app_dir)
        log("Cleared output directories")


def clone(settings):
    log("Cloning app through Git...")
    branch_args = ["--branch", settings.git_branch] if settings.git_branch else []
    try:
        subprocess.run(
            ["git", "clone", *branch_args, settings.git_repository, settings.app_dir],
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
    if os.path.isfile(settings.requirements_file):
        log("Installing requirements via pip...")
        result = subprocess.call(["pip", "install", "--user", "-r", settings.requirements_file])
        if result != 0:
            raise Exception("Pip install failed!")
        log("Requirements installed!")
    else:
        log("No requirements.txt found, skipping install.")


def run():
    try:
        settings = Settings()
        if is_first_run(settings):
            log("This is container first run, running app installing process...")
            clear_output_dir(settings)
            clone(settings)
            install_requirements(settings)
            save_setup_done(settings)
            log("Setup completed successfully!")
        else:
            log("App already installed")
    except Exception as ex:
        log(f"Error! {ex}")
        exit(1)


if __name__ == "__main__":
    run()
