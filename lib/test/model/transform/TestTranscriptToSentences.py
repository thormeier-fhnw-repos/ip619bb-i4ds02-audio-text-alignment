import unittest
from lib.src.model.transform.transcript_to_sentences import transcricpt_to_sentences


class TestTranscriptToSentences(unittest.TestCase):
    """
    Tests the src.model.transform.transcript_to_sentences function.
    """

    def test_transcript_to_sentences(self):
        text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec sed dapibus nibh. Sed ornare sem id " \
               "lorem aliquet mollis. Nunc at viverra lorem. "
        sentences = transcricpt_to_sentences(text)
        self.assertEqual(4, len(sentences))


if __name__ == '__main__':
    unittest.main()
