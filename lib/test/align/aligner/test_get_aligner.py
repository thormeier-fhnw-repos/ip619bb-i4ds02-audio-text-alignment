import unittest
from typing import Dict, Any, Type
from lib.src.align.aligner.FilesAligner import FilesAligner
from lib.src.align.aligner.basic.BasicAlignerStrategy import BasicAlignerStrategy
from lib.src.align.aligner.random.RandomAlignerStrategy import RandomAlignerStrategy
from lib.src.align.aligner.google.GoogleFilesAligner import GoogleFilesAligner
from lib.src.align.aligner.google.GoogleBiopythonAlignerStrategy import GoogleBiopythonAlignerStrategy
from lib.src.align.aligner.google.GoogleGlobalCharacterAlignerStrategy import GoogleGlobalCharacterAlignerStrategy
from lib.src.align.aligner.google.GoogleGlobalWordAlignerStrategy import GoogleGlobalWordAlignerStrategy
from lib.src.align.aligner.google.GoogleSemiglobalCharacterAlignerStrategy import GoogleSemiglobalCharacterAlignerStrategy
from lib.src.align.aligner.google.GoogleSemiglobalWordAlignerStrategy import GoogleSemiglobalWordAlignerStrategy
from lib.src.align.aligner.google.GoogleLocalCharacterAlignerStrategy import GoogleLocalCharacterAlignerStrategy
from lib.src.align.aligner.google.GoogleLocalWordAlignerStrategy import GoogleLocalWordAlignerStrategy
from unittest_data_provider import data_provider
from lib.src.align.aligner.get_aligner import get_aligner


class TestGetAligner(unittest.TestCase):

    get_aligner_data_provider = lambda: (
        ("basic", FilesAligner, BasicAlignerStrategy),
        ("random", FilesAligner, RandomAlignerStrategy),
        ("google_biopython", GoogleFilesAligner, GoogleBiopythonAlignerStrategy),
        ("google_global_character", GoogleFilesAligner, GoogleGlobalCharacterAlignerStrategy),
        ("google_global_word", GoogleFilesAligner, GoogleGlobalWordAlignerStrategy),
        ("google_semiglobal_character", GoogleFilesAligner, GoogleSemiglobalCharacterAlignerStrategy),
        ("google_semiglobal_word", GoogleFilesAligner, GoogleSemiglobalWordAlignerStrategy),
        ("google_local_character", GoogleFilesAligner, GoogleLocalCharacterAlignerStrategy),
        ("google_local_word", GoogleFilesAligner, GoogleLocalWordAlignerStrategy)
    )

    @data_provider(get_aligner_data_provider)
    def test_get_aligner(self, desired: str, expected_aligner: Type, expected_strategy: Type) -> None:
        """
        Tests get_aligner function's behevaiour
        :return:
        """
        config = {
            "foo": "bar",
            "aligner_type": desired,
        }

        aligner = get_aligner(config)

        self.assertIsInstance(aligner, expected_aligner)
        self.assertIsInstance(aligner.aligner, expected_strategy.__class__)


if __name__ == '__main__':
    unittest.main()
