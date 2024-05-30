from models import MyModel, AnotherModel
from base_model import BaseModel

# Create tables
MyModel.create_table()
AnotherModel.create_table()

# Create a new model instance
my_model = MyModel(name="My_First_Model", my_number=89)
my_model.save()

# Retrieve the model instance from the database
retrieved_model = MyModel.get(my_model.id)
print("Retrieved Model:", retrieved_model.to_dict())

# Check all instances of MyModel
all_models = MyModel.all()
for model in all_models:
    print("All Models:", model.to_dict())

# Convert to dictionary and back to model
my_model_json = my_model.to_dict()
my_new_model = MyModel.from_dict(my_model_json)
print("New Model from JSON:", my_new_model.to_dict())

# Check if they are the same instance
print("Same instance:", my_model is my_new_model)

# Update the model instance
my_model.update(name="Updated_Model")
print("Updated Model:", MyModel.get(my_model.id).to_dict())

# Add foreign key example
BaseModel.add_foreign_key('AnotherModel', 'my_model_id', 'MyModel', 'id')

# Create AnotherModel instance with a foreign key reference
another_model = AnotherModel(description="Sample Description", amount=99.99)
another_model.my_model_id = my_model.id  # Ensure my_model.id exists
another_model.save()
print("Another Model with Foreign Key:", AnotherModel.get(another_model.id).to_dict())

# Delete the model instance
my_model.delete()
print("Deleted Model:", MyModel.get(my_model.id))