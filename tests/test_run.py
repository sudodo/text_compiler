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

if __name__ == '__main__':
    unittest.main()