from followutils.entities.entity import Entity
import pandas as pd


class Company(Entity):
    def __init__(self, item):
        super().__init__(item)
        self.entity_type = 'Company'

    def from_csv_row(self, row: pd.core.series.Series):
        self.data_dict = row.to_dict()

    def make_id(self, entity):
        entity.id = self.add_id_prefix(self.data_dict['ogrnCode'], 'ogrn')
        return