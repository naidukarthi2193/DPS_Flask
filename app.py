from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://woinnuilgqisba:d34efb777d10fa1718a85413e679ed4fcdd212746e5f6a9f9c191e8354a74be1@ec2-54-165-90-230.compute-1.amazonaws.com:5432/d926ep6d3j9qcr'
db = SQLAlchemy(app)


# Model
class Student(db.Model):
    __tablename__ = "student"
    suid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(100))
    email = db.Column(db.String(100))
    contact_number = db.Column(db.String(100))
    emergency_number = db.Column(db.String(100))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, suid, name, address, email, contact_number, emergency_number):
        self.suid = suid
        self.name = name
        self.address = address
        self.email = email
        self.contact_number = contact_number
        self.emergency_number = emergency_number

    def __repr__(self):
        return f"{self.suid}"


db.create_all()


class StudentSchema(SQLAlchemySchema):
    class Meta(SQLAlchemySchema.Meta):
        model = Student
        sqla_session = db.session

    suid = fields.Number(dump_only=True)
    name = fields.String(required=True)
    address = fields.String(required=True)
    email = fields.String(required=True)
    contact_number = fields.String(required=True)
    emergency_number = fields.String(required=True)

@app.route('/', methods=['GET'])
def index():
    get_student = Student.query.all()
    student_schema = StudentSchema(many=True)
    students = student_schema.dump(get_student)
    return make_response(jsonify({"students": students}))


@app.route('/student/<suid>', methods=['GET'])
def get_todo_by_suid(suid):
    get_student = Student.query.get(suid)
    student_schema = StudentSchema()
    student = student_schema.dump(get_student)
    return make_response(jsonify({"students": student}))


@app.route('/student/<suid>', methods=['PUT'])
def update_todo_by_id(suid):
    data = request.get_json()
    get_student = Student.query.get(suid)
    if get_student == None:
        student = Student(suid = suid, **data)
        student.create()
        return make_response(jsonify({"students": data}), 200)
    if data.get('name'):
        get_student.name = data['name']
    if data.get('address'):
        get_student.address = data['address']
    if data.get('email'):
        get_student.email = data['email']
    if data.get('contact_number'):
        get_student.contact_number = data['contact_number']
    if data.get('emergency_number'):
        get_student.emergency_number = data['emergency_number']
    db.session.add(get_student)
    db.session.commit()
    student_schema = StudentSchema(only=[ 'suid', 'name', 'address', 'email', 'contact_number', 'emergency_number'])
    student = student_schema.dump(get_student)
    return make_response(jsonify({"students": student}))


@app.route('/student/<suid>', methods=['DELETE'])
def delete_todo_by_id(suid):
    get_student = Student.query.get(suid)
    db.session.delete(get_student)
    db.session.commit()
    return make_response("", 204)


@app.route('/student', methods=['POST'])
def create_todo():
    data = request.get_json()
    student = Student(**data)
    student.create()
    return make_response(jsonify({"students": data}), 200)


if __name__ == "__main__":
    app.run(debug=True)
