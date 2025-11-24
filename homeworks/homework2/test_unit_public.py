import os
import unittest

from unittest.mock import patch, MagicMock

from mgrep import search_in_file, run_multi_threaded, InvalidFileError, InvalidAmountOfWorkers


class TestSearchInFile(unittest.TestCase):
    def test_01_normal_search(self):
        # Arrange
        file_path = os.path.join("/assets", "second.txt")
        pattern = "hinting"

        expected_file = file_path
        expected_line = "Clouds gathered quickly, hinting at an approaching storm."
        expected_line_number = 5

        # Act
        actual_results = search_in_file(pattern, file_path, is_in_memory=True)

        # Assert
        self.assertEqual(len(actual_results), 1)
        actual_line, actual_file, actual_line_number = actual_results[0]
        self.assertEqual(actual_file, expected_file)
        self.assertEqual(actual_line, expected_line)
        self.assertEqual(actual_line_number, expected_line_number)

    def test_02_regex_search(self):
        # Arrange
        file_path = os.path.join("/assets", "first.txt")
        pattern = r"[cm]ode"

        expected_files = [file_path, file_path]
        expected_lines = [
            "Machine learning models require quality data.",
            "Version control tracks code changes efficiently.",
        ]
        expected_line_numbers = [8, 21]

        expected_results = [
            (line, file, line_number)
            for line, file, line_number in zip(expected_lines, expected_files, expected_line_numbers)
        ]
        # Act
        actual_results = search_in_file(pattern, file_path, is_in_memory=True)

        # Assert
        self.assertEqual(expected_results, actual_results)

    def test_05_file_not_found(self):
        # Arrange
        file_path = os.path.join("/assets", "non_existent_file.txt")
        pattern = "anything"

        # Act & Assert
        with self.assertRaises(InvalidFileError):
            search_in_file(pattern, file_path, is_in_memory=True)


class TestRunMultiThreaded(unittest.TestCase):
    def test_01_less_files_than_workers(self):
        # Arrange
        amount_of_files = 3
        file_paths = [os.path.join("/assets", "first.txt") for i in range(amount_of_files)]
        pattern = r"code"
        amount_of_workers = 5

        # Act

        with self.assertRaises(InvalidAmountOfWorkers):
            run_multi_threaded(
                pattern, file_paths, is_in_memory=True, is_line_numbers=False, amount_of_workers=amount_of_workers
            )

    def test_02_negative_workers(self):
        # Arrange
        amount_of_files = 3
        file_paths = [os.path.join("/assets", "first.txt") for i in range(amount_of_files)]
        pattern = r"code"
        amount_of_workers = -5

        # Act

        with self.assertRaises(InvalidAmountOfWorkers):
            run_multi_threaded(
                pattern, file_paths, is_in_memory=True, is_line_numbers=False, amount_of_workers=amount_of_workers
            )
