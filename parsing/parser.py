from abc import ABC, abstractmethod
import re

# one of the questions i have is that in regex i do not need to put /s* at the start and in the end
class Parser(ABC):
    @abstractmethod
    def line_format_checker(self, line:tuple[int, str]):
        pass

    @abstractmethod
    def data_updater(self, line:tuple[int, str]):
        pass

class HeaderParser(Parser):
    def line_format_checker(self, line:tuple[int, str]):
         if not re.match(r"^nb_drones:\s*\d+$", line[1]):
            raise ValueError(f"line {line[0]} : the header line should be nb_drones: <positive number>")
         return (self.data_updater(line))

    def data_updater(self, line:tuple[int, str]):
        parts = line[1].replace(":", " ").split()
        name = parts[0]
        drones = int(parts[1])
        if drones <= 0:
            raise ValueError("nb_drones must be a positive integer.")
        return (line[0], name, drones)

class ConnectionParser(Parser):
    def __init__(self, metadataparser):
        self.metadataparser = metadataparser
    
    def line_format_checker(self, line:tuple[int, str]):
        metadata = self.metadataparser.conexion_metadata(line)
        data = r"^connection:\s*[a-zA-Z0-9]+-[a-zA-Z0-9]+(?:\s+\[[^\]]*\])?$"
        if not re.match(data, line[1]):
            raise ValueError(f"line {line[0]}: connexion should be like this (connection: <name1>-<name2> [metadata]) metadata is optionnal")
        return self.data_updater(line, metadata)
    
    def data_updater(self, line: tuple[int, str], metadata: str):
        data = line[1].replace(":", " ").split() 
        if metadata:
            return (line[0], data[0], tuple(data[1].replace("-", " ").split()), metadata)
        return (line[0], data[0], tuple(data[1].replace("-", " ").split()))

    # def check_duplicate(self, line: list[tuple]):
    #     for 

class ZoneParser(Parser):
    def __init__(self, metadataparser):
        self.metadataparser = metadataparser

    def line_format_checker(self, line: tuple[int, str]):
        pattern = r"^(start_hub|hub|end_hub):\s+[a-zA-Z0-9]+\s+-?\d+\s+-?\d+(?:\s+\[[^\]]*\])?\s*$"
        if not re.match(pattern, line[1]):
            raise ValueError(
                f"line {line[0]}: zone line should be "
                "'(start_hub|hub|end_hub): <name> <x> <y> [metadata]'"
            )
        metadata = self.metadataparser.zone_metadata(line)
        return self.data_updater(line, metadata)

    def data_updater(self, line: tuple[int, str], metadata: dict):
        body = line[1].split("[")[0]
        parts = body.replace(":", " ").split()
        zone_kind, name, x, y = parts[0], parts[1], int(parts[2]), int(parts[3])
        # if not (x >= 0 and y >= 0):
        #     raise ValueError(f"line {line[0]}: '{line[1]}' zone cordinate must be positive")
        if metadata:
            return (line[0], zone_kind, name, x, y, metadata)
        return (line[0], zone_kind, name, x, y)
