import unittest
from unittest_data_provider import data_provider
from lib.src.model.Sentence import Sentence
from lib.src.align.compare.load_alignment import load_alignment
from lib.test.test_utils.TempFile import TempFile


class TestLoadAlignment(unittest.TestCase):
    """
    Tests lib.src.align.compare.load_alignment
    """

    load_alignment_data_provider = lambda: (
        ("0.0\t0.1\tfoo\n0.1\t0.2\tbar\n0.2\t0.3\tbaz", 3),
        ("", 0),
    )

    @data_provider(load_alignment_data_provider)
    def test_load_alignment(self, file_content: str, expected_list_length: int) -> None:
        """
        Tests load_alignment function's behaviour.
        :param file_content:
        :param expected_list_length:
        :return: None
        """

        # Create temporary file to open
        file = TempFile(file_content)
        result = load_alignment(file.get_name())
        file.delete()

        self.assertEqual(expected_list_length, len(result))

        for el in result:
            self.assertIsInstance(el, Sentence)


if __name__ == '__main__':
    unittest.main()
