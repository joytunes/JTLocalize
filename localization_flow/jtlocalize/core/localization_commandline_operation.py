from abc import abstractmethod, ABCMeta
import argparse


class LocalizationCommandLineOperation(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def name(self):
        """
        Return:
            str: The name of the operation, as will be used as an argument to the master script.
        """
        pass

    @abstractmethod
    def description(self):
        """
        Return:
            str: The one-liner description of the operation, as will be used as the help for it in the usage.
        """
        pass

    def configure_parser(self, parser):
        """
        Adds the necessary supported arguments to the argument parser.

        Args:
            parser (argparse.ArgumentParser): The parser to add arguments to.
        """
        parser.add_argument("--log_path", default="", help="The log file path")
        parser.add_argument("--verbose", help="Increase logging verbosity", action="store_true")

    @abstractmethod
    def run(self, parsed_args):
        """
        Will run the localization operation.

        Args:
            parsed_args: The result of parser.parse_args() after configured by the configure_parser method.
        """
        pass

    def run_with_standalone_parser(self):
        """
        Will run the operation as standalone with a new ArgumentParser
        """
        parser = argparse.ArgumentParser(description=self.description())
        self.configure_parser(parser)
        self.run(parser.parse_args())



