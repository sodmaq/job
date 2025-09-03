from flask import Flask, render_template, request, redirect, flash, url_for, session, flash, jsonify, send_from_directory
import mysql.connector
from mysql.connector import Error
import os
from flask import session
import os
import re
import fitz  # PyMuPDF
import docx  # python-docx
from werkzeug.utils import secure_filename



# app = Flask(__name__)
# app.secret_key = 'supersecret123'
app = Flask(__name__, static_folder='static', static_url_path='', template_folder='templates')
app.secret_key = 'supersecret123'

db_config = {
    'user': 'user_deb2e6c5',
    'password': '8ca5809f66c97bceb7967901c84296e5',
    'host': 'db.pxxl.pro',
    'port': 14871,
    'database': 'db_d728de84'
}

# Global DB connection
try:
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor(buffered=True)
    print("✅ Connected to MySQL database.")
except Error as e:
    print(f"❌ Error connecting to database: {e}")


@app.route('/test')
def home():
    return "Flask is working with MySQL!"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form['role']
        email = request.form['email']
        password = request.form['password']

        if not role or role not in ['job_seeker', 'employer']:
            flash("Please select a valid role.", "error")
            return redirect('/login')

        try:
            db = mysql.connector.connect(
                host='db.pxxl.pro',
                user='user_deb2e6c5',
                password='8ca5809f66c97bceb7967901c84296e5',
                database='job_portal'
            )
            cursor = db.cursor()

            # Choose table based on role
            table = 'users' if role == 'job_seeker' else 'employers'

            cursor.execute(f"SELECT * FROM {table} WHERE email = %s AND password = %s", (email, password))
            user = cursor.fetchone()

            
            if user:
                # Clear old sessions (to avoid role conflicts)
                session.clear()

                if role == 'job_seeker':
                    session['user_id'] = user[0]
                    session['user_name'] = user[1]
                    session['role'] = role
                    flash("✅ Logged in successfully as Job Seeker!", "success")
                    return redirect('/user/')
                else:
                    session['employer_id'] = user[0]
                    session['employer_name'] = user[1]
                    session['role'] = 'employer'
                    flash("✅ Logged in successfully as Employer!", "success")
                    return redirect('/employer/')

            else:
                flash("❌ Invalid email or password.", "error")
                return redirect('/login')

        except mysql.connector.Error as err:
            print("❌ Login error:", err)
            flash("Something went wrong. Please try again.", "error")

        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'db' in locals():
                db.close()

    return render_template('login.html')



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        role = request.form['role']
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        if not role or role not in ['job_seeker', 'employer']:
            flash("Please select a valid role.", "error")
            return redirect('/signup')

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect('/signup')

        try:
            db = mysql.connector.connect(
                host='db.pxxl.pro',
                user='user_deb2e6c5',
                password='8ca5809f66c97bceb7967901c84296e5',
                database='job_portal'
            )
            cursor = db.cursor()

            # Choose table based on role
            table = 'users' if role == 'job_seeker' else 'employers'

            # Check if email already exists in the chosen table
            cursor.execute(f"SELECT * FROM {table} WHERE email = %s", (email,))
            if cursor.fetchone():
                flash("Email already registered.", "error")
                return redirect('/signup')

            # Insert into appropriate table
            cursor.execute(
                f"INSERT INTO {table} (name, email, password) VALUES (%s, %s, %s)",
                (name, email, password)
            )
            db.commit()

            flash("✅ Account created successfully!", "success")
            return redirect('/login')

        except mysql.connector.Error as err:
            print("❌ Error during signup:", err)
            flash("Something went wrong. Please try again.", "error")

        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'db' in locals():
                db.close()

    return render_template('signup.html')


# ----------------------
# Employer Routes
# ----------------------
@app.route('/employer/')
def employer_index():
    db = None
    cursor = None
    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor(dictionary=True)

        # Ensure user is logged in and is an employer
        employer_id = session.get('employer_id')
        user_role = session.get('role')

        if not employer_id or user_role != 'employer':
            flash("Please log in as an employer to access the dashboard.", "error")
            return redirect('/login')


        # Count statistics
        cursor.execute("SELECT COUNT(*) AS total FROM jobs WHERE employer_id = %s", (employer_id,))
        posted_jobs = cursor.fetchone()['total']

        cursor.execute("SELECT COUNT(*) AS total FROM applications WHERE job_id IN (SELECT id FROM jobs WHERE employer_id = %s)", (employer_id,))
        total_applications = cursor.fetchone()['total']

        # After (no error)
        cursor.execute("SELECT COUNT(*) AS total FROM jobs WHERE employer_id = %s", (employer_id,))
        active_jobs = cursor.fetchone()['total']

        # Recent job posts
        cursor.execute("""
            SELECT j.id, j.title, j.created_at,
                (SELECT COUNT(*) FROM applications a WHERE a.job_id = j.id) AS applicant_count
            FROM jobs j
            WHERE j.employer_id = %s
            ORDER BY j.created_at DESC
            LIMIT 5
        """, (employer_id,))
        recent_jobs = cursor.fetchall()

        return render_template('employer/index.html',
                               posted_jobs=posted_jobs,
                               total_applications=total_applications,
                               active_jobs=active_jobs,
                               recent_jobs=recent_jobs)

    except mysql.connector.Error as err:
        print("❌ DB Error:", err)
        flash("Database error occurred.", "error")
        return redirect('/')

    finally:
        if cursor:  # Only close if cursor was created
            cursor.close()
        if db:  # Only close if db connection was created
            db.close()


