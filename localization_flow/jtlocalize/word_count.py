import argparse
from core.localization_utils import extract_header_comment_key_value_tuples_from_file, open_strings_file

__author__ = 'lwager'

def parse_args():
    """ Parses the arguments given in the command line

    Returns:
        args: The configured arguments will be attributes of the returned object.
    """
    parser = argparse.ArgumentParser(
        description='Perform a word count on pending localization file.')

    parser.add_argument("localizable_file", help="The file that requires translation.")

    return parser.parse_args()

def word_count(f_name):

    f = open_strings_file(f_name, "r")

    count = 0
    for _header_comment, comments, key, value in extract_header_comment_key_value_tuples_from_file(f):
        count += len(key.split())
    return count

if __name__ == "__main__":
    args = parse_args()
    print word_count(args.localizable_file)
