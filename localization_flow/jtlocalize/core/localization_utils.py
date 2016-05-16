#!/usr/bin/env python

import codecs
import os
import re
import operator
import logging

from localization_objects import *

# Regexp to parse and inspect strings in format JTL('Key Name', 'Key Comment')
JTL_REGEX = r"""JTL\(['"](.+?)['"],\s*['"](.+?)['"]\)"""

# Regexp to parse and inspect localization entries in the strings file.
HEADER_COMMENT_KEY_VALUE_TUPLES_REGEX = '((/\*\*\* *[^\n]*? *\*\*\*/\n*)*)(/\* *[^;]* *\*/\n*)"(.*?)" *= *"(.*?)";\s*\n'


def rewrite_localization_file_with_entry_modifications(localizable_file, output_file, modification_func):
    file_descriptor = open_strings_file(localizable_file, "r")

    output_file_elements = []

    for header_comment, comments, key, value in extract_header_comment_key_value_tuples_from_file(file_descriptor):

        if len(header_comment) > 0:
            output_file_elements.append(Comment(header_comment))

        output_file_elements.append(modification_func(LocalizationEntry(comments, key, value)))

    write_file_elements_to_strings_file(output_file, output_file_elements)


def open_strings_file(file_path, mode):
    """ Open the strings file

    Args:
        file_path (str): The path to the strings file
        mode (str): string representation of the mode in which to open the file (read, write, append, etc.)
    """
    return codecs.open(file_path, mode, "utf-16")


def write_file_elements_to_strings_file(file_path, file_elements):
    """ Write elements to the string file

    Args:
        file_path (str): The path to the strings file
        file_elements (list) : List of elements to write to the file.
    """
    f = open_strings_file(file_path, "w")
    for element in file_elements:
        f.write(unicode(element))
        f.write(u"\n")

    f.close()


def setup_logging(args=None):
    """ Setup logging module.

    Args:
        args (optional): The arguments returned by the argparse module.
    """
    logging_level = logging.WARNING
    if args is not None and args.verbose:
        logging_level = logging.INFO
    config = {"level": logging_level, "format": "jtlocalize:%(message)s"}

    if args is not None and args.log_path != "":
        config["filename"] = args.log_path

    logging.basicConfig(**config)


def __generate_localization_dictionary_from_file(file_path, localization_entry_attribute_name_for_key):
    """ Generates a dictionary mapping between keys (defined by the given attribute name) and localization entries.

    Args:
        file_path (str): The strings file path.
        localization_entry_attribute_name_for_key: The name of the attribute of LocalizationEntry to use as key.

    Returns:
        dict: A dictionary mapping between keys (defined by the given attribute name) and localization entries.
    """
    localization_dictionary = {}
    f = open_strings_file(file_path, "r+")
    header_comment_key_value_tuples = extract_header_comment_key_value_tuples_from_file(f)

    if len(header_comment_key_value_tuples) == 0:
        logging.warning("Couldn't find any strings in file '%s'. Check encoding and format." % file_path)

    for header_comment, comments, key, value in header_comment_key_value_tuples:
        localization_entry = LocalizationEntry(comments, key, value)
        localization_dictionary[
            localization_entry.__getattribute__(localization_entry_attribute_name_for_key)] = localization_entry
    f.close()
    return localization_dictionary


def generate_localization_key_to_entry_dictionary_from_file(file_path):
    """ Generates a dictionary mapping between localization keys and entries.

    Args:
        file_path (str): The strings file path.

    Returns:
        dict: A dictionary mapping between localization keys and entries.
    """
    return __generate_localization_dictionary_from_file(file_path, "key")


def generate_localization_value_to_entry_dictionary_from_file(file_path):
    """ Generates a dictionary mapping between localization values and entries.

    Args:
        file_path (str): The strings file path.

    Returns:
        dict: A dictionary mapping between localization values and entries.
    """
    return __generate_localization_dictionary_from_file(file_path, "value")


def extract_header_comment_key_value_tuples_from_file(file_descriptor):
    """ Extracts tuples representing comments and localization entries from strings file.

    Args:
        file_descriptor (file): The file to read the tuples from

    Returns:
        list : List of tuples representing the headers and localization entries.

    """
    file_data = file_descriptor.read()
    findall_result = re.findall(HEADER_COMMENT_KEY_VALUE_TUPLES_REGEX, file_data, re.MULTILINE | re.DOTALL)

    returned_list = []
    for header_comment, _ignored, raw_comments, key, value in findall_result:
        comments = re.findall("/\* (.*?) \*/", raw_comments)
        if len(comments) == 0:
            comments = [u""]
        returned_list.append((header_comment, comments, key, value))

    return returned_list