@app.route('/employer/interview')
def employer_interview():
    try:
        db = mysql.connector.connect(
            host='db.pxxl.pro',
            user='user_deb2e6c5',
            password='8ca5809f66c97bceb7967901c84296e5',
            database='job_portal'
        )
        cursor = db.cursor(dictionary=True)

        cursor.execute("""
            SELECT a.id AS application_id, a.applied_at,
                u.name AS applicant_name, u.email AS applicant_email,
                j.title AS job_title
            FROM applications a
            JOIN users u ON a.user_id = u.id
            JOIN jobs j ON a.job_id = j.id
            WHERE a.status = 'invited'
            ORDER BY a.applied_at DESC
        """)

        interviews = cursor.fetchall()

    except mysql.connector.Error as err:
        print("❌ Error loading interview invites:", err)
        interviews = []

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db' in locals():
            db.close()

    return render_template('employer/interview.html', interviews=interviews)




#   -----------
#   POST JOB
#   -----------
@app.route('/employer/post_job', methods=['GET', 'POST'])
def employer_post_job():
    if request.method == 'POST':
        # Get form data
        title = request.form['title']
        company = request.form['company']
        department = request.form['department']
        job_type = request.form['job_type']
        experience = request.form['experience']
        salary = request.form['salary']
        location = request.form['location']
        description = request.form['description']
        skills = request.form['skills']

        try:
            db = mysql.connector.connect(
                host='db.pxxl.pro',
                user='user_deb2e6c5',
                password='8ca5809f66c97bceb7967901c84296e5',
                database='job_portal'
            )
            cursor = db.cursor()

            query = """
                INSERT INTO jobs (company, title, department, job_type, experience, salary, location, description, skills)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (company, title, department, job_type, experience, salary, location, description, skills))
            db.commit()

            flash("✅ Job posted successfully!", "success")

        except mysql.connector.Error as err:
            print("❌ Error posting job:", err)
            flash("❌ Failed to post job. Please try again.", "error")

        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'db' in locals():
                db.close()

    # Fetch job listings to show below the form
    try:
        db = mysql.connector.connect(
            host='db.pxxl.pro',
            user='user_deb2e6c5',
            password='8ca5809f66c97bceb7967901c84296e5',
            database='job_portal'
        )
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT * FROM jobs ORDER BY created_at DESC")
        jobs = cursor.fetchall()

    except mysql.connector.Error as err:
        print("❌ Failed to fetch jobs:", err)
        jobs = []

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db' in locals():
            db.close()

    return render_template("employer/post_job.html", jobs=jobs)


# ---------------
# EDIT JOBS
# ---------------

@app.route('/employer/edit-job/<int:job_id>', methods=['POST'])
def edit_job(job_id):
    # Get updated form data
    title = request.form['title']
    company = request.form['company']
    department = request.form['department']
    job_type = request.form['job_type']
    experience = request.form['experience']
    salary = request.form['salary']
    location = request.form['location']
    description = request.form['description']
    skills = request.form['skills']

    try:
        db = mysql.connector.connect(
            host='db.pxxl.pro',
            user='user_deb2e6c5',
            password='8ca5809f66c97bceb7967901c84296e5',
            database='job_portal'
        )
        cursor = db.cursor()

        query = """
            UPDATE jobs
            SET title = %s, company = %s, department = %s, job_type = %s, experience = %s,
                salary = %s, location = %s, description = %s, skills = %s
            WHERE id = %s
        """
        cursor.execute(query, (
            title, company, department, job_type, experience,
            salary, location, description, skills, job_id
        ))
        db.commit()

        flash("✅ Job updated successfully!", "success")

    except mysql.connector.Error as err:
        print(f"❌ Error updating job: {err}")
        flash("❌ Failed to update job. Please try again.", "error")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db' in locals():
            db.close()

    return redirect(url_for('employer_post_job'))


@app.route('/employer/delete-job/<int:job_id>', methods=['POST'])
def delete_job(job_id):
    try:
        db = mysql.connector.connect(
            host='db.pxxl.pro',
            user='user_deb2e6c5',
            password='8ca5809f66c97bceb7967901c84296e5',
            database='job_portal'
        )
        cursor = db.cursor()

        cursor.execute("SELECT * FROM jobs WHERE id = %s", (job_id,))
        job = cursor.fetchone()

        if not job:
            flash("❌ Job not found.", "error")
            return redirect(url_for('employer_post_job'))

        cursor.execute("DELETE FROM jobs WHERE id = %s", (job_id,))
        db.commit()

        if cursor.rowcount == 0:
            flash("❌ Failed to delete job. It might already be removed.", "error")
        else:
            flash("✅ Job deleted successfully!", "success")

    except mysql.connector.Error as err:
        print(f"❌ Error deleting job: {err}")
        flash("❌ Failed to delete job due to a database error.", "error")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db' in locals():
            db.close()

    return redirect(url_for('employer_post_job'))


@app.route("/employer/scheduled_interviews")
def employer_scheduled_interviews():
    if "employer_id" not in session:
        return redirect(url_for("employer_login"))

    db = mysql.connector.connect(**db_config)
    cursor = db.cursor(dictionary=True)

    query = """
        SELECT i.id, i.applicant_id, i.employer_id, i.job_id,
               i.interview_date, i.meeting_link, i.status,
               j.title AS job_title,
               u.name AS applicant_name
        FROM interviews i
        JOIN jobs j ON i.job_id = j.id
        JOIN users u ON i.applicant_id = u.id
        WHERE i.employer_id = %s
        ORDER BY i.interview_date ASC
    """
    cursor.execute(query, (session["employer_id"],))
    interviews = cursor.fetchall()

    # Format datetime
    for interview in interviews:
        try:
            dt = interview["interview_date"]
            if isinstance(dt, datetime):
                interview["formatted_date"] = dt.strftime("%b %d, %Y – %I:%M %p")
            else:
                interview["formatted_date"] = datetime.strptime(
                    dt, "%Y-%m-%d %H:%M:%S"
                ).strftime("%b %d, %Y – %I:%M %p")
        except:
            interview["formatted_date"] = interview["interview_date"]

    cursor.close()
    db.close()

    return render_template("employer/scheduled_interviews.html", interviews=interviews)

@app.route('/update_interview_status', methods=['POST'])
def update_interview_scheduled_status():
    interview_id = request.form['interview_id']
    status = request.form['status']

    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()

    cursor.execute(
        "UPDATE interviews SET status=%s WHERE id=%s",
        (status, interview_id)
    )
    db.commit()

    cursor.close()
    db.close()

    flash("Interview status updated successfully!", "success")
    return redirect(url_for('employer_scheduled_interviews'))


@app.route('/employer/view_applicants')
def employer_view_applicants():
    try:
        db = mysql.connector.connect(
            host='db.pxxl.pro',
            user='user_deb2e6c5',
            password='8ca5809f66c97bceb7967901c84296e5',
            database='job_portal'
        )
        cursor = db.cursor(dictionary=True)

        cursor.execute("""
            SELECT a.*, 
                   j.title AS job_title,
                   u.name AS applicant_name,u.phone AS applicant_phone,
                   u.email AS applicant_email
            FROM applications a
            JOIN jobs j ON a.job_id = j.id
            JOIN users u ON a.user_id = u.id
            WHERE a.status NOT IN ('rejected', 'invited', 'accepted')
            ORDER BY a.applied_at DESC
        """)
        applicants = cursor.fetchall()

    except mysql.connector.Error as err:
        print("❌ Error loading applicants:", err)
        applicants = []

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db' in locals():
            db.close()

    return render_template('employer/view_applicants.html', applicants=applicants)

@app.route('/employer/view_applicants/<int:job_id>')
def view_applicants(job_id):
    try:
        db = mysql.connector.connect(
            host='db.pxxl.pro',
            user='user_deb2e6c5',
            password='8ca5809f66c97bceb7967901c84296e5',
            database='job_portal'
        )
        cursor = db.cursor(dictionary=True)

        cursor.execute("""
            SELECT a.*, 
                   j.title AS job_title,
                   u.id AS user_id,
                   u.name AS applicant_name,
                   u.email AS applicant_email
            FROM applications a
            JOIN jobs j ON a.job_id = j.id
            JOIN users u ON a.user_id = u.id
            WHERE a.status != 'rejected' AND a.job_id = %s
            ORDER BY a.applied_at DESC
        """, (job_id,))
        applicants = cursor.fetchall()

    except mysql.connector.Error as err:
        print("❌ Error loading applicants:", err)
        applicants = []

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db' in locals():
            db.close()

    return render_template(
        'employer/view_applicants.html',
        applicants=applicants,
        job_id=job_id
    )

@app.route('/employer/invite/<int:application_id>/<int:job_seeker_id>/<int:job_id>', methods=['POST'])
def invite_applicant(application_id, job_seeker_id, job_id):
    try:
        interview_date = request.form.get("interview_date")
        interview_time = request.form.get("interview_time")
        meeting_link = request.form.get("meeting_link")

        db = mysql.connector.connect(
            host='db.pxxl.pro',
            user='user_deb2e6c5',
            password='8ca5809f66c97bceb7967901c84296e5',
            database='job_portal'
        )
        cursor = db.cursor()

        # 1. Update application status
        cursor.execute("UPDATE applications SET status = %s WHERE id = %s", ('invited', application_id))

        # 2. Insert into interviews table
        query = """
            INSERT INTO interviews (applicant_id, employer_id, job_id, interview_date, meeting_link)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            job_seeker_id,
            session["employer_id"], job_id, 
            f"{interview_date} {interview_time}",
            meeting_link
        ))

        db.commit()
        flash("✅ Applicant invited for interview. Meeting link saved.", "success")

    except mysql.connector.Error as err:
        print("❌ Error inviting applicant:", err)
        flash("❌ Failed to invite applicant.", "error")

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'db' in locals(): db.close()

    return redirect(url_for('employer_view_applicants'))

