#!/usr/bin/env python
# coding=utf-8

import unittest
from jtlocalize.core.localization_utils import *

TMP_FILE_PATH = "/tmp/Localizable.tmp.strings"

EXAMPLE_FILE_CONTENT = u"""
/**
 * Comment 1
 */

/*** Header comment 1 ***/

/* Entry Comment 1 */
"key1" = "value1";

/* Entry Comment 2 */
/* Duplicate - Entry Comment 2 */
"key2" = "value2";
"""


class LocalizationUtilsTest(unittest.TestCase):

    def setUp(self):
        self.file_for_tests = open_strings_file(TMP_FILE_PATH, "w")
        self.file_for_tests.write(EXAMPLE_FILE_CONTENT)
        self.file_for_tests.close()

    def tearDown(self):
        os.remove(TMP_FILE_PATH)

    def test_parse(self):
        result_dict = generate_localization_key_to_entry_dictionary_from_file(TMP_FILE_PATH)
        self.assertEquals(len(result_dict), 2, "Wrong number of keys")
        self.assertEquals(result_dict["key1"].value, "value1")
        self.assertEquals(result_dict["key1"].comments, ["Entry Comment 1"])
        self.assertEquals(result_dict["key2"].value, "value2")
        self.assertEquals(len(result_dict["key2"].comments), 2)


if __name__ == '__main__':
    unittest.main()

