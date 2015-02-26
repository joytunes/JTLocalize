import argparse
from core.localization_utils import extract_header_comment_key_value_tuples_from_file, open_strings_file
from jtlocalize.core.localization_commandline_operation import LocalizationCommandLineOperation

__author__ = 'lwager'


class WordCountOperation(LocalizationCommandLineOperation):

    def name(self):
        return "word_count"

    def description(self):
        return "Perform a word count on pending localization file."

    def configure_parser(self, parser):
        parser.add_argument("localizable_file", help="The file that requires translation.")

    def run(self, parsed_args):
        print word_count(parsed_args.localizable_file)


def word_count(f_name):

    f = open_strings_file(f_name, "r")

    count = 0
    for _header_comment, comments, key, value in extract_header_comment_key_value_tuples_from_file(f):
        count += len(key.split())
    return count

if __name__ == "__main__":
    operation = WordCountOperation()
    operation.run_with_standalone_parser()
