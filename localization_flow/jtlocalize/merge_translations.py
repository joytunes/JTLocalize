#!/usr/bin/env python

import glob

from jtlocalize.core.localization_merge_back import localization_merge_back
from jtlocalize.core.localization_utils import *
from jtlocalize.configuration.localization_configuration import *
from jtlocalize.core.localization_commandline_operation import LocalizationCommandLineOperation


TRANSLATED_SUFFIX = ".translated"


class MergeTranslationsOperation(LocalizationCommandLineOperation):

    def name(self):
        return "merge"

    def description(self):
        return "Merge translated files to the localization bundle."

    def configure_parser(self, parser):
        super(MergeTranslationsOperation, self).configure_parser(parser)
        parser.add_argument("localization_bundle_path", default=LOCALIZATION_BUNDLE_PATH,
                            help="The path to the localizable bundle.")

    def run(self, parsed_args):
        setup_logging(parsed_args)

        merge_translations(parsed_args.localization_bundle_path)


def merge_translations(localization_bundle_path):
    """ Merges the new translation with the old one.

    The translated files are saved as '.translated' file, and are merged with old translated file.

    Args:
        localization_bundle_path (str): The path to the localization bundle.

    """
    logging.info("Merging translations")
    for lang_dir in os.listdir(localization_bundle_path):
        if lang_dir == DEFAULT_LANGUAGE_DIRECTORY_NAME:
            continue
        for translated_path in glob.glob(os.path.join(localization_bundle_path, lang_dir, "*" + TRANSLATED_SUFFIX)):
            strings_path = translated_path[:-1 * len(TRANSLATED_SUFFIX)]
            localizable_path = os.path.join(localization_bundle_path,
                                            DEFAULT_LANGUAGE_DIRECTORY_NAME,
                                            os.path.basename(strings_path))

            localization_merge_back(localizable_path, strings_path, translated_path, strings_path)


# The main method for simple command line run.
if __name__ == "__main__":

    operation = MergeTranslationsOperation()
    operation.run_with_standalone_parser()
