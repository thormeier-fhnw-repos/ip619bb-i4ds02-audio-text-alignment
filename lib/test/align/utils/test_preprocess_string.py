import unittest
from string import punctuation
from unittest_data_provider import data_provider
from lib.src.align.utils.preprocess_string import preprocess_string


class TestPreprocessString(unittest.TestCase):
    """
    Tests lib.src.align.utils.preprocess_string
    """

    preprocess_string_data_provider = lambda: (
        ("abc", "abc"),
        ("".join(punctuation), ""),
        ("a.b,c", "abc"),
        ("abc😀abc", "abcabc"),
    )


    @data_provider(preprocess_string_data_provider)
    def test_preprocess_string(self, input_data: str, expected_output: str) -> None:
        """
        Tests preprocess_string function's behaviour
        :param input:           Input string
        :param expected_output: Expected output string
        :return: None
        """
        self.assertEqual(expected_output, preprocess_string(expected_output))


if __name__ == "__main__":
    unittest.main()
