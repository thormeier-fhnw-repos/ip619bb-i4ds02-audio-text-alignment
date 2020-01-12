import tempfile
import shutil
import os


class TempDir:
    """
    A temporary directory to write files to, delets itself after usage
    """

    def __init__(self) -> None:
        self.path = tempfile.mkdtemp()
        pass

    def __del__(self) -> None:
        """
        Deconstructor to make sure the entire tree is deleted
        :return: None
        """
        self.delete()

    def get_path(self):
        """
        Get the temp dir path
        :return:
        """
        return self.path

    def delete(self) -> None:
        """
        Deletes the entire temp dir and all its contents
        :return:
        """
        shutil.rmtree(self.path)

    def create_file(self, name: str, content: str) -> None:
        """
        Creates a given file within the temporary directory with given content
        :param name:    Name of the file
        :param content: Content of the file
        :return:
        """
        file_path = self.path + os.path.sep + name
        with open(file_path, "w+") as file:
            file.write(content)
            file.close()