@app.route('/employer/reject/<int:applicant_id>', methods=['POST'])
def reject_applicant(applicant_id):
    try:
        db = mysql.connector.connect(
            host='db.pxxl.pro',
            user='user_deb2e6c5',
            password='8ca5809f66c97bceb7967901c84296e5',
            database='job_portal'
        )
        cursor = db.cursor()

        # Update the application status to "rejected"
        cursor.execute("UPDATE applications SET status = %s WHERE id = %s", ('rejected', applicant_id))
        db.commit()

        flash("⚠️ Applicant has been rejected.", "info")

    except mysql.connector.Error as err:
        print("❌ Error rejecting applicant:", err)
        flash("❌ Failed to reject applicant.", "error")

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'db' in locals(): db.close()

    return redirect(url_for('employer_view_applicants'))

@app.route('/employer/approved_applications')
def employer_approved_applications():
    employer_id = session.get('employer_id')
    if not employer_id:
        flash("Please log in to view this page.", "warning")
        return redirect(url_for('employer_login'))

    try:
        db = mysql.connector.connect(
            host='db.pxxl.pro',
            user='user_deb2e6c5',
            password='8ca5809f66c97bceb7967901c84296e5',
            database='job_portal'
        )
        cursor = db.cursor(dictionary=True)

        # Fetch only approved applications for this employer's jobs
        query = """
            SELECT a.id AS application_id, 
                   a.user_id, 
                   a.job_id, 
                   a.status, 
                   a.applied_at,
                   j.title AS job_title, 
                   j.company, 
                   j.location, 
                   j.job_type,
                   u.name, 
                   u.email
            FROM applications a
            JOIN jobs j ON a.job_id = j.id
            JOIN users u ON a.user_id = u.id
            WHERE a.status = 'accepted'
              AND j.employer_id = %s
            ORDER BY a.applied_at DESC
        """
        cursor.execute(query, (employer_id,))
        approved_apps = cursor.fetchall()

    except mysql.connector.Error as err:
        print("❌ Error fetching approved applications:", err)
        flash("Database error occurred.", "error")
        approved_apps = []

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db' in locals():
            db.close()

    return render_template('employer/approved_applications.html', applications=approved_apps)

