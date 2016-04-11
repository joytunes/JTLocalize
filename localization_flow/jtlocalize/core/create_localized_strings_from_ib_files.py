#!/usr/bin/env python

import argparse
from xml.dom import minidom
from xml.sax.saxutils import unescape

from localization_utils import *

# The prefix to identify a comment for an internationalized comment.
JT_INTERNATIONALIZED_COMMENT_PREFIX = 'jtl_'

DEFAULT_UI_COMPONENTS_PREFIX = 'JT'


def write_string_pairs_from_ib_file_to_file(ib_files_directory, exclude_dirs, output_file,
                                            special_ui_components_prefix):
    logging.info('Creating localization string pairs from IB files')

    string_pairs = extract_string_pairs_in_dir(ib_files_directory, exclude_dirs, special_ui_components_prefix)
    output_file_desc = open_strings_file(output_file, "a")
    write_section_header_to_file(output_file_desc, 'IB Files Section')
    for entry_key, entry_comment in string_pairs:
        output_file_desc.write('\n')
        if entry_key is not None:
            write_entry_to_file(output_file_desc, entry_comment, entry_key)
        else:
            write_section_header_to_file(output_file_desc, entry_comment)

    output_file_desc.close()


def extract_string_pairs_in_dir(directory, exclude_dirs, special_ui_components_prefix):
    """ Extract string pairs in the given directory's xib/storyboard files.

    Args:
        directory (str): The path to the directory.
        exclude_dirs (str): A list of directories to exclude from extraction.
        special_ui_components_prefix (str):
            If not None, extraction will not warn about internationalized UI components with this class prefix.

    Returns:
        list: The extracted string pairs for all IB files in the directory.

    """
    result = []
    for ib_file_path in find_files(directory, [".xib", ".storyboard"], exclude_dirs):
        result += extract_string_pairs_in_ib_file(ib_file_path, special_ui_components_prefix)

    return result


def get_element_attribute_or_empty(element, attribute_name):
    """

    Args:
        element (element): The xib's element.
        attribute_name (str): The desired attribute's name.

    Returns:
        The attribute's value, or an empty str if none exists.

    """
    return element.attributes[attribute_name].value if element.hasAttribute(attribute_name) else ""


def extract_element_internationalized_comment(element):
    """ Extracts the xib element's comment, if the element has been internationalized.

    Args:
        element (element): The element from which to extract the comment.

    Returns:
        The element's internationalized comment, None if it does not exist, or hasn't been internationalized (according
        to the JTLocalize definitions).

    """
    element_entry_comment = get_element_attribute_or_empty(element, 'userLabel')
    if element_entry_comment == "":
        try:
            element_entry_comment = element.getElementsByTagName('string')[0].firstChild.nodeValue
        except Exception:
            element_entry_comment = ""
    if not element_entry_comment.lower().startswith(JT_INTERNATIONALIZED_COMMENT_PREFIX):
        return None
    else:
        return element_entry_comment[len(JT_INTERNATIONALIZED_COMMENT_PREFIX):]


def warn_if_element_not_of_class(element, class_suffix, special_ui_components_prefix):
    """ Log a warning if the element is not of the given type (indicating that it is not internationalized).

    Args:
        element: The xib's XML element.
        class_name: The type the element should be, but is missing.
        special_ui_components_prefix: If provided, will not warn about class with this prefix (default is only 'JT')
    """
    valid_class_names = ["%s%s" % (DEFAULT_UI_COMPONENTS_PREFIX, class_suffix)]
    if special_ui_components_prefix is not None:
        valid_class_names.append("%s%s" % (special_ui_components_prefix, class_suffix))

    if (not element.hasAttribute('customClass')) or element.attributes['customClass'].value not in valid_class_names:
        logging.warn("WARNING: %s is internationalized but isn't one of %s",
                     extract_element_internationalized_comment(element), valid_class_names)


