import os
import psutil
import time
import subprocess
import unittest


class TestsFunctional(unittest.TestCase):
    def test_01_regex_search_in_file(self):
        # Arrange
        file_path = os.path.join("/assets", "first.txt")
        pattern = r"[cm]ode"

        command = build_command(pattern, [file_path])

        expected_lines = [
            "Machine learning models require quality data.",
            "Version control tracks code changes efficiently.",
        ]

        # Act
        process_result = subprocess.run(command, capture_output=True, text=True, check=True)

        actual_lines = process_result.stdout.split("\n")
        actual_lines = [line for line in actual_lines if line != ""]

        # Assert
        self.assertEqual(expected_lines, actual_lines)

    def test_02_multiple_files(self):
        # Arrange
        file_paths = [os.path.join("/assets", "first.txt"), os.path.join("/assets", "second.txt")]
        pattern = r"sound"

        command = build_command(pattern, file_paths)

        expected_lines = [
            "The sound of thunder.",
            "The sound of distant laughter echoed through the empty streets.",
        ]

        # Act
        process_result = subprocess.run(command, capture_output=True, text=True, check=True)

        actual_lines = process_result.stdout.split("\n")
        actual_lines = [line for line in actual_lines if line != ""]

        # Assert
        self.assertEqual(expected_lines, actual_lines)

    def test_06_recursive_and_file_url_mutually_exclusive(self):
        # Arrange
        pattern = r"[cm]ode"

        command = build_command(pattern, [], is_recursive=True, is_from_url=True)

        # Act
        process_result = subprocess.run(command, capture_output=True, text=True, check=False)

        # Assert
        self.assertEqual(process_result.returncode, 2)


def build_command(
    pattern: str,
    files: list[str],
    is_line_number: bool = False,
    is_in_memory: bool = False,
    parallel: int = 0,
    is_recursive: bool = False,
    is_from_url: bool = False,
) -> list[str]:
    parts = [
        "python3",
        os.path.join(os.getcwd(), "mgrep.py"),
        pattern,
        *files,
    ]

    if is_line_number:
        parts.append("-n")

    if is_in_memory:
        parts.append("-m")

    if parallel != 0:
        parts.append("-p")
        parts.append(str(parallel))

    if is_recursive:
        parts.append("-r")

    if is_from_url:
        parts.append("-u")

    return parts


def get_children(pid: int) -> list[int]:
    parent = psutil.Process(pid)
    children = parent.children(recursive=False)

    return [child.pid for child in children]
