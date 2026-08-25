from parsing import MainParser, SourceReader
from initialization import ZoneFactory, ConnectionFactory 
from graph import Graph

#i should check if he did not find the file/folder what happen
class Network:
    def __init__(self):
        self.zones = ZoneFactory()
        self.factory = {
            "connection": ConnectionFactory(),
            "start_hub": self.zones,
            "hub": self.zones,
            "end_hub": self.zones
        }

    def start(self, file_name):
        reader = SourceReader(file_name)
        parsing = MainParser()
        lines = parsing.check_grammar(reader.read_lines())
        for line in lines[1:]:
            self.factory[line[1]].builder(line, self.zones.zones)
        graph = Graph(self.zones.zones, self.factory["connection"].connections)
        # print(self.zones.zones)
        # print(self.factory["connection"].connections)
            

if __name__ == "__main__":
    network = Network()
    network.start("maps/easy/01_linear_path.txt")