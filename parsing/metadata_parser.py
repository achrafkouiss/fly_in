import re

class MetadaParser():
    def get_brackets(self, line: str):
        return re.findall(r"\[(.*?)\]", line)

    def check_valid_keys(self, line: tuple[int, str], valid_keys):
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

    def conexion_metadata(self, line: tuple[int, str]) -> dict:
        VALID_CONNECTION_KEYS = {"max_link_capacity"}
        metadata = self.check_valid_keys(line, VALID_CONNECTION_KEYS)
        if "max_link_capacity" in metadata:
            cap = metadata["max_link_capacity"]
            if not cap.isdigit() or int(cap) <= 0:
                raise ValueError(
                    f"line {line[0]}: max_link_capacity must be a positive integer"
                )
        return metadata

    def zone_metadata(self, line: tuple[int, str]) -> dict:
        VALID_ZONE_KEYS = {"zone", "color", "max_drones"}
        VALID_ZONE_TYPES = {"normal", "blocked", "restricted", "priority"}
        metadata = self.check_valid_keys(line, VALID_ZONE_KEYS)
        if "zone" in metadata and metadata["zone"] not in VALID_ZONE_TYPES:
            raise ValueError(
                f"line {line[0]}: invalid zone type '{metadata['zone']}'"
            )
        if "max_drones" in metadata:
            mx = metadata["max_drones"]
            # print(metadata)
            if not mx.isdigit() or int(mx) <= 0:
                raise ValueError(
                    f"line {line[0]}: max_drones must be a positive integer"
                )
        return metadata
