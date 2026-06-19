from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SECRET_KEY'] = 'meditrack_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# ---------------- DATABASE ---------------- #

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    fullname = db.Column(db.String(100), nullable=False)

    email = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    phone = db.Column(
        db.String(15),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        nullable=False
    )


# ---------------- PATIENT MODEL ---------------- #

class Patient(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    fullname = db.Column(
        db.String(100),
        nullable=False
    )

    age = db.Column(
        db.Integer,
        nullable=False
    )

    gender = db.Column(
        db.String(20),
        nullable=False
    )

    disease = db.Column(
        db.String(100),
        nullable=False
    )

    phone = db.Column(
        db.String(15),
        nullable=False
    )


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#---------------------appointment model---------------------#


class Appointment(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    patient_name = db.Column(
        db.String(100),
        nullable=False
    )

    doctor_id = db.Column(
        db.Integer,
        nullable=False
    )

    doctor_name = db.Column(
        db.String(100),
        nullable=False
    )

    appointment_date = db.Column(
        db.String(50),
        nullable=False
    )

    problem = db.Column(
        db.String(200),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="Pending"
    )

    appointment_time = db.Column(
        db.String(50),
        nullable=True
    )




    
# ---------------- HOME ---------------- #

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- REGISTER ---------------- #

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form.get("fullname")
        email = request.form.get("email")
        phone = request.form.get("phone")
        password = request.form.get("password")
        confirm_password = request.form.get(
            "confirm_password"
        )
        role = request.form.get("role")

        if password != confirm_password:
            flash(
                "Passwords do not match!",
                "danger"
            )
            return redirect(url_for("register"))

        existing_email = User.query.filter_by(
            email=email
        ).first()

        if existing_email:
            flash(
                "Email already exists!",
                "danger"
            )
            return redirect(url_for("register"))

        existing_phone = User.query.filter_by(
            phone=phone
        ).first()

        if existing_phone:
            flash(
                "Phone number already exists!",
                "danger"
            )
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(
            password
        )

        user = User(
            fullname=fullname,
            email=email,
            phone=phone,
            password=hashed_password,
            role=role
        )

        db.session.add(user)
        db.session.commit()

        flash(
            "Registration Successful!",
            "success"
        )

        return redirect(url_for("login"))

    return render_template("register.html")


# ---------------- LOGIN ---------------- #

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        login_input = request.form.get(
            "login_input"
        )

        password = request.form.get(
            "password"
        )

        user = User.query.filter(
            (User.email == login_input) |
            (User.phone == login_input)
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):

            login_user(user)

            if user.role == "admin":
                return redirect(
                    url_for(
                        "admin_dashboard"
                    )
                )

            elif user.role == "doctor":
                return redirect(
                    url_for(
                        "doctor_dashboard"
                    )
                )

            else:
                return redirect(
                    url_for(
                        "patient_dashboard"
                    )
                )

        flash(
            "Invalid Credentials!",
            "danger"
        )

    return render_template(
        "login.html"
    )


# ---------------- PATIENT MANAGEMENT ---------------- #

@app.route(
    "/add-patient",
    methods=["GET", "POST"]
)
@login_required
def add_patient():

    if request.method == "POST":

        fullname = request.form.get("fullname")
        age = request.form.get("age")
        gender = request.form.get("gender")
        disease = request.form.get("disease")
        phone = request.form.get("phone")

        patient = Patient(
            fullname=fullname,
            age=age,
            gender=gender,
            disease=disease,
            phone=phone
        )

        db.session.add(patient)
        db.session.commit()

        flash(
            "Patient Added Successfully!",
            "success"
        )

        return redirect(
            url_for("view_patients")
        )

    return render_template(
        "add_patient.html"
    )


@app.route("/patients")
@login_required
def view_patients():

    patients = Patient.query.all()

    return render_template(
        "patients.html",
        patients=patients
    )


@app.route("/delete-patient/<int:id>")
@login_required
def delete_patient(id):

    patient = Patient.query.get_or_404(id)

    db.session.delete(patient)
    db.session.commit()

    flash(
        "Patient Deleted!",
        "success"
    )

    return redirect(
        url_for("view_patients")
    )

# ---------------- APPOINTMENTS ---------------- #

# ---------------- APPOINTMENTS ---------------- #

@app.route(
    "/book-appointment",
    methods=["GET", "POST"]
)
@login_required
def book_appointment():

    # only patient can book
    if current_user.role != "patient":
        return redirect(
            url_for("login")
        )

    doctors = User.query.filter_by(
        role="doctor"
    ).all()

    if request.method == "POST":

        patient_name = current_user.fullname

        doctor_id = request.form.get(
            "doctor_id"
        )

        appointment_date = request.form.get(
            "appointment_date"
        )

        problem = request.form.get(
            "problem"
        )

        doctor = User.query.get(
            int(doctor_id)
        )

        appointment = Appointment(
            patient_name=patient_name,
            doctor_id=doctor.id,
            doctor_name=doctor.fullname,
            appointment_date=appointment_date,
            problem=problem,
            status="Pending"
        )

        db.session.add(
            appointment
        )

        db.session.commit()

        flash(
            "Appointment Booked Successfully!",
            "success"
        )

        return redirect(
            url_for(
                "view_appointments"
            )
        )

    return render_template(
        "book_appointment.html",
        doctors=doctors
    )


# ---------------- VIEW APPOINTMENTS ---------------- #

@app.route("/appointments")
@login_required
def view_appointments():

    # patient
    if current_user.role == "patient":

        appointments = Appointment.query.filter_by(
            patient_name=current_user.fullname
        ).all()

    # doctor
    elif current_user.role == "doctor":

        appointments = Appointment.query.filter_by(
            doctor_name=current_user.fullname
        ).all()

    # admin
    else:

        appointments = Appointment.query.all()

    return render_template(
        "appointments.html",
        appointments=appointments
    )



# ---------------- DOCTOR APPOINTMENTS ---------------- #

@app.route("/doctor-appointments")
@login_required
def doctor_appointments():

    if current_user.role != "doctor":
        return redirect(
            url_for("login")
        )

    appointments = Appointment.query.filter_by(
        doctor_name=current_user.fullname
    ).all()

    return render_template(
        "doctor_appointments.html",
        appointments=appointments
    )


@app.route(
    "/update-appointment/<int:id>",
    methods=["POST"]
)
@login_required
def update_appointment(id):

    appointment = Appointment.query.get_or_404(id)

    action = request.form.get("action")
    time = request.form.get("time")

    if action == "accept":
        appointment.status = "Accepted"
        appointment.appointment_time = time

    elif action == "reject":
        appointment.status = "Rejected"

    db.session.commit()

    return redirect(
        url_for(
            "doctor_appointments"
        )
    )


# ---------------- DASHBOARDS ---------------- #

@app.route("/admin")
@login_required
def admin_dashboard():

    if current_user.role != "admin":
        return redirect(url_for("login"))

    return render_template("admin_dashboard.html")


@app.route("/doctor")
@login_required
def doctor_dashboard():

    if current_user.role != "doctor":
        return redirect(url_for("login"))

    return render_template("doctor_dashboard.html")


@app.route("/patient")
@login_required
def patient_dashboard():

    if current_user.role != "patient":
        return redirect(url_for("login"))

    return render_template("patient_dashboard.html")


# ---------------- LOGOUT ---------------- #

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# ---------------- RUN ---------------- #

if __name__ == "__main__":

    with app.app_context():
        db.create_all()

        admin = User.query.filter_by(
            email="admin@meditrack.com"
        ).first()

        if not admin:

            admin_user = User(
                fullname="Admin",
                email="admin@meditrack.com",
                phone="9999999999",
                password=generate_password_hash(
                    "admin123"
                ),
                role="admin"
            )

            db.session.add(admin_user)
            db.session.commit()

    app.run(debug=True)