def add_string_pairs_from_attributed_ui_element(results, ui_element, comment_prefix):
    """ Adds string pairs from a UI element with attributed text

    Args:
        results (list): The list to add the results to.
        attributed_element (element): The element from the xib that contains, to extract the fragments from.
        comment_prefix (str): The prefix of the comment to use for extracted string
                              (will be appended "Part X" suffices)

    Returns:
        bool: Whether or not an attributed string was found.
    """
    attributed_strings = ui_element.getElementsByTagName('attributedString')
    if attributed_strings.length == 0:
        return False

    attributed_element = attributed_strings[0]
    fragment_index = 1
    for fragment in attributed_element.getElementsByTagName('fragment'):
        # The fragment text is either as an attribute <fragment content="TEXT">
        # or a child in the format <string key='content'>TEXT</string>
        try:
            label_entry_key = fragment.attributes['content'].value
        except KeyError:
            label_entry_key = fragment.getElementsByTagName('string')[0].firstChild.nodeValue

        comment = "%s Part %d" % (comment_prefix, fragment_index)
        results.append((label_entry_key, comment))
        fragment_index += 1

    return fragment_index > 1


def add_string_pairs_from_label_element(xib_file, results, label, special_ui_components_prefix):
    """ Adds string pairs from a label element.

    Args:
        xib_file (str): Path to the xib file.
        results (list): The list to add the results to.
        label (element): The label element from the xib, to extract the string pairs from.
        special_ui_components_prefix (str):
            If not None, extraction will not warn about internationalized UI components with this class prefix.

    """
    label_entry_comment = extract_element_internationalized_comment(label)
    if label_entry_comment is None:
        return

    warn_if_element_not_of_class(label, 'Label', special_ui_components_prefix)

    if label.hasAttribute('usesAttributedText') and label.attributes['usesAttributedText'].value == 'YES':
        add_string_pairs_from_attributed_ui_element(results, label, label_entry_comment)
    else:
        try:
            label_entry_key = label.attributes['text'].value
        except KeyError:
            try:
                label_entry_key = label.getElementsByTagName('string')[0].firstChild.nodeValue
            except Exception:
                label_entry_key = 'N/A'
                logging.warn("%s: Missing text entry in %s", xib_file, label.toxml('UTF8'))
        results.append((label_entry_key, label_entry_comment))


def add_string_pairs_from_text_field_element(xib_file, results, text_field, special_ui_components_prefix):
    """ Adds string pairs from a textfield element.

    Args:
        xib_file (str): Path to the xib file.
        results (list): The list to add the results to.
        text_field(element): The textfield element from the xib, to extract the string pairs from.
        special_ui_components_prefix (str):
            If not None, extraction will not warn about internationalized UI components with this class prefix.

    """
    text_field_entry_comment = extract_element_internationalized_comment(text_field)
    if text_field_entry_comment is None:
        return

    if text_field.hasAttribute('usesAttributedText') and text_field.attributes['usesAttributedText'].value == 'YES':
        add_string_pairs_from_attributed_ui_element(results, text_field, text_field_entry_comment)
    else:
        try:
            text_field_entry_key = text_field.attributes['text'].value
            results.append((text_field_entry_key, text_field_entry_comment + ' default text value'))
        except KeyError:
            pass
    try:
        text_field_entry_key = text_field.attributes['placeholder'].value
        results.append((text_field_entry_key, text_field_entry_comment + ' placeholder text value'))
    except KeyError:
        pass
    warn_if_element_not_of_class(text_field, 'TextField', special_ui_components_prefix)


def add_string_pairs_from_text_view_element(xib_file, results, text_view, special_ui_components_prefix):
    """ Adds string pairs from a textview element.

    Args:
        xib_file (str): Path to the xib file.
        results (list): The list to add the results to.
        text_view(element): The textview element from the xib, to extract the string pairs from.
        special_ui_components_prefix(str): A custom prefix for internationalize component to allow (default is only JT)

    """
    text_view_entry_comment = extract_element_internationalized_comment(text_view)
    if text_view_entry_comment is None:
        return

    if text_view.hasAttribute('usesAttributedText') and text_view.attributes['usesAttributedText'].value == 'YES':
        add_string_pairs_from_attributed_ui_element(results, text_view, text_view_entry_comment)
    else:
        try:
            text_view_entry_key = text_view.attributes['text'].value
            results.append((text_view_entry_key, text_view_entry_comment + ' default text value'))
        except KeyError:
            pass
    warn_if_element_not_of_class(text_view, 'TextView', special_ui_components_prefix)