import smtplib
from email.mime.text import MIMEText

def send_email(to, subject, body):
    sender = "frontend4mie@gmail.com"
    password = "asvkqvytmqqwfdoh"  # use Gmail App Password, not your normal Gmail password

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, [to], msg.as_string())
    except Exception as e:
        print("Error in send_email:", e)
        raise


import mysql.connector

@app.route('/employer/send_message', methods=['POST'])
def send_message_to_applicant():
    user_id = request.form['user_id']   # Get user_id from the form
    subject = request.form['subject']
    message = request.form['message']

    try:
        # Connect using db_config
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Fetch applicant details from users table
        cursor.execute("SELECT name, email FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()

        if not user:
            flash("Applicant not found.", "danger")
            return redirect(url_for('employer_approved_applications'))

        email = user['email']
        name = user['name']

        # Send email using your helper function
        send_email(to=email, subject=subject, body=message)

        flash(f"Message sent to {name} ({email})", "success")

    except Exception as e:
        print("Error sending email:", e)
        flash("Failed to send message. Please try again.", "danger")

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

    return redirect(url_for('employer_approved_applications'))


@app.route('/employer/logout')
def employer_logout():
    session.clear()  # Remove all user data from session
    flash("You’ve been logged out successfully.", "success")
    return redirect('/')



# 
# 
# 
@app.route('/employer/reschedule/<int:application_id>', methods=['POST'])
def reschedule_interview(application_id):
    new_date = request.form['new_date']

    try:
        db = mysql.connector.connect(
            host='db.pxxl.pro',
            user='user_deb2e6c5',
            password='8ca5809f66c97bceb7967901c84296e5',
            database='job_portal'
        )
        cursor = db.cursor()

        # update applied_at for that application
        cursor.execute("""
            UPDATE applications 
            SET applied_at = %s
            WHERE id = %s
        """, (new_date, application_id))

        db.commit()
        flash('Interview rescheduled successfully.', 'success')

    except mysql.connector.Error as err:
        print("❌ Error updating interview date:", err)
        flash('Failed to reschedule interview.', 'danger')

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db' in locals():
            db.close()

    return redirect(url_for('employer_interview'))

@app.route('/employer/cancel/<int:application_id>', methods=['POST'])
def cancel_interview(application_id):
    db = mysql.connector.connect(host='db.pxxl.pro', user='user_deb2e6c5', password='8ca5809f66c97bceb7967901c84296e5', database='job_portal')
    cursor = db.cursor()
    cursor.execute("UPDATE applications SET status = 'cancelled' WHERE id = %s", (application_id,))
    db.commit()
    cursor.close()
    db.close()
    flash('Interview cancelled.', 'info')
    return redirect(url_for('employer_interview'))

@app.route('/employer/accept/<int:application_id>', methods=['POST'])
def accept_candidate(application_id):
    db = mysql.connector.connect(host='db.pxxl.pro', user='user_deb2e6c5', password='8ca5809f66c97bceb7967901c84296e5', database='job_portal')
    cursor = db.cursor()
    cursor.execute("UPDATE applications SET status = 'accepted' WHERE id = %s", (application_id,))
    db.commit()
    cursor.close()
    db.close()
    flash('Candidate accepted!', 'success')
    return redirect(url_for('employer_interview'))

@app.route('/update_interview_status', methods=['POST'])
def update_interview_status():
    application_id = request.form['application_id']
    status = request.form['status']

    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()

    cursor.execute(
        "UPDATE interviews SET status=%s WHERE applicant_id=%s",
        (status, application_id)
    )
    db.commit()

    cursor.close()
    db.close()

    flash("Interview status updated successfully!", "success")
    return redirect(url_for('employer_interview'))



# ----------------------
# User Routes
# ----------------------

@app.route('/user/')
def user_index():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    
    try:
        db = mysql.connector.connect(
            host='db.pxxl.pro',
            user='user_deb2e6c5',
            password='8ca5809f66c97bceb7967901c84296e5',
            database='job_portal'
        )
        cursor = db.cursor(dictionary=True)

        # Count saved jobs
        cursor.execute("SELECT COUNT(*) AS count FROM saved_jobs WHERE user_id = %s", (user_id,))
        saved_count = cursor.fetchone()['count']

        # Count applied jobs
        cursor.execute("SELECT COUNT(*) AS count FROM applications WHERE user_id = %s", (user_id,))
        applied_count = cursor.fetchone()['count']


        # Get recommended jobs from session
        recommended_jobs = session.get('recommended_jobs', [])
        recommended_count = len(recommended_jobs)

        # Get 3 random recommended jobs (for now: all jobs)
        cursor.execute("""
            SELECT j.*, e.name 
            FROM jobs j
            JOIN employers e ON j.employer_id = e.id
            ORDER BY RAND() LIMIT 3
        """)
        recommended_jobs = cursor.fetchall()

    except mysql.connector.Error as err:
        print("❌ DB Error:", err)
        saved_count = applied_count = 0
        recommended_jobs = []

    finally:
        cursor.close()
        db.close()

    return render_template('user/index.html',
                           saved_count=saved_count,
                           applied_count=applied_count,
                           recommended_jobs=recommended_jobs,
                           recommended_count=recommended_count)


@app.route('/user/feedback')
def user_feedback():
    return render_template('user/feedback.html')

@app.route('/user/job_details')
def user_job_details():
    return render_template('user/job_details.html')

@app.route('/user/logout')
def user_logout():
    session.clear()  # Remove all user data from session
    flash("You’ve been logged out successfully.", "success")
    return redirect('/')


@app.route('/user/notifications')
def user_notifications():
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in to view notifications.", "warning")
        return redirect(url_for('login'))

    try:
        db = mysql.connector.connect(
            host='db.pxxl.pro',
            user='user_deb2e6c5',
            password='8ca5809f66c97bceb7967901c84296e5',
            database='job_portal'
        )
        cursor = db.cursor(dictionary=True)

        cursor.execute("""
            SELECT a.status, a.applied_at, j.title AS job_title
            FROM applications a
            JOIN jobs j ON a.job_id = j.id
            WHERE a.user_id = %s
            ORDER BY a.applied_at DESC
        """, (user_id,))
        notifications = cursor.fetchall()

    except mysql.connector.Error as err:
        print("❌ Error fetching notifications:", err)
        notifications = []

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db' in locals():
            db.close()

    return render_template('user/notifications.html', notifications=notifications)

from datetime import datetime

@app.route("/user/interviews")
def user_interviews():
    if "user_id" not in session:
        return redirect(url_for("user_login"))

    db = mysql.connector.connect(**db_config)
    cursor = db.cursor(dictionary=True)

    query = """
        SELECT i.id, j.title AS job_title, i.interview_date, i.meeting_link, i.status
        FROM interviews i
        JOIN jobs j ON i.job_id = j.id
        WHERE i.applicant_id = %s
        ORDER BY i.interview_date ASC
    """
    cursor.execute(query, (session["user_id"],))
    interviews = cursor.fetchall()

    # Format the datetime for each interview
    for interview in interviews:
        date_value = interview["interview_date"]
        if isinstance(date_value, datetime):
            interview["formatted_date"] = date_value.strftime("%b %d, %Y – %I:%M %p")
        else:
            # Fallback in case it's a string from MySQL
            try:
                dt = datetime.strptime(date_value, "%Y-%m-%d %H:%M:%S")
                interview["formatted_date"] = dt.strftime("%b %d, %Y – %I:%M %p")
            except:
                interview["formatted_date"] = date_value  # leave as is

    cursor.close()
    db.close()

    return render_template("user/interviews.html", interviews=interviews)


@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)


