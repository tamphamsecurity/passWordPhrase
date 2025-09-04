import unittest
import os
import json
# Add parent directory to sys.path so we can import passWordPhrase
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from passWordPhrase import (LoadDictionaryFile)

class TestUnitPasswordPhrase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a minimal test dictionary file. 
        cls.test_dict_tmp_dir = './pythonTests/tmp'
        cls.test_dict_file_path = cls.test_dict_tmp_dir + '/dictionary.json'
        os.makedirs(os.path.dirname(cls.test_dict_file_path), exist_ok=True)
        with open(cls.test_dict_file_path, 'w') as f:
            json.dump({"apple": "fruit", "banana": "fruit", "cat": "animal", "dog": "animal"}, f)

    def setUp(self):
        self.generator = LoadDictionaryFile()
        self.generator.LoadFile()

    def test_random_characters_length(self):
        result = self.generator.RandomCharacters(count=8)
        self.assertEqual(len(result), 8)

    def test_password_word_count(self):
        result = self.generator.PassWord(count=3)
        # Should contain 3 words (separated by nothing if no separators)
        self.assertTrue(any(word in result for word in self.generator.WebstersDictionary.keys()))
        self.assertGreaterEqual(len(result), 3)

    def test_password_with_separators(self):
        result = self.generator.PassWord(count=3, insertNumbers=True, insertSpecial=True)
        # Should contain at least 2 separators
        separators = self.generator.AdditionalSeparatorCharacters(True, True, False, False)
        sep_count = sum(1 for c in result if c in separators)
        self.assertGreaterEqual(sep_count, 2)

    def test_additional_separator_characters(self):
        chars = self.generator.AdditionalSeparatorCharacters(True, True, True, True)
        self.assertTrue(any(c.isdigit() for c in chars))
        self.assertTrue(any(c in chars for c in '!@#$%^&*()'))
        self.assertTrue(any(c.isalpha() for c in chars))
        self.assertTrue(any(c.isupper() for c in chars))

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_dict_file_path):
            os.remove(cls.test_dict_file_path)
        if os.path.exists(cls.test_dict_tmp_dir):
            os.rmdir(cls.test_dict_tmp_dir)

if __name__ == '__main__':
    unittest.main()
