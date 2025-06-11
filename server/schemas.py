from marshmallow import Schema, fields, ValidationError

class MoveSchema(Schema):
    """Schema for validating move requests."""
    board = fields.List(
        fields.Raw(allow_none=True), 
        required=True, 
        validate=lambda x: len(x) == 9
    )
    index = fields.Integer(
        required=True, 
        validate=lambda x: 0 <= x <= 8
    )

def validate_move_input(data):
    """Validate move input data."""
    schema = MoveSchema()
    try:
        return schema.load(data), None
    except ValidationError as err:
        return None, err.messages