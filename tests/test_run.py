import unittest
import os
from text_compiler.run import process_file  # Import the process_file function

class TestFileCompiler(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up test files
        with open('test1.txt', 'w') as f:
            f.write("This is a test file.\n")
        with open('test2.txt', 'w') as f:
            f.write("@import(test1.txt)\nThis file imports test1.")
        with open('test3.txt', 'w') as f:
            f.write("@import(test2.txt)\nThis file imports test2.")
        # More setup can be done here for complex cases

    @classmethod
    def tearDownClass(cls):
        # Clean up test files
        os.remove('test1.txt')
        os.remove('test2.txt')
        os.remove('test3.txt')
        # More cleanup can be done here if needed

    def test_simple_import(self):
        content = process_file('test1.txt')
        self.assertEqual(content, "This is a test file.\n")

    def test_nested_import(self):
        content = process_file('test3.txt')
        expected = "This is a test file.\nThis file imports test1.\nThis file imports test2."
        self.assertEqual(content, expected)

    # You can add more tests to cover other cases like handling non-existent files

class TestRelativePathImports(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create directories
        os.makedirs('test_dir/sub_dir', exist_ok=True)

        # Create test files
        with open('test_dir/test_file.txt', 'w') as f:
            f.write("Content of test file.\n")

        with open('test_dir/sub_dir/test_import.txt', 'w') as f:
            f.write("@import(../test_file.txt)\nContent of import file.")

    @classmethod
    def tearDownClass(cls):
        # Remove test files and directories
        os.remove('test_dir/sub_dir/test_import.txt')
        os.remove('test_dir/test_file.txt')
        os.rmdir('test_dir/sub_dir')
        os.rmdir('test_dir')

    def test_relative_import(self):
        expected_content = "Content of test file.\nContent of import file."
        content = process_file('test_dir/sub_dir/test_import.txt')
        self.assertEqual(content, expected_content)

class TestNonCircularImports(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create test files
        with open('fileC.txt', 'w') as f:
            f.write("Content of file C.\n")

        with open('fileB.txt', 'w') as f:
            f.write("@import(fileC.txt)\nContent of file B.\n")

        with open('fileA.txt', 'w') as f:
            f.write("@import(fileB.txt)\n@import(fileC.txt)\nContent of file A.\n")

    @classmethod
    def tearDownClass(cls):
        # Remove test files
        os.remove('fileC.txt')
        os.remove('fileB.txt')
        os.remove('fileA.txt')

    def test_non_circular_imports(self):
        expected_content = "Content of file C.\nContent of file B.\nContent of file C.\nContent of file A.\n"
        content = process_file('fileA.txt')
        self.assertEqual(content, expected_content)


class TestCircularImports(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create test files for circular import
        with open('fileA.txt', 'w') as f:
            f.write("@import(fileB.txt)\nContent of file A.\n")

        with open('fileB.txt', 'w') as f:
            f.write("@import(fileA.txt)\nContent of file B.\n")

    @classmethod
    def tearDownClass(cls):
        # Remove test files
        os.remove('fileA.txt')
        os.remove('fileB.txt')

    def test_circular_import(self):
        # with self.assertLogs(level='WARNING') as log:
        #     content = process_file('fileA.txt')
        #     self.assertIn("Circular import detected", log.output[0])

        content = process_file('fileA.txt')
        # Check content to ensure it doesn't contain repeated imports due to circular reference
        expected_content = "Content of file B.\nContent of file A.\n"
        self.assertEqual(content, expected_content)

if __name__ == '__main__':
    unittest.main()