@app.route('/user/profile')
def user_profile():
    if 'user_id' not in session:
        flash("Please log in to access your profile.", "warning")
        return redirect(url_for('login'))

    try:
        db = mysql.connector.connect(
            host='db.pxxl.pro',
            user='user_deb2e6c5',
            password='8ca5809f66c97bceb7967901c84296e5',
            database='job_portal'
        )
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT id, name, email, phone, preference, location, profile_picture FROM users WHERE id = %s", (session['user_id'],))
        user = cursor.fetchone()

    except mysql.connector.Error as err:
        print("❌ Error loading user profile:", err)
        user = None

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db' in locals():
            db.close()

    return render_template('user/profile.html', user=user)


from flask import request, redirect, url_for, flash, session
import mysql.connector
import os



# --- Save Changes (Name, Email, Location, Phone) ---
@app.route('/profile/update_info', methods=['POST'])
def update_profile_info():
    user_id = session.get('user_id')
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    location = request.form.get('location')

    try:
        db = mysql.connector.connect(host="db.pxxl.pro", user="user_deb2e6c5", password="8ca5809f66c97bceb7967901c84296e5", database="job_portal")
        cursor = db.cursor()
        cursor.execute("""
            UPDATE users 
            SET name=%s, email=%s, phone=%s, location=%s 
            WHERE id=%s
        """, (name, email, phone, location, user_id))
        db.commit()
        flash("Profile updated successfully!", "success")
    except Exception as e:
        flash(f"Error updating profile: {e}", "danger")
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('user_profile'))


