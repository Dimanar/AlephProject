from followutils.entities.entity import Entity


class Contract(Entity):
    def __init__(self, item):
        super().__init__(item)
        self.entity_type = 'Contract'

    def make_id(self, entity):
        entity.make_id(self.data_dict['title'], self.data_dict['procedureNumber'])
        return entity
