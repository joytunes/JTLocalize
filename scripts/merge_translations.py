#!/usr/bin/env python
import shutil

from localization_merge_back import localization_merge_back
from localization_utils import *
import os
import argparse
import glob
from localization_configuration import *

TRANSLATED_SUFFIX = ".translated"


def parse_args():
    """ Parses the arguments given in the command line

    Returns:
        args: The configured arguments will be attributes of the returned object.
    """
    parser = argparse.ArgumentParser(description='Merge translated files to the localization bundle.')

    parser.add_argument("localization_bundle_path", default=LOCALIZATION_BUNDLE_PATH,
                        help="The path to the localizable bundle.")

    parser.add_argument("--log_path", default="", help="The log file path")

    return parser.parse_args()


def merge_translations(localization_bundle_path):
    """ Merges the new translation with the old one.

    The translated files are saved as '.translated' file, and are merged with old translated file.

    Args:
        localization_bundle_path (str): The path to the localization bundle.

    """
    logging.info('Start merging translations for "%s"..' % localization_bundle_path)
    for lang_dir in os.listdir(localization_bundle_path):
        if lang_dir == DEFAULT_LANGUAGE_DIRECTORY_NAME:
            continue
        for translated_path in glob.glob(os.path.join(localization_bundle_path, lang_dir, "*" + TRANSLATED_SUFFIX)):
            strings_path = translated_path[:-1 * len(TRANSLATED_SUFFIX)]
            localizable_path = os.path.join(localization_bundle_path,
                                            DEFAULT_LANGUAGE_DIRECTORY_NAME,
                                            os.path.basename(strings_path))

            localization_merge_back(localizable_path, strings_path, translated_path, strings_path)
            os.remove(translated_path)

    logging.info('Finished merging translations for "%s"' % localization_bundle_path)

# The main method for simple command line run.
if __name__ == "__main__":

    args = parse_args()
    setup_logging(args)

    merge_translations(args.localization_bundle_path)