# --- Save Preferences ---
@app.route('/profile/update_preferences', methods=['POST'])
def update_preferences():
    user_id = session.get('user_id')
    preference = request.form.get('preference')

    try:
        db = mysql.connector.connect(host="db.pxxl.pro", user="user_deb2e6c5", password="8ca5809f66c97bceb7967901c84296e5", database="job_portal")
        cursor = db.cursor()
        cursor.execute("""
            UPDATE users 
            SET preference=%s 
            WHERE id=%s
        """, (preference, user_id))
        db.commit()
        flash("Preferences saved successfully!", "success")
    except Exception as e:
        flash(f"Error saving preferences: {e}", "danger")
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('user_profile'))

import os
from flask import request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "static/uploads/profile_pics"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
def allowed_file(filename):
    print("🔎 Raw filename:", filename)
    if "." not in filename:
        print("❌ No dot in filename")
        return False

    ext = filename.rsplit(".", 1)[1].lower().strip()
    print("🔎 Extracted extension:", ext)
    print("✅ Allowed extensions:", ALLOWED_EXTENSIONS, " | Type:", type(ALLOWED_EXTENSIONS))

    if ext in ALLOWED_EXTENSIONS:
        print("🎉 Extension is valid!")
        return True
    else:
        print("🚨 Extension NOT allowed")
        return False

# ✅ Define allowed extensions globally (case-insensitive check)
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    # Ensure filename has an extension and check case-insensitively
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ✅ Define upload folder inside static
UPLOAD_FOLDER = os.path.join("static", "uploads", "profile_pics")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/update_profile_picture", methods=["POST"])
def update_profile_picture():
    if "profile_picture" not in request.files:
        flash("No file part")
        return redirect(request.referrer)

    file = request.files["profile_picture"]

    if file.filename == "":
        flash("No selected file")
        return redirect(request.referrer)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        # ✅ Save into static/uploads/profile_pics
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(save_path)

        # ✅ Save only filename in DB (not full path)
        db = mysql.connector.connect(
            host="db.pxxl.pro",
            user="user_deb2e6c5",
            password="8ca5809f66c97bceb7967901c84296e5",
            database="job_portal"
        )
        cursor = db.cursor()

        # Example: assuming you store in `users` table
        cursor.execute("UPDATE users SET profile_picture=%s WHERE id=%s", (filename, 1))
        db.commit()
        cursor.close()
        db.close()

        flash("Profile picture updated successfully")
        return redirect(url_for("user/profile"))

    flash("Invalid file type")
    return redirect(request.referrer)
# @app.route('/user/start_job_search', methods=['POST'])
# def start_job_search():
#     data = request.get_json()

#     name = data.get('name')
#     email = data.get('email')
#     skills = data.get('skills')
#     experience = data.get('experience')

#     # Simulate job search logic — this is where you'd use the skills, etc.
#     # For now, just store in session for use in recommended_jobs
#     session['recommended_jobs'] = [
#         {
#             'title': 'Frontend Developer',
#             'company': 'TechNova',
#             'location': 'Remote',
#             'match': '85%',
#             'description': 'Looking for a skilled React developer.'
#         },
#         {
#             'title': 'Data Analyst',
#             'company': 'InsightPro',
#             'location': 'Lagos, Nigeria',
#             'match': '78%',
#             'description': 'Python and SQL required for data insights.'
#         }
#     ]

#     return jsonify({'success': True})


