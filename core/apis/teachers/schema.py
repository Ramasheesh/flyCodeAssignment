from marshmallow import Schema, fields, validate
from core.models.assignments import Assignment

class AssignmentSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str()
    grade = fields.Str(validate=validate.OneOf(["A", "B", "C", "D", "F"]))
    student_id = fields.Int()
    teacher_id = fields.Int()

class AssignmentSubmitSchema(Schema):
    id = fields.Int(required=True)
    teacher_id = fields.Int(required=True)

class AssignmentGradeSchema(Schema):
    id = fields.Int(required=True)
    grade = fields.Str(validate=validate.OneOf(["A", "B", "C", "D", "F"]), required=True)
