from app import db # Import db from the app package

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    matches = db.relationship('Match', foreign_keys='Match.student_id', backref='student', lazy=True)

    def __repr__(self):
        return f"Student('{self.name}', '{self.email}', '{self.subject}')"

class Mentor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    availability = db.Column(db.String(200), nullable=False) # e.g., "Mon 9-12, Wed 2-5"
    matches = db.relationship('Match', foreign_keys='Match.mentor_id', backref='mentor', lazy=True)

    def __repr__(self):
        return f"Mentor('{self.name}', '{self.email}', '{self.subject}')"

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    mentor_id = db.Column(db.Integer, db.ForeignKey('mentor.id'), nullable=False)
    subject = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Match('{self.student.name}' with '{self.mentor.name}' for '{self.subject}')"