@app.route('/user/start_job_search', methods=['POST'])
def start_job_search():
    data = request.get_json()
    skills = data.get('skills', '').strip()

    if not skills:
        return jsonify({'success': False, 'message': 'No skills provided.'})

    # Clean and normalize skill list
    skill_list = [s.strip().lower() for s in skills.split(',') if s.strip()]

    if not skill_list:
        return jsonify({'success': False, 'message': 'No valid skills found.'})

    try:
        db = mysql.connector.connect(
            host='db.pxxl.pro',
            user='user_deb2e6c5',
            password='8ca5809f66c97bceb7967901c84296e5',
            database='job_portal'
        )
        cursor = db.cursor(dictionary=True)

        # Build dynamic WHERE clause for skill matching
        where_clauses = ' OR '.join(["LOWER(j.skills) LIKE %s" for _ in skill_list])
        params = ['%' + skill + '%' for skill in skill_list]

        query = f"""
            SELECT j.id, j.title, j.company, j.location, j.job_type, j.salary, j.description, j.skills
            FROM jobs j
            WHERE {where_clauses}
            ORDER BY j.created_at DESC
            LIMIT 10
        """

        cursor.execute(query, params)
        jobs = cursor.fetchall()

        recommended_jobs = []
        for job in jobs:
            job_skills = [s.strip().lower() for s in job['skills'].split(',') if s.strip()]
            matched_skills = set(skill_list) & set(job_skills)
            match_percent = int((len(matched_skills) / len(job_skills)) * 100) if job_skills else 0

            recommended_jobs.append({
                'id': job['id'],
                'title': job['title'],
                'company': job['company'],
                'location': job['location'],
                'job_type': job['job_type'],
                'salary': job['salary'],
                'description': job['description'],
                'match': f'{match_percent}%'
            })

        session['recommended_jobs'] = recommended_jobs
        return jsonify({'success': True})

    except mysql.connector.Error as err:
        print("❌ Error executing query:", err)
        return jsonify({'success': False, 'message': 'Database error'})

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db' in locals():
            db.close()


@app.route('/user/recommended_jobs')
def user_recommended_jobs():
    jobs = session.get('recommended_jobs', [])
    return render_template('user/recommended_jobs.html', jobs=jobs)

@app.route('/user/saved_jobs')
def user_saved_jobs():
    user_id = session.get('user_id')  # Ensure user is logged in
    if not user_id:
        flash("Please log in to view saved jobs.", "warning")
        return redirect(url_for('login'))

    try:
        db = mysql.connector.connect(
            host='db.pxxl.pro',
            user='user_deb2e6c5',
            password='8ca5809f66c97bceb7967901c84296e5',
            database='job_portal'
        )
        cursor = db.cursor(dictionary=True)

        query = """
            SELECT jobs.id AS job_id, jobs.title, jobs.company, jobs.location, 85 AS match_score
            FROM saved_jobs
            JOIN jobs ON saved_jobs.job_id = jobs.id
            WHERE saved_jobs.user_id = %s
        """
        cursor.execute(query, (user_id,))
        saved_jobs = cursor.fetchall()

    except mysql.connector.Error as err:
        print(f"❌ Database error: {err}")
        flash("Error loading saved jobs.", "error")
        saved_jobs = []

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db' in locals():
            db.close()

    return render_template('user/saved_jobs.html', saved_jobs=saved_jobs)



@app.route('/user/save_job', methods=['POST'])
def save_job():
    user_id = session.get('user_id')
    job_id = request.json.get('job_id')

    if not user_id or not job_id:
        return jsonify({'success': False, 'message': 'Missing user or job information.'})

    try:
        db = mysql.connector.connect(
            host='db.pxxl.pro',
            user='user_deb2e6c5',
            password='8ca5809f66c97bceb7967901c84296e5',
            database='job_portal'
        )
        cursor = db.cursor()

        # Check if the job has already been saved
        check_query = """
            SELECT 1 FROM saved_jobs
            WHERE user_id = %s AND job_id = %s
            LIMIT 1
        """
        cursor.execute(check_query, (user_id, job_id))
        existing_job = cursor.fetchone()

        if existing_job:
            return jsonify({'success': False, 'message': 'Job already saved!'})

        # Insert into saved_jobs table
        insert_query = """
            INSERT INTO saved_jobs (user_id, job_id)
            VALUES (%s, %s)
        """
        cursor.execute(insert_query, (user_id, job_id))
        db.commit()

        return jsonify({'success': True, 'message': 'Job saved successfully!'})

    except mysql.connector.Error as err:
        print("❌ Error saving job:", err)
        return jsonify({'success': False, 'message': 'Database error'})

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db' in locals():
            db.close()

@app.route('/user/save_job_direct', methods=['POST'])
def save_job_direct():
    user_id = session.get('user_id')
    job_id = request.form.get('job_id')

    if not user_id or not job_id:
        flash("Missing job or user information.", "error")
        return redirect(request.referrer or url_for('user_dashboard'))

    try:
        db = mysql.connector.connect(host='db.pxxl.pro', user='user_deb2e6c5', password='8ca5809f66c97bceb7967901c84296e5', database='job_portal')
        cursor = db.cursor()

        # Check if already saved
        cursor.execute("SELECT 1 FROM saved_jobs WHERE user_id = %s AND job_id = %s", (user_id, job_id))
        if cursor.fetchone():
            flash("Job already saved!", "warning")
        else:
            cursor.execute("INSERT INTO saved_jobs (user_id, job_id) VALUES (%s, %s)", (user_id, job_id))
            db.commit()
            flash("Job saved successfully!", "success")

    except mysql.connector.Error as err:
        print(f"❌ Error saving job: {err}")
        flash("Database error occurred while saving the job.", "error")

    finally:
        cursor.close()
        db.close()

    return redirect(request.referrer or url_for('user_dashboard'))