def add_string_pairs_from_button_element(xib_file, results, button, special_ui_components_prefix):
    """ Adds strings pairs from a button xib element.

    Args:
        xib_file (str): Path to the xib file.
        results (list): The list to add the results to.
        button(element): The button element from the xib, to extract the string pairs from.
        special_ui_components_prefix(str): A custom prefix for internationalize component to allow (default is only JT)

    """
    button_entry_comment = extract_element_internationalized_comment(button)
    if button_entry_comment is None:
        return

    for state in button.getElementsByTagName('state'):
        state_name = state.attributes['key'].value
        state_entry_comment = button_entry_comment + " - " + state_name + " state of button"
        if not add_string_pairs_from_attributed_ui_element(results, state, state_entry_comment):
            try:
                button_entry_key = state.attributes['title'].value
            except KeyError:
                try:
                    button_entry_key = state.getElementsByTagName('string')[0].firstChild.nodeValue
                except Exception:
                    continue

            results.append((button_entry_key, state_entry_comment))

    warn_if_element_not_of_class(button, 'Button', special_ui_components_prefix)


def extract_string_pairs_in_ib_file(file_path, special_ui_components_prefix):
    """ Extract the strings pairs (key and comment) from a xib file.

    Args:
        file_path (str): The path to the xib file.
        special_ui_components_prefix (str):
            If not None, extraction will not warn about internationalized UI components with this class prefix.

    Returns:
        list: List of tuples representing the string pairs.

    """
    try:
        results = []
        xmldoc = minidom.parse(file_path)

        element_name_to_add_func = {'label': add_string_pairs_from_label_element,
                                    'button': add_string_pairs_from_button_element,
                                    'textField': add_string_pairs_from_text_field_element,
                                    'textView': add_string_pairs_from_text_view_element}

        for element_name in element_name_to_add_func:
            add_func = element_name_to_add_func[element_name]
            elements = xmldoc.getElementsByTagName(element_name)
            for element in elements:
                add_func(file_path, results, element, special_ui_components_prefix)

        # Find strings of format JTL('Key Name', 'Key Comment') and add them to the results
        jtl_brackets_find_results = re.findall(JTL_REGEX, open(file_path).read())
        unescaped_jtl_brackets_find_results = [(unescape(x), unescape(y)) for (x, y) in jtl_brackets_find_results]
        results += unescaped_jtl_brackets_find_results

        if len(results) > 0:
            results = [(None, os.path.basename(file_path))] + results
        return results

    except Exception, e:
        logging.warn("ERROR: Error processing %s (%s: %s)", file_path, type(e), str(e))
        return []


def create_localized_strings_from_ib_files(ib_files_directory, exclude_dirs, output_file,
                                           special_ui_components_prefix=None):
    write_string_pairs_from_ib_file_to_file(ib_files_directory, exclude_dirs, output_file, special_ui_components_prefix)


def parse_args():
    """ Parses the arguments given in the command line

    Returns:
        args: The configured arguments will be attributes of the returned object.
    """
    parser = argparse.ArgumentParser(description='Extract the string for localization from IB files directory.')

    parser.add_argument("ib_files_directory", help="The directory containing the IB files.")

    parser.add_argument("output_file", help="The output file.")

    parser.add_argument("--special_ui_components_prefix", 
                        help="By default script will warn about ui components using JTL comments that aren't using the "
                             "JT prefix (e.g. JTLabel). if you pass a value like XYZ here, it won't warn about "
                             "components like XYZButton, XYZLabel, etc.")

    parser.add_argument("--exclude_dirs", nargs='+',
                        help="Directories to exclude when looking for IB files to extract strings from")

    parser.add_argument("--log_path", default="", help="The log file path")

    return parser.parse_args()

# The main method for simple command line run.
if __name__ == '__main__':

    args = parse_args()
    setup_logging(args)

    create_localized_strings_from_ib_files(args.ib_files_directory, args.exclude_dirs, args.output_file,
                                           args.special_ui_components_prefix)


