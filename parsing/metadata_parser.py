import re


class MetadaParser:
    """Parses and validates the optional `[key=value ...]` metadata blocks."""

    def get_brackets(self, line: str) -> list[str]:
        """Return the raw contents of every `[...]` block in the line."""
        return re.findall(r"\[(.*?)\]", line)

    def check_valid_keys(self, line: tuple[int, str], valid_keys: set[str]) -> dict[str, str]:
        """Parse a metadata block and validate its keys.

        Args:
            line: (line_number, content) tuple.
            valid_keys: The set of metadata keys allowed for this line type.

        Returns:
            A dict of key/value pairs found in the metadata block, or an
            empty dict if the line has no metadata block.
        """
        line_number, content = line
        brackets = self.get_brackets(content)
        if not brackets:
            return {}
        tokens = brackets[0].split()
        if not tokens:
            raise ValueError(f"line {line_number}: empty metadata block")
        metadata: dict[str, str] = {}
        for token in tokens:
            if "=" not in token:
                raise ValueError(
                    f"line {line_number}: invalid metadata token '{token}', "
                    "expected key=value"
                )
            key, _, value = token.partition("=")
            if key not in valid_keys:
                raise ValueError(f"line {line_number}: unknown metadata key '{key}'")
            if not value:
                raise ValueError(f"line {line_number}: metadata key '{key}' has no value")
            if key in metadata:
                raise ValueError(f"line {line_number}: duplicate metadata key '{key}'")
            metadata[key] = value
        return metadata

    def _to_positive_int(self, line_number: int, key: str, value: str) -> int:
        """Validate and convert a metadata value expected to be a positive int.
 
        Uses str.isdigit() before calling int() so an invalid value (e.g.
        "abc" or "-3") raises a clean, line-numbered error instead of a
        raw ValueError from int().
        """
        if not value.isdigit() or int(value) <= 0:
            raise ValueError(f"line {line_number}: {key} must be a positive integer")
        return int(value)
 
    def conexion_metadata(self, line: tuple[int, str]) -> dict[str, object]:
        """Validate and return metadata for a connection line."""
        valid_connection_keys = {"max_link_capacity"}
        raw_metadata = self.check_valid_keys(line, valid_connection_keys)
        metadata: dict[str, object] = dict(raw_metadata)
        if "max_link_capacity" in metadata:
            metadata["max_link_capacity"] = self._to_positive_int(
                line[0], "max_link_capacity", raw_metadata["max_link_capacity"]
            )
        return metadata
 
    def zone_metadata(self, line: tuple[int, str]) -> dict[str, object]:
        """Validate and return metadata for a zone line."""
        valid_zone_keys = {"zone", "color", "max_drones"}
        valid_zone_types = {"normal", "blocked", "restricted", "priority"}
        raw_metadata = self.check_valid_keys(line, valid_zone_keys)
        if "zone" in raw_metadata and raw_metadata["zone"] not in valid_zone_types:
            raise ValueError(f"line {line[0]}: invalid zone type '{raw_metadata['zone']}'")
        metadata: dict[str, object] = dict(raw_metadata)
        if "max_drones" in metadata:
            metadata["max_drones"] = self._to_positive_int(
                line[0], "max_drones", raw_metadata["max_drones"]
            )
        return metadata