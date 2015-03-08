#!/usr/bin/env python

from localization_utils import *
import sys
import argparse
import re


def parse_args():
    """ Parses the arguments given in the command line

    Returns:
        args: The configured arguments will be attributes of the returned object.
    """
    parser = argparse.ArgumentParser(description='Add the comments of duplicate keys to the strings file.')

    parser.add_argument("localization_file", help="The strings file from genstrings output.")

    parser.add_argument("genstrings_err", help="The stderr output of the genrstrings script.")

    parser.add_argument("--log_path", default="", help="The log file path")

    return parser.parse_args()


def add_genstrings_comments_to_file(localization_file, genstrings_err):
    """ Adds the comments produced by the genstrings script for duplicate keys.

    Args:
        localization_file (str): The path to the strings file.

    """

    errors_to_log = [line for line in genstrings_err.splitlines() if "used with multiple comments" not in line]

    if len(errors_to_log) > 0:
        logging.warning("genstrings warnings:\n%s", "\n".join(errors_to_log))

    loc_file = open_strings_file(localization_file, "a")

    regex_matches = re.findall(r'Warning: Key "(.*?)" used with multiple comments ("[^"]*" (& "[^"]*")+)',
                               genstrings_err)

    logging.info("Adding multiple comments from genstrings output")
    for regex_match in regex_matches:
        if len(regex_match) == 3:
            key = regex_match[0]
            comments = [comment.strip()[1:-1] for comment in regex_match[1].split("&")]

            logging.info("Found key with %d comments: %s", len(comments), key)

            loc_key = LocalizationEntry(comments, key, key)

            loc_file.write(unicode(loc_key))
            loc_file.write(u"\n")

    loc_file.close()


# The main method for simple command line run.
if __name__ == "__main__":

    args = parse_args()
    setup_logging(args)

    add_genstrings_comments_to_file(args.localization_file, args.genstrings_err)