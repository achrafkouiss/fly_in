import re
from abc import ABC, abstractmethod
from typing import Optional
from .metadata_parser import MetadaParser


class Parser(ABC):
    """Common interface for line-format validators/parsers."""

    @abstractmethod
    def line_format_checker(self, line: tuple[int, str]) -> tuple:
        """Validate a line's format and return its parsed representation."""

    @abstractmethod
    def data_updater(self, line: tuple[int, str], metadata: Optional[dict] = None) -> tuple:
        """Convert a validated line into a structured tuple.

        Args:
            line: (line_number, content) tuple.
            metadata: Parsed metadata dict, when relevant to this parser.
        """


class HeaderParser(Parser):
    """Parses the mandatory `nb_drones: <number>` line."""

    _PATTERN = re.compile(r"^nb_drones:\s*\d+$")

    def line_format_checker(self, line: tuple[int, str]) -> tuple:
        """Validate and parse the drone-count header line."""
        if not self._PATTERN.match(line[1]):
            raise ValueError(
                f"line {line[0]} : the header line should be "
                "nb_drones: <positive number>"
            )
        return self.data_updater(line)

    def data_updater(self, line: tuple[int, str], metadata: Optional[dict] = None) -> tuple:
        """Convert the header line into (line_number, 'nb_drones', count)."""
        parts = line[1].replace(":", " ").split()
        name = parts[0]
        drones = int(parts[1])
        if drones <= 0:
            raise ValueError(f"line {line[0]}: nb_drones must be a positive integer.")
        return (line[0], name, drones)


class ConnectionParser(Parser):
    """Parses `connection: <name1>-<name2> [metadata]` lines."""

    _PATTERN = re.compile(
        r"^connection:\s*[a-zA-Z0-9]+-[a-zA-Z0-9]+(?:\s+\[[^\]]*\])?$"
    )

    def __init__(self, metadataparser: MetadaParser) -> None:
        """Store the shared metadata parser."""
        self.metadataparser = metadataparser

    def line_format_checker(self, line: tuple[int, str]) -> tuple:
        """Validate and parse a connection line."""
        metadata = self.metadataparser.conexion_metadata(line)
        if not self._PATTERN.match(line[1]):
            raise ValueError(
                f"line {line[0]}: connexion should be like this "
                "(connection: <name1>-<name2> [metadata]) metadata is optionnal"
            )
        return self.data_updater(line, metadata)

    def data_updater(self, line: tuple[int, str], metadata: Optional[dict] = None) -> tuple:
        """Convert a validated connection line into a structured tuple."""
        data = line[1].replace(":", " ").split()
        endpoints = tuple(data[1].replace("-", " ").split())
        if metadata:
            return (line[0], data[0], endpoints, metadata)
        return (line[0], data[0], endpoints)


class ZoneParser(Parser):
    """Parses `(start_hub|hub|end_hub): <name> <x> <y> [metadata]` lines."""

    _PATTERN = re.compile(
        r"^(start_hub|hub|end_hub):\s+[a-zA-Z0-9]+\s+-?\d+\s+-?\d+(?:\s+\[[^\]]*\])?\s*$"
    )

    def __init__(self, metadataparser: MetadaParser) -> None:
        """Store the shared metadata parser."""
        self.metadataparser = metadataparser

    def line_format_checker(self, line: tuple[int, str]) -> tuple:
        """Validate and parse a zone line."""
        if not self._PATTERN.match(line[1]):
            raise ValueError(
                f"line {line[0]}: zone line should be "
                "'(start_hub|hub|end_hub): <name> <x> <y> [metadata]'"
            )
        metadata = self.metadataparser.zone_metadata(line)
        return self.data_updater(line, metadata)

    def data_updater(self, line: tuple[int, str], metadata: Optional[dict] = None) -> tuple:
        """Convert a validated zone line into a structured tuple."""
        body = line[1].split("[")[0]
        parts = body.replace(":", " ").split()
        zone_kind, name, x, y = parts[0], parts[1], int(parts[2]), int(parts[3])
        if metadata:
            return (line[0], zone_kind, name, x, y, metadata)
        return (line[0], zone_kind, name, x, y)