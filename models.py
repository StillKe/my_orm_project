from base_model import BaseModel

class MyModel(BaseModel):
    def __init__(self, name=None, my_number=None, **kwargs):
        super().__init__(name=name, my_number=my_number, **kwargs)
        self.name = name
        self.my_number = my_number

    @classmethod
    def additional_columns(cls):
        return "name TEXT, my_number INTEGER"

class AnotherModel(BaseModel):
    def __init__(self, description=None, amount=None, **kwargs):
        super().__init__(description=description, amount=amount, **kwargs)
        self.description = description
        self.amount = amount

    @classmethod
    def additional_columns(cls):
        return "description TEXT, amount REAL"