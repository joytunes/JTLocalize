#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from localization_utils import *

class Replacement:
    def __init__(self):
        pass

    def regex(self):
        pass


class StaticReplacement(Replacement):
    def __init__(self, static_val):
        Replacement.__init__(self)
        self.static_val = static_val.decode("utf8")

    def regex(self):
        return self.static_val


class WrapReplacement(Replacement):
    def __init__(self, wrapping_prefix):
        Replacement.__init__(self)
        self.wrapping_prefix = wrapping_prefix.decode("utf8")

    def regex(self):
        return u"%s(\\1)" % self.wrapping_prefix


PRESET_REPLACEMENTS = {"chicken" : StaticReplacement("Chicken"),
                       "chinese" : StaticReplacement("鸡鸡鸡"),
                       "localized" : WrapReplacement("LOCALIZED")}

DEFAULT_REPLACEMENT = PRESET_REPLACEMENTS["chicken"]


def replace_english_values(filename, replacement):
    f = open_strings_file(filename, "r+")
    compiled = re.compile('= "(.*?)";', re.MULTILINE | re.DOTALL)
    subbed = compiled.sub(u'= "%s";' % replacement.regex(), f.read())
    f.seek(0)
    f.write(subbed)
    f.truncate()
    f.close()


def usage():
    print >> sys.stderr, "Usage: %s <file_path> <%s|-static (static_text)|-wrap (wrapping_text)>" % \
                         (sys.argv[0], "|".join(PRESET_REPLACEMENTS.keys()))


def unlocalize(filename, args):
    try:
        if filename is None:
            usage()
            return
        replacement_type = args[0]
        if replacement_type in PRESET_REPLACEMENTS:
            replace_english_values(filename, PRESET_REPLACEMENTS[replacement_type])

        elif replacement_type == "-static":
            replace_english_values(filename, StaticReplacement(args[1]))

        elif replacement_type == "-wrap":
            replace_english_values(filename, WrapReplacement(args[1]))

        else:
            usage()
    except IndexError:
        usage()


if __name__ == "__main__":
    try:
        unlocalize(sys.argv[1], sys.argv[2:])
    except IndexError:
        usage()

