#!/usr/bin/env python
import shutil

from localization_diff import localization_diff
from localization_utils import *
from localization_configuration import *
import os
import argparse


def parse_args():
    """ Parses the arguments given in the command line

    Returns:
        args: The configured arguments will be attributes of the returned object.
    """
    parser = argparse.ArgumentParser(description='Prepare the localization bundle for translation.')

    parser.add_argument("localization_bundle_path", default=LOCALIZATION_BUNDLE_PATH,
                        help="The path to the localizable bundle.")

    parser.add_argument("--log_path", default="", help="The log file path")

    return parser.parse_args()


def prepare_for_translation(localization_bundle_path):
    """ Prepares the localization bundle for translation.

    This means, after creating the strings files using genstrings.sh, this will produce '.pending' files, that contain
    the files that are yet to be translated.

    Args:
        localization_bundle_path (str): The path to the localization bundle.

    """

    logging.info('Start preparing "%s" for translation..' % localization_bundle_path)

    for strings_file in os.listdir(os.path.join(localization_bundle_path, DEFAULT_LANGUAGE_DIRECTORY_NAME)):
        if not strings_file.endswith(".strings"):
            continue

        strings_path = os.path.join(localization_bundle_path, DEFAULT_LANGUAGE_DIRECTORY_NAME, strings_file)
        for lang_dir in os.listdir(localization_bundle_path):
            if lang_dir == DEFAULT_LANGUAGE_DIRECTORY_NAME or lang_dir.startswith("."):
                continue

            dest_strings_path = os.path.join(localization_bundle_path, lang_dir, strings_file)
            pending_path = dest_strings_path + ".pending"
            if os.path.exists(dest_strings_path):
                logging.info("Found %s in %s, creating new diff in %s" % (strings_file, lang_dir, pending_path))
                localization_diff(strings_path, dest_strings_path, pending_path)
            else:
                logging.info("Didn't find %s in %s, creating new file in %s" % (strings_file, lang_dir, pending_path))
                shutil.copyfile(strings_path, pending_path)

    logging.info('Finished preparing "%s" for translation!' % localization_bundle_path)

# The main method for simple command line run.
if __name__ == "__main__":

    args = parse_args()
    setup_logging(args)

    prepare_for_translation(args.localization_bundle_path)
