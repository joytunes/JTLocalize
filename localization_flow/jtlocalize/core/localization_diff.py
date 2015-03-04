#!/usr/bin/env python

from localization_utils import *
import argparse

VALUE_PLACEHOLDER = "XXX"


def parse_args():
    """ Parses the arguments given in the command line

    Returns:
        args: The configured arguments will be attributes of the returned object.
    """
    parser = argparse.ArgumentParser(
        description='Perform a diff on the new localizable file, and the file we already translated.')

    parser.add_argument("input_localizable_file", help="The file that requires translation.")

    parser.add_argument("input_translated_file", help="The file that was already translated.")

    parser.add_argument("excluded_strings_file",
                        help="A file that contains all strings we want to exclude from diff.")

    parser.add_argument("output_translation_file", help="Output file to send for translation.")

    parser.add_argument("--log_path", default="", help="The log file path")

    return parser.parse_args()


def localization_diff(localizable_file, translated_file, excluded_strings_file, output_translation_file):
    """ Generates a strings file representing the strings that were yet to be translated.

    Args:
        localizable_file (str): The path to the localization strings file, meaning the file that represents the strings
            that require translation.
        translated_file (str): The path to the translated strings file, meaning the file containing the strings that
            were already translated.
        excluded_strings_file (str): The path to a file that contains all the strings we want to exclude from this and
            from future diffs.
        output_translation_file (str): The path to the output file, which will contain the strings the require
            translation, but are not in the already given translation file.
    """
    old_translated_file_dictionary = generate_localization_key_to_entry_dictionary_from_file(translated_file)
    if excluded_strings_file is not None and os.path.isfile(excluded_strings_file):
        excluded_file_dictionary = generate_localization_key_to_entry_dictionary_from_file(excluded_strings_file)
    else:
        excluded_file_dictionary = {}

    # The reason we keep a list of the keys, and not just pop is because values can repeat themselves.
    translated_list = old_translated_file_dictionary.keys()
    output_dictionary = {}
    output_file_elements = []
    f = open_strings_file(localizable_file, "r")

    output_file_elements.append(Comment(u"""
/**
 * This file contains all the strings that were extracted from our app and that need to be translated.
 * Each entry may or may not have a comment explaining context, and a "key" = "%s" equation.
 * To localize, you need to fill the right side of the equation with the translation of the left side.
 * Please keep special expressions such as '%%@' or '%%1$@' as is. Usually the comment will explain their context.
 */
""" % (VALUE_PLACEHOLDER,)))

    for _header_comment, comments, key, value in extract_header_comment_key_value_tuples_from_file(f):
        if key in translated_list or key in excluded_file_dictionary:
            if key in old_translated_file_dictionary:
                old_translated_file_dictionary.pop(key)
        elif value in output_dictionary:
            output_dictionary[value].add_comments(comments)
            output_file_elements.append(Comment(
                u"/* There was a value '%s' here but it was a duplicate of an older value and removed. */\n" % value))
        else:
            loc_obj = LocalizationEntry(comments, value, VALUE_PLACEHOLDER)
            output_dictionary[value] = loc_obj
            output_file_elements.append(loc_obj)

    for key, removed_trans in old_translated_file_dictionary.items():
        output_file_elements.append(Comment(u"""
/*
 * Entry removed from previous translation file:
 * %s
 * "%s" = "%s";
 */
""" % (", ".join(removed_trans.comments), removed_trans.key, removed_trans.value)))

    write_file_elements_to_strings_file(output_translation_file, output_file_elements)

# The main method for simple command line run.
if __name__ == "__main__":
    args = parse_args()
    setup_logging(args)

    localization_diff(args.input_localizable_file, args.input_translated_file, args.excluded_strings_file,
                      args.output_translation_file)
