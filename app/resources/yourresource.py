from .. import db
from ..models import YourModel

class YourResource:
    """
    Your resource that performs data validation and interacts with the model directly.
    """

    @classmethod
    def get_from_data(cls, data: dict):
        # Iterate through the dictionary to find a matching column and value
        for key, value in data.items():
            if hasattr(YourModel, key):
                return YourModel.query.filter(getattr(YourModel, key) == value).all()
        
        return None
    
    @classmethod
    def create_from_data(data):
        yourmodel = YourModel()
        db.session.add(yourmodel)
        return YourResource.update_model(yourmodel, data)
    
    @classmethod
    def update_from_data(data):
        if data.get('id'):
            yourmodel = YourModel.query.get(data.get('id'))
            if yourmodel:
                return YourResource.update_model(yourmodel, data)
        return False, "ID must be provided.", None
    
    @classmethod
    def update_model(yourmodel, data):
        return YourResource.validate_and_submit(yourmodel)
    
    @classmethod
    def validate_and_submit(yourmodel):
        db.session.commit()
        return True, "Model updated.", yourmodel