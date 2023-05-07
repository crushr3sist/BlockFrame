import json
import json
import xml.etree.ElementTree as ET
from types import SimpleNamespace


class Config:
    def __init__(self, file_path):
        self.file_path = file_path
        self.option_dict = {
            "json": "from_json",
            "py": "from_pyfile",
            "xml": "from_xml",
            "toml": "from_toml",
        }

        self.execute_config_extraction = self.option_dict[str(file_path).split(".")[1]]
        self.config_id = (getattr(self, self.execute_config_extraction))()

    def from_json(self):
        return json.loads(open(self.file_path, "rb").read())

    def from_pyfile(self):
        with open(self.file_path, "r") as f:
            config_dict = {}
            exec(compile(f.read(), self.file_path, "exec"), config_dict)
            return config_dict

    def from_xml(self):
        root = ET.parse(self.file_path).getroot()
        return SimpleNamespace(**{child.tag: child.text for child in root})

    def from_toml(self):
        with open(self.file_path, "rb") as f:
            return toml.load(f)
