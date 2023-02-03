from followutils.entities.entity import Entity
import pandas as pd


class Organisation(Entity):
    def __init__(self, item):
        super().__init__(item)
        self.entity_type = 'Company'

    def from_csv_row(self, row: pd.Series):
        self.data_dict = row.to_dict()

    def make_id(self, entity):
        entity.make_id(self.data_dict['name'], self.data_dict['idNumber'])
        return entity