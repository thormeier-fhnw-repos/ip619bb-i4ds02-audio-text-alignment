from string import punctuation


def preprocess_string(input: str) -> str:
    """
    Preprocesses a given string to be fit for alignment.

    :param input: String to process

    :return: Processed string
    """
    input = input.replace("*", "")

    input = input.encode("utf8", "ignore").decode("utf8")

    # Make sure to always have a space after a punctuation sign.
    for punct_sign in list(punctuation):
        input = input.replace(punct_sign + " ", punct_sign)
        input = input.replace(punct_sign, punct_sign + " ")

    input = " ".join(input.split())

    input = "".join([c for c in list(input) if c not in punctuation])

    return input.lower()
