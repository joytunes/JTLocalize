#!/usr/bin/env python


import unittest
import shutil
from jtlocalize.core.merge_strings_files import *
from jtlocalize.core.localization_utils import *

OLD_LOCALIZABLE_FILE_PATH = os.path.join(os.path.dirname(__file__), "resources/Localizable.old.strings")
NEW_LOCALIZABLE_FILE_PATH = os.path.join(os.path.dirname(__file__), "resources/app_localization_strings_output.strings")
MERGED_FILE_PATH = "/tmp/Localizable.merged.strings"


class MergeLocalizableTest(unittest.TestCase):
    """
    Test for the merge localizable script
    """

    def setUp(self):
        print "Starting test.."

    def tearDown(self):
        os.remove(MERGED_FILE_PATH)

    def test_merge(self):

        old_localizable_file_keys_to_objects = generate_localization_key_to_entry_dictionary_from_file(OLD_LOCALIZABLE_FILE_PATH)
        new_localizable_file_keys_to_objects = generate_localization_key_to_entry_dictionary_from_file(NEW_LOCALIZABLE_FILE_PATH)

        shutil.copyfile(OLD_LOCALIZABLE_FILE_PATH, MERGED_FILE_PATH)
        merge_strings_files(MERGED_FILE_PATH, NEW_LOCALIZABLE_FILE_PATH)

        f = open_strings_file(MERGED_FILE_PATH, "r")

        for comments, key, value in extract_comment_key_value_tuples_from_file(f):
            if key in old_localizable_file_keys_to_objects:
                self.assertEqual(value, old_localizable_file_keys_to_objects[key].value)
                if key in new_localizable_file_keys_to_objects:
                    self.assertItemsEqual(comments, new_localizable_file_keys_to_objects[key].comments)
                    new_localizable_file_keys_to_objects.pop(key)
                else:
                    self.assertItemsEqual(comments, old_localizable_file_keys_to_objects[key].comments)
                old_localizable_file_keys_to_objects.pop(key)
            else:
                self.assertIn(key, new_localizable_file_keys_to_objects)
                self.assertEqual(value, new_localizable_file_keys_to_objects[key].value)
                self.assertListEqual(comments, new_localizable_file_keys_to_objects[key].comments)
                new_localizable_file_keys_to_objects.pop(key)

        self.assertEqual(len(new_localizable_file_keys_to_objects), 0)

if __name__ == '__main__':
    unittest.main()
