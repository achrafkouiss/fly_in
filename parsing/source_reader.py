import os


class SourceReader:
    """A class to handle secure and clean file reading operations."""

    def __init__(self, file_path: str) -> None:
        """Initializes the reader with a targeted file path."""
        self.file_path = file_path

    def strip_comments(self, line: str) -> str:
        """Strip the comments from the line."""
        return line.split("#")[0].rstrip()

    def read_lines(self) -> list[tuple[int, str]]:
        """Reads the file and returns a structured list of individual lines.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"file not found: '{self.file_path}'")
        with open(self.file_path, "r") as file:
            result = []
            for line_number, line in enumerate(file, start=1):
                cleaned = self.strip_comments(line.strip())
                if cleaned:
                    result.append((line_number, cleaned))
            return result

if __name__ == "__main__":
    reader = SourceReader("../maps/easy/01_linear_path.txt")
    print(reader.read_lines())