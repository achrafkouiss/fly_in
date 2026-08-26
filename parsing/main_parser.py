from .source_reader import SourceReader
from .parser import HeaderParser, ConnectionParser, ZoneParser, Parser
from .metadata_parser import MetadaParser


class MainParser:
    """Validates and converts raw map lines into structured tuples."""

    def __init__(self) -> None:
        """Initialize the parser and its keyword dispatch table."""
        self.new_data: list[tuple] = []
        metadata = MetadaParser()
        zone_parser = ZoneParser(metadata)
        self.dispatch: dict[str, Parser] = {
            "nb_drones": HeaderParser(),
            "connection": ConnectionParser(metadata),
            "start_hub": zone_parser,
            "hub": zone_parser,
            "end_hub": zone_parser,
        }

    @staticmethod
    def get_keyword(content: str) -> str:
        """Extract the leading keyword (text before the first ':') of a line."""
        return content.split(":", 1)[0].strip()

    def check_grammar(self, lines: list[tuple[int, str]]) -> list[tuple]:
        """Validate and parse every line, populating self.new_data."""
        for line_number, content in lines:
            keyword = self.get_keyword(content)
            parser = self.dispatch.get(keyword)
            if parser is None:
                raise ValueError(f"line {line_number} :{content} is not correct")
            self.new_data.append(parser.line_format_checker((line_number, content)))
        self.checks()
        return self.new_data

    def check_necessery_line(self) -> None:
        """Ensure the required line types appear the expected number of times."""
        strings = {"nb_drones": 0, "start_hub": 0, "end_hub": 0, "connection": 0}
        for line in self.new_data:
            if line[1] in strings:
                strings[line[1]] += 1
            if strings.get(line[1], 0) != 1 and line[1] in (
                "nb_drones",
                "start_hub",
                "end_hub",
            ):
                raise ValueError(
                    f"{line[0]}: there should be one {line[1]} no less and no more"
                )
            if strings.get(line[1], 0) < 1 and line[1] == "connection":
                raise ValueError("there should atleast one connection.")
        zero_keys = [key for key, value in strings.items() if value == 0]
        if zero_keys:
            raise ValueError(f"there is no {' and '.join(zero_keys)}")

    def check_duplicate_connection_name(self) -> None:
        """Ensure no connection is a self-loop or duplicates another connection."""
        connections = [line for line in self.new_data if line[1] == "connection"]
        for index, line in enumerate(connections):
            name1, name2 = line[2]
            if name1 == name2:
                raise ValueError(
                    f"line {line[0]}: {line[2]} names of the zones should not be the same"
                )
            for other in connections[index + 1:]:
                if sorted((name1, name2)) == sorted(other[2]):
                    raise ValueError(
                        f"line {line[0]} and {other[0]}: "
                        f"{line[2]} and {other[2]} duplicated connection"
                    )

    def checks(self) -> None:
        """Run all cross-line validation checks."""
        self.check_necessery_line()
        if self.new_data[0][1] != "nb_drones":
            raise ValueError(
                f"line {self.new_data[0][0]}: The first line should defines the "
                "number of drones using nb_drones: <number>."
            )
        self.check_duplicate_connection_name()


if __name__ == "__main__":
    reader = SourceReader("../maps/easy/01_linear_path.txt")
    parsing = MainParser()
    parsing.check_grammar(reader.read_lines())
    # print(parsing.new_data)