#!/usr/bin/env python


class Comment(object):
    """ Class representing a comment in the strings file.

    Attributes:
        comment (str): The actual comment content
    """
    def __init__(self, comment):
        """
        Args:
            comment (str): The actual comment content
        """
        self.comment = comment

    def __unicode__(self):
        """ String description of the comment, to be added to the file. """
        return u"%s\n" % self.comment.strip()


class LocalizationEntry(object):
    """ Class representing the localization details for a single string in the strings file.

    Attributes:
        comments (list of str): The comments regarding the localization entry, giving the translation context.
        key (str): The string for translation.
        value (str): The translated value.
    """
    def __init__(self, comments, key, value):
        """
        Args:
            comments (list of Comment objects): The comments regarding the localization entry, giving the translation context.
            key (str): The string for translation.
            value (str): The translated value.
        """
        self.comments = comments
        self.key = key
        self.value = value

    def __unicode__(self):
        """ String description of the entry, to be added to the file. """
        comments_str = u"\n".join([u"/* %s */" % comment for comment in self.comments])
        return u'%s\n"%s" = "%s";\n' % (comments_str, self.key, self.value)

    def add_comments(self, comments):
        """ Add comments to the localization entry

        Args:
            comments (list of str): The comments to be added to the localization entry.
        """
        for comment in comments:
            if comment not in self.comments and len(comment) > 0:
                self.comments.append(comment)
            if len(self.comments[0]) == 0:
                self.comments.pop(0)
