from string import punctuation


def preprocess_string(input: str) -> str:
    """
    Preprocesses a given string to be fit for alignment.
    :param input: String to process
    :return: Processed string
    """
    input = input.replace('*', '')
    input = ''.join([c for c in list(input) if c not in punctuation])
    input = input.encode('utf8', 'ignore').decode('utf8')

    return input.lower()
