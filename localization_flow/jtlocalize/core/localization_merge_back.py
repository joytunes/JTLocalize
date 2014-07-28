#!/usr/bin/env python

from localization_utils import *
import argparse


def parse_args():
    """ Parses the arguments given in the command line

    Returns:
        args: The configured arguments will be attributes of the returned object.
    """
    parser = argparse.ArgumentParser(description='Merging the old translations and the new ones.')

    parser.add_argument("updated_localizable_file", help="The updated localization strings file (produced by genstrings.sh).")

    parser.add_argument("old_translated_file", help="The old translated strings file (with all previously translated strings).")

    parser.add_argument("new_translated_file", help="The new translated strings file (with the new translations).")

    parser.add_argument("merged_translated_file", help="The output file with the merged translations.")

    parser.add_argument("--log_path", default="", help="The log file path")

    return parser.parse_args()


def localization_merge_back(updated_localizable_file, old_translated_file, new_translated_file, merged_translated_file):
    """ Generates a file merging the old translations and the new ones.

    Args:
        updated_localizable_file (str): The path to the updated localization strings file, meaning the strings that
            require translation.
        old_translated_file (str): The path to the strings file containing the previously translated strings.
        new_translated_file (str): The path to the strings file containing the newly translated strings.
        merged_translated_file (str): The path to the output file with the merged translations.

    """
    output_file_elements = []
    old_translated_file_dict = generate_localization_key_to_entry_dictionary_from_file(old_translated_file)
    new_translated_file_dict = generate_localization_key_to_entry_dictionary_from_file(new_translated_file)

    f = open_strings_file(updated_localizable_file, "r")

    for header_comment, comments, key, value in extract_header_comment_key_value_tuples_from_file(f):
        translation_value = None
        if len(header_comment) > 0:
            output_file_elements.append(Comment(header_comment))

        if value in new_translated_file_dict:
            translation_value = new_translated_file_dict[value].value
        elif key in old_translated_file_dict:
            translation_value = old_translated_file_dict[key].value

        if translation_value is not None:
            output_file_elements.append(LocalizationEntry(comments, key, translation_value))

    f.close()

    write_file_elements_to_strings_file(merged_translated_file, output_file_elements)


# The main method for simple command line run.
if __name__ == "__main__":
    args = parse_args()
    setup_logging(args)

    localization_merge_back(args.updated_localizable_file, args.old_translated_file, args.new_translated_file,
                            args.merged_translated_file)