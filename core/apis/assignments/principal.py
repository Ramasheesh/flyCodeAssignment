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


# Example of Principal API to list all teachers

# @app.route('/principal/teachers', methods=['GET'])
# def list_teachers():
#     principal = request.headers.get('X-Principal')
#     if not principal or 'principal_id' not in principal:
#         return jsonify({"error": "Unauthorized"}), 403
    
#     teachers = Teacher.query.all()  # Assuming a Teacher model exists
#     response = [{"id": teacher.id, "created_at": teacher.created_at, "updated_at": teacher.updated_at} for teacher in teachers]
    
#     return jsonify({"data": response})

# # Example of Principal API to list all assignments (submitted or graded)

# @app.route('/principal/assignments', methods=['GET'])
# def list_assignments():
#     principal = request.headers.get('X-Principal')
#     if not principal or 'principal_id' not in principal:
#         return jsonify({"error": "Unauthorized"}), 403
    
#     assignments = Assignment.query.filter(Assignment.state.in_(['SUBMITTED', 'GRADED'])).all()
#     response = [{"id": a.id, "content": a.content, "state": a.state, "student_id": a.student_id, "teacher_id": a.teacher_id} for a in assignments]
    
#     return jsonify({"data": response})

# # Example of Principal API to grade/re-grade an assignment

# @app.route('/principal/assignments/grade', methods=['POST'])
# def grade_assignment():
#     principal = request.headers.get('X-Principal')
#     if not principal or 'principal_id' not in principal:
#         return jsonify({"error": "Unauthorized"}), 403
    
#     data = request.json
#     assignment_id = data.get("id")
#     grade = data.get("grade")
    
#     assignment = Assignment.query.get(assignment_id)
#     if not assignment:
#         return jsonify({"error": "Assignment not found"}), 404
    
#     assignment.grade = grade
#     assignment.state = "GRADED"
#     db.session.commit()
    
#     return jsonify({"data": {"id": assignment.id, "content": assignment.content, "grade": assignment.grade}})
