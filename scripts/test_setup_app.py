import os
import unittest
from unittest.mock import patch, MagicMock
import setup_app


class TestSetupApp(unittest.TestCase):

    def setUp(self):
        """Setup common environment variables for tests"""
        self.env = {
            "APP_NAME": "MyApp",
            "GIT_REPOSITORY": "https://github.com/example/repo.git",
            "GIT_BRANCH": "main"
        }

    @patch.dict(os.environ, {}, clear=True)
    def test_missing_environment_variable(self):
        """Should raise an exception if environment variable is missing"""
        with self.assertRaises(Exception) as context:
            setup_app.Settings()
        self.assertIn("Environment variable", str(context.exception))

    @patch.dict(os.environ, {
        "APP_NAME": "MyApp",
        "GIT_REPOSITORY": "https://github.com/example/repo.git"
    })
    def test_settings_initialization(self):
        """Settings should correctly initialize attributes"""
        settings = setup_app.Settings()
        self.assertTrue(settings.app_dir.endswith("MyApp"))
        self.assertIn("repo.git", settings.git_repository)
        self.assertIn("MyApp", settings.app_name)

    @patch("os.path.isfile", return_value=False)
    def test_is_first_run_true(self, mock_isfile):
        settings = MagicMock()
        self.assertTrue(setup_app.is_first_run(settings))

    @patch("os.path.isfile", return_value=True)
    def test_is_first_run_false(self, mock_isfile):
        settings = MagicMock()
        self.assertFalse(setup_app.is_first_run(settings))

    @patch("os.mknod")
    def test_save_setup_done(self, mock_mknod):
        settings = MagicMock(first_run_file="file.flag")
        setup_app.save_setup_done(settings)
        mock_mknod.assert_called_once_with("file.flag")

    @patch("os.rmdir")
    def test_clear_output_dir(self, mock_rmdir):
        settings = MagicMock(app_dir="/fake/path")
        setup_app.clear_output_dir(settings)
        mock_rmdir.assert_called_once_with("/fake/path")

    @patch("subprocess.call", return_value=0)
    def test_clone_success(self, mock_subprocess):
        settings = MagicMock(
            git_repository="https://github.com/example/repo.git",
            app_dir="/fake/app",
            git_branch="main"
        )
        setup_app.clone(settings)
        mock_subprocess.assert_called()

    @patch("subprocess.call", return_value=1)
    def test_clone_failure(self, mock_subprocess):
        settings = MagicMock(
            git_repository="https://github.com/example/repo.git",
            app_dir="/fake/app"
        )
        with self.assertRaises(Exception):
            setup_app.clone(settings)

    @patch("os.path.isfile", return_value=True)
    @patch("subprocess.call", return_value=0)
    def test_install_requirements_success(self, mock_subprocess, mock_isfile):
        settings = MagicMock(requirements_file="requirements.txt")
        setup_app.install_requirements(settings)
        mock_subprocess.assert_called()

    @patch("os.path.isfile", return_value=True)
    @patch("subprocess.call", return_value=1)
    def test_install_requirements_failure(self, mock_subprocess, mock_isfile):
        settings = MagicMock(requirements_file="requirements.txt")
        with self.assertRaises(Exception):
            setup_app.install_requirements(settings)

    @patch("os.path.isfile", return_value=False)
    def test_install_requirements_no_file(self, mock_isfile):
        settings = MagicMock(requirements_file="missing.txt")
        setup_app.install_requirements(settings)
        mock_isfile.assert_called_once()


if __name__ == "__main__":
    unittest.main()
