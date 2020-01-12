from tempfile import NamedTemporaryFile
import os


class TempFile:
    """
    Temporary file for convenience in tests that include opening and reading files.
    """

    def __init__(self, content: str) -> None:
        """
        Initializes a temporary file
        :param content: File content
        """
        with NamedTemporaryFile(delete=False, mode="w", encoding="utf-8") as f:
            f.write(content)
            f.flush()
            f.close()

            self.f = f.name

    def __del__(self) -> None:
        """
        Deconstructor to make sure the file is deleted
        :return: None
        """
        self.delete()

    def get_name(self) -> str:
        """
        Returns the temp files name
        :return: File name
        """
        return self.f

    def delete(self) -> None:
        """
        Delete the file from disk if it exists.
        :return:
        """
        if os.path.exists(self.f):
            os.unlink(self.f)
