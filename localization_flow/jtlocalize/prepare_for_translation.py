#!/usr/bin/env python

import shutil

from jtlocalize.core.localization_commandline_operation import LocalizationCommandLineOperation
from jtlocalize.core.localization_diff import localization_diff
from jtlocalize.core.localization_utils import *
from jtlocalize.configuration.localization_configuration import *


class PrepareForTranslationOperation(LocalizationCommandLineOperation):

    def name(self):
        return "prepare_diff"

    def description(self):
        return "Prepare the localization bundle for translation with only the necessary diff."

    def configure_parser(self, parser):
        super(PrepareForTranslationOperation, self).configure_parser(parser)
        
        parser.add_argument("localization_bundle_path", default=LOCALIZATION_BUNDLE_PATH,
                            help="The path to the localizable bundle.")

    def run(self, parsed_args):
        setup_logging(parsed_args)

        prepare_for_translation(parsed_args.localization_bundle_path)


def prepare_for_translation(localization_bundle_path):
    """ Prepares the localization bundle for translation.

    This means, after creating the strings files using genstrings.sh, this will produce '.pending' files, that contain
    the files that are yet to be translated.

    Args:
        localization_bundle_path (str): The path to the localization bundle.

    """

    logging.info("Preparing for translation..")

    for strings_file in os.listdir(os.path.join(localization_bundle_path, DEFAULT_LANGUAGE_DIRECTORY_NAME)):
        if not strings_file.endswith(".strings"):
            continue

        strings_path = os.path.join(localization_bundle_path, DEFAULT_LANGUAGE_DIRECTORY_NAME, strings_file)
        for lang_dir in os.listdir(localization_bundle_path):
            if lang_dir == DEFAULT_LANGUAGE_DIRECTORY_NAME or lang_dir.startswith("."):
                continue

            dest_strings_path = os.path.join(localization_bundle_path, lang_dir, strings_file)
            pending_path = dest_strings_path + ".pending"
            excluded_path = dest_strings_path + ".excluded"
            if not os.path.exists(dest_strings_path):
                open_strings_file(dest_strings_path, "a").close()

            logging.info("Preparing diff for %s in %s", lang_dir, pending_path)
            localization_diff(strings_path, dest_strings_path, excluded_path, pending_path)



# The main method for simple command line run.
if __name__ == "__main__":

    operation = PrepareForTranslationOperation()
    operation.run_with_standalone_parser()

