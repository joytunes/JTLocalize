#!/usr/bin/env python

import unittest
from jtlocalize.core.localization_diff import *
from jtlocalize.core.localization_merge_back import *
from jtlocalize.mock_translate import *

NEW_LOCALIZABLE_FILE_PATH = os.path.join(os.path.dirname(__file__), "resources/Localizable.new.strings")
OLD_TRANSLATED_FILE_PATH = os.path.join(os.path.dirname(__file__), "resources/Localizable.translated.old.strings")
NEW_TRANSLATED_FILE_PATH = "/tmp/Localizable.translated.new.strings"
MERGED_FILE_PATH = "/tmp/Localizable.merged.strings"


class LocalizationDiffTest(unittest.TestCase):
    """
    The test is currently pretty stupid, just wanted to check a specific use case
    """

    def setUp(self):
        print "Starting test.."

    def tearDown(self):
        os.remove(MERGED_FILE_PATH)
        os.remove(NEW_TRANSLATED_FILE_PATH)

    def translate_pending_file(self):
        mock_translate(NEW_TRANSLATED_FILE_PATH, wrap="test")

    def assert_only_new_keys_in_pending_file(self):

        old_translated_file_keys_to_objects = generate_localization_key_to_entry_dictionary_from_file(OLD_TRANSLATED_FILE_PATH)
        localizable_values_to_objects = generate_localization_value_to_entry_dictionary_from_file(NEW_LOCALIZABLE_FILE_PATH)

        f = open_strings_file(NEW_TRANSLATED_FILE_PATH, "r")

        for header_comment, comments, key, value in extract_header_comment_key_value_tuples_from_file(f):
            localizable_key = localizable_values_to_objects[key]
            self.assertFalse(localizable_key in old_translated_file_keys_to_objects)

    def assert_localizable_value_translated(self):
        merged_file_dict = generate_localization_key_to_entry_dictionary_from_file(MERGED_FILE_PATH)

        f = open_strings_file(NEW_LOCALIZABLE_FILE_PATH, "r")

        for header_comment, comments, key, value in extract_header_comment_key_value_tuples_from_file(f):
            merged_value = merged_file_dict[key].value
            self.assertEqual(merged_value, "test(%s)" % value)

    def test_simple_flow(self):

        localization_diff(NEW_LOCALIZABLE_FILE_PATH, OLD_TRANSLATED_FILE_PATH, None, NEW_TRANSLATED_FILE_PATH)

        self.assert_only_new_keys_in_pending_file()

        self.translate_pending_file()

        localization_merge_back(NEW_LOCALIZABLE_FILE_PATH, OLD_TRANSLATED_FILE_PATH, NEW_TRANSLATED_FILE_PATH,
                                MERGED_FILE_PATH)

        self.assert_localizable_value_translated()


if __name__ == '__main__':
    unittest.main()

