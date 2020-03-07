import getopt
import sys
import yaml
from typing import Dict, Any


def intro(command_title: str, help_text: str, args: list, argv: list) -> Dict[str, Any]:
    """
    Generic function to parse arguments and display help. Also takes care of verbosity level.

    :param command_title: Title of the command
    :param help_text:     Text to print when `-h` is supplied
    :param args:          All long args
    :param argv:          Args given to the CLI command itself

    :return: with all given options and arguments
    """
    print(command_title)
    print("----------")
    print("")

    try:
        opts, args = getopt.getopt(argv, "h:v", args)
    except getopt.GetoptError as error:
        print(error)
        print("")
        print(help_text)
        print("")
        sys.exit(2)

    if len(opts) == 0 and len(args) == 0:
        print(help_text)
        print("")
        sys.exit()

    verbosity = len([opt for opt in opts if opt[0] == "-v"])
    if verbosity > 3:
        verbosity = 3

    input_args = dict()
    input_args["verbosity"] = verbosity

    for opt, arg in opts:
        if opt == "-h":
            print(help_text)
            print("")
            sys.exit()
        if opt != "-v":
            input_args[opt.replace("--", "")] = arg

    bin_print(verbosity, 3, "Input args:", input_args)

    return input_args


def bin_print(verbosity: int, required_verbosity: int, *args) -> None:
    """
    Prefixed print for debugging

    :param verbosity:          Verbosity level given by user input
    :param required_verbosity: Verbosity level at which the output actually happens
    :param args:               Other arguments, similar to print(...)

    :return: None
    """
    if verbosity >= required_verbosity:
        prefix = "  [INFO]  "
        if required_verbosity == 2:
            prefix = "  [DEBUG] "
        if required_verbosity == 3:
            prefix = "  [TRACE] "

        print(prefix, *args, flush=True)


def load_config(path: str) -> Dict[str, Any]:
    """
    Loads the bin configuration from yaml file

    :param path: Path to config file

    :return: The configuration
    """
    with open(path) as file:
        return yaml.load(file, Loader=yaml.FullLoader)
