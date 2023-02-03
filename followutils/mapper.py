import yaml
from typing import Dict


class Mapper:
    def __init__(self) -> None:
        self.yaml_documents = {}

    def _get_yml_mapping(self, yml_name: str, folder: str) -> Dict:
        with open(f"{folder}/{yml_name}.yaml", "r") as file:
            yaml_document = yaml.load(file, Loader=yaml.FullLoader)
        self.yaml_documents[yml_name] = yaml_document

        return yaml_document

    def __getitem__(self, name:str) -> Dict:
        if name in self.yaml_documents:
            return self.yaml_documents[name]
        else:
            return self._get_yml_mapping(name, folder='mapping')
