#!/usr/bin/env python

from localization_utils import *
import argparse


def parse_args():
    """ Parses the arguments given in the command line

    Returns:
        args: The configured arguments will be attributes of the returned object.
    """
    parser = argparse.ArgumentParser(description='Omits duplications in a given localizable file.')

    parser.add_argument("localizable_file", help="The file that requires duplication handling.")

    parser.add_argument("--log_path", default="", help="The log file path")

    return parser.parse_args()


def handle_duplications(file_path):
    """ Omits the duplications in the strings files.
        Keys that appear more than once, will be joined to one appearance and the omit will be documented.

    Args:
        file_path (str): The path to the strings file.

    """
    logging.info('Handling duplications for "%s"', file_path)
    f = open_strings_file(file_path, "r+")
    comment_key_value_tuples = extract_comment_key_value_tuples_from_file(f)
    file_elements = []
    keys_to_objects = {}
    duplicates_found = []
    for comments, key, value in comment_key_value_tuples:
        if key in keys_to_objects:
            keys_to_objects[key].add_comments(comments)
            duplicates_found.append(key)
        else:
            loc_obj = LocalizationEntry(comments, key, value)
            keys_to_objects[key] = loc_obj
            file_elements.append(loc_obj)

    # Sort by key
    file_elements = sorted(file_elements, key=lambda x: x.key)

    f.seek(0)

    for element in file_elements:
        f.write(unicode(element))
        f.write(u"\n")

    f.truncate()
    f.close()

    logging.info("Omitted %d duplicates (%s)" % (len(duplicates_found), ",".join(duplicates_found)))
    logging.info('Finished handling duplications for "%s"', file_path)


# The main method for simple command line run.
if __name__ == "__main__":

    args = parse_args()
    setup_logging(args)
    handle_duplications(args.localizable_file)
