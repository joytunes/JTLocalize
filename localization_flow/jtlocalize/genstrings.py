#!/usr/bin/env python

import shutil
import subprocess

from jtlocalize.core.localization_utils import *
from jtlocalize.configuration.localization_configuration import *
from jtlocalize.core.add_genstrings_comments_to_file import add_genstrings_comments_to_file
from jtlocalize.core.create_localized_strings_from_ib_files import create_localized_strings_from_ib_files
from jtlocalize.core.handle_duplicates_in_localization import handle_duplications
from jtlocalize.core.merge_strings_files import merge_strings_files
from jtlocalize.core.localization_commandline_operation import LocalizationCommandLineOperation


LOCALIZATION_FILENAME = "Localizable.strings"
DEFAULT_TMP_DIRECTORY = "/tmp"


class GenerateStringsFileOperation(LocalizationCommandLineOperation):
    def name(self):
        return "generate"

    def description(self):
        return "Create the unified strings file."

    def configure_parser(self, parser):
        parser.add_argument("project_base_directory", help="The directory in which the app code lays")

        parser.add_argument("localization_bundle_path", default=LOCALIZATION_BUNDLE_PATH,
                            help="The path to the localizable bundle.")

        parser.add_argument("--tmp_directory", default=DEFAULT_TMP_DIRECTORY,
                            help="The default temporary directory to write files to in the process")

        parser.add_argument("--log_path", default="", help="The log file path")

    def run(self, parsed_args):
        setup_logging(parsed_args)

        generate_strings(parsed_args.project_base_directory,
                         parsed_args.localization_bundle_path,
                         parsed_args.tmp_directory)


def generate_strings(project_base_dir, localization_bundle_path, tmp_directory):
    """
    Calls the builtin 'genstrings' command with JTLocalizedString as the string to search for,
    and adds strings extracted from UI elements internationalized with 'JTL' + removes duplications.
    """

    localization_directory = os.path.join(localization_bundle_path, DEFAULT_LANGUAGE_DIRECTORY_NAME)
    localization_file = os.path.join(localization_directory, LOCALIZATION_FILENAME)

    # Creating the same directory tree structure in the tmp directory
    tmp_localization_directory = os.path.join(tmp_directory, DEFAULT_LANGUAGE_DIRECTORY_NAME)
    tmp_localization_file = os.path.join(tmp_localization_directory, LOCALIZATION_FILENAME)

    if os.path.isdir(tmp_localization_directory):
        shutil.rmtree(tmp_localization_directory)
    os.mkdir(tmp_localization_directory)

    logging.info("Running genstrings")

    find_cmd = 'find %s ! -path "*matlab*" -name "*.m" -print' % project_base_dir

    find_process = subprocess.Popen(find_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    find_out, find_err = find_process.communicate()

    genstrings_cmd = 'xargs genstrings -s JTLocalizedString -o %s' % tmp_localization_directory

    genstrings_process = subprocess.Popen(genstrings_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                          stdin=subprocess.PIPE, shell=True)

    genstrings_out, genstrings_err = genstrings_process.communicate(find_out)

    add_genstrings_comments_to_file(tmp_localization_file, genstrings_err)

    create_localized_strings_from_ib_files(project_base_dir, tmp_localization_file)

    handle_duplications(tmp_localization_file)

    if os.path.isfile(localization_file):
        logging.info("Merging old localizable with new one...")
        merge_strings_files(localization_file, tmp_localization_file)
    else:
        logging.info("No Localizable yet, moving the created file...")
        shutil.move(tmp_localization_file, localization_file)

    logging.info("Moving others files in the temporary directory to the localization directory")

    copy_tmp_files_cmd = 'find %s -not -name %s -and -not -path %s -exec cp "{}" %s \ ' % (tmp_localization_directory,
                                                                                           LOCALIZATION_FILENAME,
                                                                                           tmp_localization_directory,
                                                                                           localization_directory)

    copy_tmp_files_process = subprocess.Popen(copy_tmp_files_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                              shell=True)

    copy_tmp_files_process.communicate()


# The main method for simple command line run.
if __name__ == "__main__":
    operation = GenerateStringsFileOperation()
    operation.run_with_standalone_parser()