@app.route('/user/apply_job', methods=['POST'])
def apply_job():
    user_id = session.get('user_id')
    job_id = request.form.get('job_id')

    if not user_id or not job_id:
        flash("Missing job or user information.", "error")
        return redirect(request.referrer or url_for('user_dashboard'))

    try:
        db = mysql.connector.connect(host='db.pxxl.pro', user='user_deb2e6c5', password='8ca5809f66c97bceb7967901c84296e5', database='job_portal')
        cursor = db.cursor()

        # Check if already applied
        cursor.execute("SELECT 1 FROM applications WHERE user_id = %s AND job_id = %s", (user_id, job_id))
        if cursor.fetchone():
            flash("You’ve already applied for this job.", "info")
        else:
            cursor.execute("INSERT INTO applications (user_id, job_id) VALUES (%s, %s)", (user_id, job_id))
            db.commit()
            flash("Application submitted successfully!", "success")

    except mysql.connector.Error as err:
        print(f"❌ Error applying for job: {err}")
        flash("Database error occurred while applying.", "error")

    finally:
        cursor.close()
        db.close()

    return redirect(request.referrer or url_for('user_dashboard'))


@app.route('/job-details/<int:job_id>')
def job_details(job_id):
    try:
        db = mysql.connector.connect(
            host='db.pxxl.pro',
            user='user_deb2e6c5',
            password='8ca5809f66c97bceb7967901c84296e5',
            database='job_portal'
        )
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT * FROM jobs WHERE id = %s", (job_id,))
        job = cursor.fetchone()

        if not job:
            flash("Job not found.", "error")
            return redirect(url_for('user_dashboard'))

    except mysql.connector.Error as err:
        print(f"❌ Error fetching job: {err}")
        flash("Unable to load job details.", "error")
        return redirect(url_for('user_dashboard'))

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db' in locals():
            db.close()

    return render_template('user/job_details.html', job=job)


@app.route('/remove-saved-job/<int:job_id>', methods=['POST'])
def remove_saved_job(job_id):
    try:
        user_id = session.get('user_id')
        if not user_id:
            flash("You must be logged in.", "error")
            return redirect(url_for('login'))

        db = mysql.connector.connect(
            host='db.pxxl.pro',
            user='user_deb2e6c5',
            password='8ca5809f66c97bceb7967901c84296e5',
            database='job_portal'
        )
        cursor = db.cursor()

        cursor.execute("DELETE FROM saved_jobs WHERE user_id = %s AND job_id = %s", (user_id, job_id))
        db.commit()

        flash("Job removed from saved list.", "success")

    except mysql.connector.Error as err:
        print(f"❌ Error removing saved job: {err}")
        flash("Error removing job.", "error")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db' in locals():
            db.close()

    return redirect(url_for('user_saved_jobs'))

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/user/upload_resume', methods=['GET', 'POST'])
def user_upload_resume():
    if request.method == 'POST':
        try:
            file = request.files.get('resumeFile')

            if not file:
                return jsonify({'success': False, 'error': 'No file part in request.'})

            if file and allowed_file(file.filename):
                
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                extracted = extract_resume_data(filepath)

                return jsonify({'success': True, 'data': extracted})

            return jsonify({'success': False, 'error': 'Invalid file type. Upload a .pdf or .docx.'})
        
        except Exception as e:
            print('Upload error:', str(e))  # Log the actual error
            return jsonify({'success': False, 'error': 'An error occurred while processing your file.'})
    
    return render_template('user/upload_resume.html')


def extract_resume_data(path):
    import re, fitz, docx

    text = ""
    if path.endswith('.pdf'):
        with fitz.open(path) as doc:
            for page in doc:
                text += page.get_text()
    elif path.endswith('.docx'):
        doc = docx.Document(path)
        text = '\n'.join([para.text for para in doc.paragraphs])

    lines = [line.strip() for line in text.strip().split("\n") if line.strip()]

    # Name: Skip generic headers like "Curriculum Vitae"
    name = "Unknown"
    for line in lines:
        if line.lower() not in ['curriculum vitae', 'cv']:
            name = line
            break

    # Email
    email_match = re.search(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', text)
    email = email_match.group(0) if email_match else "Not found"

    # Skills
    skills_list = ['Python', 'Flask', 'JavaScript', 'SQL', 'HTML', 'CSS']
    skills_found = [skill for skill in skills_list if skill.lower() in text.lower()]
    
    # Experience
    experience_match = re.search(r'(\d+)\+?\s+years?', text, re.IGNORECASE)
    experience = experience_match.group(0) if experience_match else "Not specified"

    return {
        'name': name,
        'email': email,
        'skills': ', '.join(skills_found) if skills_found else 'Not found',
        'experience': experience
    }




if __name__ == '__main__':
    app.run(debug=True)
