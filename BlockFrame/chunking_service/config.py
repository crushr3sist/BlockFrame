import json
import tomllib as toml
import xml.etree.ElementTree as ET
from types import SimpleNamespace


class Config:
    def __init__(self, file_path):
        """
        This function initializes an object with a file path and extracts configuration data based on the
        file extension.

        :param file_path: The file path of the configuration file that needs to be read and parsed
        """
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
        """
        This function reads a JSON file and returns its contents as a Python object.
        :return: The function `from_json` is returning the contents of a JSON file located at
        `self.file_path` as a Python object. The contents are read using the `open` function with the file
        path and mode "rb" (read binary), and then loaded into a Python object using the `json.loads`
        function.
        """
        return json.loads(open(self.file_path, "rb").read())

    def from_pyfile(self):
        """
        This function reads a Python file and executes its contents, returning a dictionary of the resulting
        variables.
        :return: The function `from_pyfile` is returning a dictionary object `config_dict` that is created
        by executing the Python code in the file specified by `self.file_path`. The code in the file is read
        using the `open` function, and then executed using the `exec` function. The resulting dictionary is
        then returned.
        """
        with open(self.file_path, "r") as f:
            config_dict = {}
            exec(compile(f.read(), self.file_path, "exec"), config_dict)
            return config_dict

    def from_xml(self):
        """
        This function parses an XML file and returns its contents as a namespace object.
        :return: A namespace object is being returned, created from the XML file located at
        `self.file_path`. The namespace object has attributes corresponding to the tags in the XML file, and
        the values of those attributes are the text content of the corresponding tags.
        """
        root = ET.parse(self.file_path).getroot()
        return SimpleNamespace(**{child.tag: child.text for child in root})

    def from_toml(self):
        """
        This function reads a TOML file and returns its contents as a Python object.
        :return: the contents of a TOML file located at `self.file_path` after loading it using the
        `toml.load()` method.
        """
        with open(self.file_path, "rb") as f:
            return toml.load(f)
