import os


class SourceReader:
    """A class to handle secure and clean file reading operations."""

    def __init__(self, file_path: str):
        """Initializes the reader with a targeted file path."""
        self.file_path = file_path

    def strip_comments(self, line: str):
        """Strip the comments from the line."""
        return line.split("#")[0].rstrip()

    def read_lines(self) -> list:
        """Reads the file and returns a structured list of individual lines."""
        if not os.path.exists(self.file_path):
            return []
        try:
            with open(self.file_path, "r") as file:
                result = []
                for line_number, line in enumerate(file, start=1):
                    cleaned = self.strip_comments(line.strip())
                    if cleaned:
                        result.append((line_number, cleaned))
                return result
        except (OSError):
            return []

if __name__=="__main__":
    input = SourceReader("../maps/easy/01_linear_path.txt")
    # print(input.read_lines())