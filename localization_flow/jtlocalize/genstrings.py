#!/usr/bin/env python
import shutil
import subprocess
import sys

from jtlocalize.core.localization_utils import *
from jtlocalize.configuration.localization_configuration import *
from jtlocalize.core.add_genstrings_comments_to_file import add_genstrings_comments_to_file
from jtlocalize.core.create_localized_strings_from_ib_files import create_localized_strings_from_ib_files
from jtlocalize.core.handle_duplicates_in_localization import handle_duplications
from jtlocalize.core.merge_strings_files import merge_strings_files
from jtlocalize.core.localization_commandline_operation import LocalizationCommandLineOperation


LOCALIZATION_FILENAME = "Localizable.strings"
DEFAULT_TMP_DIRECTORY = "/tmp"
NO_COMMENT_PROVIDED_STRING = "No comment provided by engineer."


class GenerateStringsFileOperation(LocalizationCommandLineOperation):
    def name(self):
        return "generate"

    def description(self):
        return "Create the unified strings file."

    def configure_parser(self, parser):
        super(GenerateStringsFileOperation, self).configure_parser(parser)

        parser.add_argument("project_base_directory", help="The directory in which the app code lays")

        parser.add_argument("localization_bundle_path", default=LOCALIZATION_BUNDLE_PATH,
                            help="The path to the localizable bundle.")

        parser.add_argument("--tmp_directory", default=DEFAULT_TMP_DIRECTORY,
                            help="The default temporary directory to write files to in the process")

        parser.add_argument("--special_ui_components_prefix",
                            help="By default script will warn about ui components using JTL comments that aren't using "
                                 "the JT prefix (e.g. JTLabel). if you pass a value like XYZ here, it won't warn about "
                                 "components like XYZButton, XYZLabel, etc.")

        parser.add_argument("--exclude_dirs", nargs='+',
                            help="Directories to exclude when looking for source files to extract strings from")

        parser.add_argument("--include_strings_from_file",
                            help="Option to add additional strings from a file other the ones extracted with genstrings")

    def run(self, parsed_args):
        setup_logging(parsed_args)

        generate_strings(parsed_args.project_base_directory,
                         parsed_args.localization_bundle_path,
                         parsed_args.tmp_directory,
                         parsed_args.exclude_dirs,
                         parsed_args.include_strings_from_file,
                         parsed_args.special_ui_components_prefix)


def extract_source_files(base_dir, exclude_dirs):
    return find_files(base_dir, [".m", ".mm", ".swift"], exclude_dirs)


def generate_strings(project_base_dir, localization_bundle_path, tmp_directory, exclude_dirs, include_strings_file,
                     special_ui_components_prefix):
    """
    Calls the builtin 'genstrings' command with JTLocalizedString as the string to search for,
    and adds strings extracted from UI elements internationalized with 'JTL' + removes duplications.
    """

    localization_directory = os.path.join(localization_bundle_path, DEFAULT_LANGUAGE_DIRECTORY_NAME)
    if not os.path.exists(localization_directory):
        os.makedirs(localization_directory)

    localization_file = os.path.join(localization_directory, LOCALIZATION_FILENAME)

    # Creating the same directory tree structure in the tmp directory
    tmp_localization_directory = os.path.join(tmp_directory, DEFAULT_LANGUAGE_DIRECTORY_NAME)
    tmp_localization_file = os.path.join(tmp_localization_directory, LOCALIZATION_FILENAME)

    if os.path.isdir(tmp_localization_directory):
        shutil.rmtree(tmp_localization_directory)
    os.mkdir(tmp_localization_directory)

    logging.info("Running genstrings")

    source_files = extract_source_files(project_base_dir, exclude_dirs)

    genstrings_cmd = 'genstrings -s JTLocalizedString -o %s %s' % (tmp_localization_directory, " ".join(
            ['"%s"' % (source_file,) for source_file in source_files]))

    genstrings_process = subprocess.Popen(genstrings_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                          stdin=subprocess.PIPE, shell=True)

    genstrings_out, genstrings_err = genstrings_process.communicate()

    remove_empty_comments_from_file(tmp_localization_file)
    add_genstrings_comments_to_file(tmp_localization_file, genstrings_err)

    genstrings_rc = genstrings_process.returncode
    if genstrings_rc != 0:
        logging.fatal("genstrings returned %d, aborting run!", genstrings_rc)
        sys.exit(genstrings_rc)

    create_localized_strings_from_ib_files(project_base_dir, exclude_dirs, tmp_localization_file,
                                           special_ui_components_prefix)

    if include_strings_file:
        target = open_strings_file(tmp_localization_file, "a")
        source = open_strings_file(include_strings_file, "r")
        target.write(source.read())
        source.close()
        target.close()

    handle_duplications(tmp_localization_file)

    if os.path.isfile(localization_file):
        logging.info("Merging old localizable with new one...")
        merge_strings_files(localization_file, tmp_localization_file)
    else:
        logging.info("No Localizable yet, moving the created file...")
        shutil.move(tmp_localization_file, localization_file)


def remove_empty_comments_from_file(file_path):
    if not os.path.exists(file_path):
        return

    orig_file = open_strings_file(file_path, "r")
    filtered_path = file_path + ".filtered"
    filtered_file = open_strings_file(filtered_path, "w")
    for line in orig_file.readlines():
        if NO_COMMENT_PROVIDED_STRING in line:
            processed_line = u"/* */\n"
        else:
            processed_line = line

        filtered_file.write(processed_line)

    orig_file.close()
    filtered_file.close()
    os.remove(file_path)
    shutil.move(filtered_path, file_path)


# The main method for simple command line run.
if __name__ == "__main__":
    operation = GenerateStringsFileOperation()
    operation.run_with_standalone_parser()
