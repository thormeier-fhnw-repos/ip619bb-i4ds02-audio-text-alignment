from typing import Dict, Any
from lib.src.align.aligner.FilesAligner import FilesAligner
from lib.src.align.aligner.basic.BasicAlignerStrategy import BasicAlignerStrategy
from lib.src.align.aligner.random.RandomAlignerStrategy import RandomAlignerStrategy
from lib.src.align.aligner.google.GoogleFilesAligner import GoogleFilesAligner
# from lib.src.align.aligner.google.GoogleBiopythonAlignerStrategy import GoogleBiopythonAlignerStrategy
from lib.src.align.aligner.google.GoogleGlobalCharacterAlignerStrategy import GoogleGlobalCharacterAlignerStrategy
from lib.src.align.aligner.google.GoogleGlobalWordAlignerStrategy import GoogleGlobalWordAlignerStrategy
from lib.src.align.aligner.google.GoogleSemiglobalCharacterAlignerStrategy import GoogleSemiglobalCharacterAlignerStrategy
from lib.src.align.aligner.google.GoogleSemiglobalWordAlignerStrategy import GoogleSemiglobalWordAlignerStrategy
from lib.src.align.aligner.google.GoogleLocalCharacterAlignerStrategy import GoogleLocalCharacterAlignerStrategy
from lib.src.align.aligner.google.GoogleLocalWordAlignerStrategy import GoogleLocalWordAlignerStrategy


def _basic(alignment_parameters):
    return FilesAligner(BasicAlignerStrategy, "basic")


def _random(alignment_parameters):
    return FilesAligner(RandomAlignerStrategy, "random")


def _google_biopython(alignment_parameters):
    return None
    # return GoogleFilesAligner(GoogleBiopythonAlignerStrategy, alignment_parameters)


def _google_global_character(alignment_parameters):
    return GoogleFilesAligner(GoogleGlobalCharacterAlignerStrategy, alignment_parameters)


def _google_global_word(alignment_parameters):
    return GoogleFilesAligner(GoogleGlobalWordAlignerStrategy, alignment_parameters)


def _google_semiglobal_character(alignment_parameters):
    return GoogleFilesAligner(GoogleSemiglobalCharacterAlignerStrategy, alignment_parameters)


def _google_semiglobal_word(alignment_parameters):
    return GoogleFilesAligner(GoogleSemiglobalWordAlignerStrategy, alignment_parameters)


def _google_local_word(alignment_parameters):
    return GoogleFilesAligner(GoogleLocalCharacterAlignerStrategy, alignment_parameters)


def _google_local_character(alignment_parameters):
    return GoogleFilesAligner(GoogleLocalWordAlignerStrategy, alignment_parameters)


def get_aligner(alignment_parameters: Dict[str, Any]):
    """
    Generates a file aligner based on the given type.
    :param alignment_parameters: Dict of parameters loaded from a given YAML file. See README for full config.
    :return: FilesAligner, preconfigured
    """
    switcher = {
        "basic": _basic,
        "random": _random,
        "google_biopython": _google_biopython,
        "google_global_character": _google_global_character,
        "google_global_word": _google_global_word,
        "google_semiglobal_character": _google_semiglobal_character,
        "google_semiglobal_word": _google_semiglobal_word,
        "google_local_character": _google_local_character,
        "google_local_word": _google_local_word
    }

    generator = switcher.get(alignment_parameters["aligner_type"])

    return generator(alignment_parameters)