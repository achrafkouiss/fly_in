from source_reader import SourceReader
from parser import HeaderParser, ConnectionParser, ZoneParser
from metadata_parser import MetadaParser


class MainParser:
    def __init__(self):
        self.new_data : list[tuple] = []
        self.header = HeaderParser()
        self.metadaparser = MetadaParser()
        self.zoneparser = ZoneParser(self.metadaparser)
        self.connection = ConnectionParser(self.metadaparser)
        

    def check_unrelated_string(self, lines: list[tuple[int, str]]):
        word_list = ["nb_drones", "start_hub", "hub", "end_hub", "connection"]
        for line in lines:
            if not any(item in line[1] for item in word_list):
                raise ValueError(f"line {line[0]} :{line[1]} is not correct")


    def check_grammar(self, lines: list[tuple[int, str]]):
        self.check_unrelated_string(lines)

        for line in lines:
            if "nb_drones" in line[1]:
                data = self.header.line_format_checker(line)
                self.new_data.append(data)
            elif "connection" in line[1]:
                data = self.connection.line_format_checker(line)
                self.new_data.append(data)
            elif any(word in line[1] for word in  ["start_hub", "hub", "end_hub"]):
                data = self.zoneparser.line_format_checker(line)
                self.new_data.append(data)
        self.checks()
        for line in self.new_data:
            print(line)

    def check_necessery_line(self):
        strings = {
            "nb_drones": 0,
            "start_hub": 0,
            "end_hub": 0,
            "connection": 0
            }
        for line in self.new_data:
            if line[1] in strings.keys():
                strings[line[1]] += 1
            if not (strings.get(line[1], 0) == 1) and line[1] in ["nb_drones", "start_hub", "end_hub"]:
                raise ValueError(f"{line[0]}: there should be one {line[1]} no less and no more")
            elif (strings.get(line[1], 0) < 1) and line[1] == "connection":
                raise ValueError("there should atleast one connection.")
        zero_keys = [key for key, value in strings.items() if value == 0]
        if zero_keys:
            raise ValueError(f"there is no {' and '.join(zero_keys)}")

    def checks(self):
        self.check_necessery_line()
        if self.new_data[0][1] != "nb_drones":
            raise ValueError(f"line {self.new_data[0][0]}: The first line should defines the number of drones using nb_drones: <number>.")
        # self.connection.check_duplicate(self.new_data)

if __name__=="__main__":
    input = SourceReader("../maps/easy/01_linear_path.txt")
    parsing = MainParser()
    parsing.check_grammar(input.read_lines())