def extract_jtl_string_pairs_from_text_file(results_dict, file_path):
    """ Extracts all string pairs matching the JTL pattern from given text file.

    This can be used as an "extract_func" argument in the extract_string_pairs_in_directory method.

    Args:
        results_dict (dict): The dict to add the the string pairs to.
        file_path (str): The path of the file from which to extract the string pairs.

    """
    result_pairs = re.findall(JTL_REGEX, open(file_path).read())
    for result_key, result_comment in result_pairs:
        results_dict[result_key] = result_comment
    return results_dict


def extract_string_pairs_in_directory(directory_path, extract_func, filter_func):
    """ Retrieves all string pairs in the directory

    Args:
        directory_path (str): The path of the directory containing the file to extract string pairs from.
        extract_func (function): Function for extracting the localization keys and comments from the files.
            The extract function receives 2 parameters:
            - dict that the keys (a key in the dict) and comments (a value in the dict) are added to.
            - str representing file path

        filter_func (function): Function for filtering files in the directory.
            The filter function receives the file name and returns a bool representing the filter result.
            True if the file name passed the filter, False otherwise.

    Returns:
        dict: A mapping between string pairs first value (probably the key), and the second value (probably the comment).
    """
    result = {}
    for root, dirnames, filenames in os.walk(directory_path):
        for file_name in filenames:
            if filter_func(file_name):
                file_path = os.path.join(root, file_name)
                try:
                    extract_func(result, file_path)
                except Exception as e:
                    print "Error in file " + file_name
                    print e
    return result


def write_entry_to_file(file_descriptor, entry_comment, entry_key):
    """ Writes a localization entry to the file

    Args:
        file_descriptor (file, instance): The file to write the entry to.
        entry_comment (str): The entry's comment.
        entry_key (str): The entry's key.
    """
    escaped_key = re.sub(r'([^\\])"', '\\1\\"', entry_key)
    file_descriptor.write(u'/* %s */\n' % entry_comment)
    file_descriptor.write(u'"%s" = "%s";\n' % (escaped_key, escaped_key))


def write_section_header_to_file(file_descriptor, section_name):
    """ Writes a section header to the file

    Args:
        file_descriptor (file, instance): The file to writes the section header to.
        section_name (str): The name of the section.
    """
    file_descriptor.write('/*** %s ***/\n' % section_name)


def append_dictionary_to_file(localization_key_to_comment, file_path, section_name):
    """ Appends dictionary of localization keys and comments to a file

    Args:
        localization_key_to_comment (dict): A mapping between localization keys and comments.
        file_path (str): The path of the file to append to.
        section_name (str): The name of the section.

    """
    output_file = open_strings_file(file_path, "a")
    write_section_header_to_file(output_file, section_name)
    for entry_key, entry_comment in sorted(localization_key_to_comment.iteritems(), key=operator.itemgetter(1)):
        output_file.write(u'\n')
        write_entry_to_file(output_file, entry_comment, entry_key)
    output_file.close()


def write_dict_to_new_file(file_name, localization_key_to_comment):
    """ Writes dictionary of localization keys and comments to a file.

    Args:
        localization_key_to_comment (dict): A mapping between localization keys and comments.
        file_name (str): The path of the file to append to.

    """
    output_file_descriptor = open_strings_file(file_name, "w")
    for entry_key, entry_comment in sorted(localization_key_to_comment.iteritems(), key=operator.itemgetter(1)):
        write_entry_to_file(output_file_descriptor, entry_comment, entry_key)
        output_file_descriptor.write(u'\n')
    output_file_descriptor.close()


def find_files(base_dir, extensions, exclude_dirs=list()):
    """ Find all files matching the given extensions.

    Args:
        base_dir (str): Path of base directory to search in.
        extensions (list): A list of file extensions to search for.
        exclude_dirs (list): A list of directories to exclude from search.

    Returns:
        list of paths that match the search
    """
    result = []
    for root, dir_names, file_names in os.walk(base_dir):
        for filename in file_names:
            candidate = os.path.join(root, filename)
            if should_include_file_in_search(candidate, extensions, exclude_dirs):
                result.append(candidate)
    return result


def should_include_file_in_search(file_name, extensions, exclude_dirs):
    """ Whether or not a filename matches a search criteria according to arguments.

    Args:
        file_name (str): A file path to check.
        extensions (list): A list of file extensions file should match.
        exclude_dirs (list): A list of directories to exclude from search.

    Returns:
        A boolean of whether or not file matches search criteria.

    """
    return (exclude_dirs is None or not any(file_name.startswith(d) for d in exclude_dirs)) and \
        any(file_name.endswith(e) for e in extensions)
