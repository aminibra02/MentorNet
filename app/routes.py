from flask import render_template, redirect, url_for, flash
from app import app, db # app and db should be imported from app package
from app.models import Student, Mentor, Match # Ensure Match is imported
from app.forms import StudentSignupForm, MentorSignupForm # Add MentorSignupForm here

# Add a simple home route for now
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home') # Updated

@app.route('/student/signup', methods=['GET', 'POST'])
def student_signup():
    form = StudentSignupForm()
    if form.validate_on_submit():
        # Check if email already exists
        existing_student = Student.query.filter_by(email=form.email.data).first()
        if existing_student:
            flash('That email address is already registered. Please use a different one.', 'danger')
            return redirect(url_for('student_signup'))

        student = Student(name=form.name.data, email=form.email.data, subject=form.subject.data)
        db.session.add(student)
        db.session.commit()
        flash(f'Account created for {form.name.data}! You can now seek a mentor.', 'success')
        return redirect(url_for('home')) # Redirect to a home page or a student dashboard later
    return render_template('student_signup.html', title='Student Signup', form=form)

@app.route('/mentor/signup', methods=['GET', 'POST'])
def mentor_signup():
    form = MentorSignupForm()
    if form.validate_on_submit():
        # Check if email already exists
        existing_mentor = Mentor.query.filter_by(email=form.email.data).first()
        if existing_mentor:
            flash('That email address is already registered by a mentor. Please use a different one.', 'danger')
            return redirect(url_for('mentor_signup'))

        mentor = Mentor(name=form.name.data,
                        email=form.email.data,
                        subject=form.subject.data,
                        availability=form.availability.data)
        db.session.add(mentor)
        db.session.commit()
        flash(f'Mentor account created for {form.name.data}! Students can now find you.', 'success')
        return redirect(url_for('home')) # Redirect to a home page or a mentor dashboard later
    return render_template('mentor_signup.html', title='Mentor Signup', form=form)

@app.route('/admin/trigger-matching') # Or a more suitable route
def trigger_matching():
    students = Student.query.all()
    mentors = Mentor.query.all()
    matches_made = 0

    for student in students:
        for mentor in mentors:
            # Check if subjects match (case-insensitive comparison)
            if student.subject.lower() == mentor.subject.lower():
                # Check if this match already exists
                existing_match = Match.query.filter_by(
                    student_id=student.id,
                    mentor_id=mentor.id,
                    subject=student.subject # Or mentor.subject, they are the same after .lower() check
                ).first()

                if not existing_match:
                    # Create new match
                    new_match = Match(student_id=student.id, mentor_id=mentor.id, subject=student.subject)
                    db.session.add(new_match)
                    matches_made += 1
    
    if matches_made > 0:
        db.session.commit()
        flash(f'{matches_made} new match(es) created!', 'success')
    else:
        flash('No new matches found.', 'info')
    
    return redirect(url_for('home')) # Redirect to home or a matches page

@app.route('/matches')
def list_matches():
    # Query to get matches along with student and mentor names
    # This uses the relationships defined in the models.
    all_matches = Match.query.all() 
    
    # For a more optimized query, especially with many matches,
    # you could consider joined loading if not relying solely on backrefs for name access in template:
    # from sqlalchemy.orm import joinedload
    # all_matches = Match.query.options(joinedload(Match.student), joinedload(Match.mentor)).all()
    
    return render_template('matches.html', title='All Matches', matches=all_matches)
