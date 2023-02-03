import pandas as pd
import random
import string
from typing import List, Dict
import followthemoney as ftm


def get_unique_id():
    # This should be fixed
    return ''.join(random.sample(string.ascii_letters, 24))


class Entity:
    def __init__(self, item):
        self.entity_type = None
        if type(item) == pd.Series:
            self.from_csv_row(item.copy())
        else:
            raise TypeError("Unrecognised input type! Currently supported types: [pd.Series]")

    def from_csv_row(self, row: pd.Series):
        self.data_dict = row.to_dict()

    def add_id_prefix(self, item_id, prefix='ogrn'):
        return f"ru-{prefix}-{item_id}"

    def make_id(self, entity, ):
        entity.id = self.add_id_prefix(get_unique_id(), 'other')
        return entity

    def set_property(self, property_name, property_value):
        self.data_dict[property_name] = property_value

    def to_ftm(self):
        entity = ftm.model.make_entity(self.entity_type)
        entity = self.make_id(entity)
        for property_name, property_value in self.data_dict.items():
            print(property_name, property_value)
            if property_name == 'phone':
                entity.add(property_name, property_value[0])
            else:
                entity.add(property_name, property_value)
        return entity