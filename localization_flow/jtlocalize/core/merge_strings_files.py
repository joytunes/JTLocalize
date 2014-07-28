#!/usr/bin/env python

import argparse
from localization_utils import *


def parse_args():
    """ Parses the arguments given in the command line

    Returns:
        args: The configured arguments will be attributes of the returned object.
    """
    parser = argparse.ArgumentParser(description='Merge old strings file with new one.')

    parser.add_argument("old_strings_file", help="The old strings file (the values might have changed).")

    parser.add_argument("new_strings_file", help="The new strings file (produced by genstrings.sh.")

    parser.add_argument("--log_path", default="", help="The log file path")

    return parser.parse_args()


def merge_strings_files(old_strings_file, new_strings_file):
    """ Merges the old strings file with the new one.

    Args:
        old_strings_file (str): The path to the old strings file (previously produced, and possibly altered)
        new_strings_file (str): The path to the new strings file (newly produced).

    """
    old_localizable_dict = generate_localization_key_to_entry_dictionary_from_file(old_strings_file)
    output_file_elements = []

    f = open_strings_file(new_strings_file, "r+")

    for header_comment, comments, key, value in extract_header_comment_key_value_tuples_from_file(f):
        if len(header_comment) > 0:
            output_file_elements.append(Comment(header_comment))

        localize_value = value
        if key in old_localizable_dict:
            localize_value = old_localizable_dict[key].value

        output_file_elements.append(LocalizationEntry(comments, key, localize_value))

    f.close()

    write_file_elements_to_strings_file(old_strings_file, output_file_elements)


# The main method for simple command line run.
if __name__ == "__main__":

    args = parse_args()
    setup_logging(args)

    merge_strings_files(args.old_strings_file, args.new_strings_file)
