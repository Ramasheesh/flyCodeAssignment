from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.teachers import Teacher  # Assuming there's a Teacher model
from core.models.assignments import Assignment
from .schema import AssignmentSchema

principal_resources = Blueprint('principal_resources', __name__)

@principal_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def view_all_teachers(p):
    """Returns a list of all teachers"""
    teachers = Teacher.query.all()
    teachers_data = [{"id": teacher.id, "name": teacher.name, "email": teacher.email} for teacher in teachers]
    return APIResponse.respond(data=teachers_data)

@principal_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def view_all_assignments(p):
    """Returns a list of all assignments"""
    assignments = Assignment.query.all()
    assignments_dump = AssignmentSchema().dump(assignments, many=True)
    return APIResponse.respond(data=assignments_dump)

@principal_resources.route('/assignments/regrade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def regrade_assignment(p, incoming_payload):
    """Re-grade an assignment"""
    assignment_id = incoming_payload.get('assignment_id')
    new_grade = incoming_payload.get('new_grade')

    assignment = Assignment.query.get(assignment_id)
    if not assignment:
        return APIResponse.respond_error('Assignment not found', 404)

    assignment.grade = new_grade
    db.session.commit()

    assignment_dump = AssignmentSchema().dump(assignment)
    return APIResponse.respond(data=assignment_dump)
