from flask import Flask, jsonify, render_template, redirect, url_for, send_file
from models import db, User, Equation, Function
from forms import (
    CreateEquationForm,
    CreateFunctionForm,
    RegistrationForm,
    LoginForm
)
from flask_migrate import Migrate
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user
)
from flask import Flask, Response, url_for, render_template, request
from flask import Flask, Response, url_for, render_template
import io
import os
import matplotlib
matplotlib.use("Agg")  # server-safe
import matplotlib.pyplot as plt
from flask_login import login_required, current_user


from datetime import date
from werkzeug.security import check_password_hash

import math_engine.equations.logarithmic as log
import math_engine.equations.exponential as ex
import math_engine.functions.functions as func
import sympy as sp
app = Flask(__name__)

# ---------------- CONFIG ----------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expologen.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ExpoLoGen'

db.init_app(app)
migrate = Migrate(app, db)

# ---------------- LOGIN ----------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.password == form.password.data:

            return render_template(
                'login.html',
                form=form,
                error="Invalid username or password"
            )

        login_user(user)
        return redirect(url_for('equations'))

    return render_template('login.html', form=form)

@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("functions"))
    return redirect(url_for("login"))



# ---------------- API ----------------
@app.route('/api/current_user')
def api_current_user():
    if not current_user.is_authenticated:
        return jsonify({"authenticated": False})

    return jsonify({
        "authenticated": True,
        "id": current_user.id,
        "username": current_user.username
    })

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # user = User.query.filter_by(username=form.username.data).first()
        # if user:
        #     return redirect(url_for('login'))

        new_user = User(username=form.username.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()

        return render_template('login.html', form=LoginForm())
    
    

    return render_template('register.html', form=form)

# ---------------- GENERATE ----------------
@login_required
@app.route("/generate/equations", methods=["GET", "POST"])
@login_required
def generate_equations():
    form = CreateEquationForm()
    if form.validate_on_submit():
        for _ in range(form.number.data):
            if form.type.data == 'logarithmic-substitute':
                equation = log.Substitution(form.level.data)
            elif form.type.data == 'logarithmic-mixed':
                equation = log.Mixed_methods(form.level.data)
            elif form.type.data == 'exponential-substitute':
                equation = ex.Substitution(form.level.data)
            elif form.type.data == 'exponential-match':
                equation = ex.Matching_bases(form.level.data)
            elif form.type.data == 'exponential-log':
                equation = ex.Logarithm(form.level.data)

            new_equation = Equation(id_user=current_user.id,
                                    level=form.level.data,
                                    type=form.type.data,
                                    equation=str(equation.get_equation()), 
                                    roots=str(equation.get_roots()), 
                                    steps=str(equation.get_steps()))
            db.session.add(new_equation)
            db.session.commit()
        
        return redirect(url_for('equations'))


    return render_template(
        "generate.html",
        active="generate",
        mode="equations",
        form=form
    )


@login_required
@app.route("/generate/functions", methods=["GET", "POST"])
@login_required
def generate_functions():
    form = CreateFunctionForm()
    if form.validate_on_submit():
        for _ in range(form.number.data):
            if form.type.data == 'exponential':
                function = func.Exponential()
            elif form.type.data == 'logarithmic':
                function = func.Logarithmic()
           

            new_function = Function(id_user=current_user.id,
                                    type=form.type.data,
                                    val_a=int(function.get_coefficients()['val_a']),
                                    val_bn=int(function.get_coefficients()['val_bn']),
                                    val_bd=int(function.get_coefficients()['val_bd']),
                                    val_v=int(function.get_coefficients()['val_v']),
                                    val_n=int(function.get_coefficients()['val_n']),
                                    val_k=int(function.get_coefficients()['val_k']),
                                    val_px=str(sp.sympify(function.get_coefficients()['val_px']).limit_denominator(100000) if not function.get_coefficients()['val_px'] in (None, 'None') else None),
                                    val_py=str(sp.sympify(function.get_coefficients()['val_py']).limit_denominator(100000) if not function.get_coefficients()['val_py'] in (None, 'None') else None))

            db.session.add(new_function)
            db.session.commit()
        
        return redirect(url_for('functions'))


    return render_template(
        "generate.html",
        active="generate",
        mode="functions",
        form=form
    )


# ---------------- EQUATIONS ----------------
@login_required
@app.route("/equations")
def equations():
    today = date.today()

    todays_equations = (
        Equation.query
        .filter(
            Equation.id_user == current_user.id,
            Equation.day_generated >= today
        )
        .order_by(Equation.day_generated.desc())
        .all()
    )

    history_equations = (
        Equation.query
        .filter(
            Equation.id_user == current_user.id,
            Equation.day_generated < today
        )
        .order_by(Equation.day_generated.desc())
        .all()
    )

    print('equations1')

    return render_template(
        "equations.html",
        active="equations",
        todays_equations=todays_equations,
        history_equations=history_equations
    )


# ---------------- FUNCTIONS PAGE ----------------
@login_required
@app.route("/functions")
def functions():
    today = date.today()

    # --- Today's functions ---
    todays_db_functions = (
        Function.query
        .filter(
            Function.id_user == current_user.id,
            Function.day_generated >= today
        )
        .order_by(Function.day_generated.desc())
        .all()
    )

    todays_functions = []
    for f_db in todays_db_functions:
        coefs = {
            'val_a': f_db.val_a,
            'val_bn': f_db.val_bn,
            'val_bd': f_db.val_bd,
            'val_v': f_db.val_v,
            'val_n': f_db.val_n,
            'val_k': f_db.val_k,
            'val_px': sp.sympify(f_db.val_px) if f_db.val_px not in (None, 'None') else None,
            'val_py': sp.sympify(f_db.val_py) if f_db.val_py not in (None, 'None') else None
        }

        if f_db.type == 'logarithmic':
            func_obj = func.Logarithmic(coefs)
        else:
            func_obj = func.Exponential(coefs)

        func_obj.id = f_db.id
        todays_functions.append(func_obj)

    # --- History functions ---
    history_db_functions = (
        Function.query
        .filter(
            Function.id_user == current_user.id,
            Function.day_generated < today
        )
        .order_by(Function.day_generated.desc())
        .all()
    )

    history_functions = []
    for f_db in history_db_functions:
        coefs = {
            'val_a': f_db.val_a,
            'val_bn': f_db.val_bn,
            'val_bd': f_db.val_bd,
            'val_v': f_db.val_v,
            'val_n': f_db.val_n,
            'val_k': f_db.val_k,
            'val_px': sp.sympify(f_db.val_px) if f_db.val_px not in (None, 'None') else None,
            'val_py': sp.sympify(f_db.val_py) if f_db.val_py not in (None, 'None') else None

        }

        if f_db.type == 'logarithmic':
            func_obj = func.Logarithmic(coefs)
        else:
            func_obj = func.Exponential(coefs)

        func_obj.id = f_db.id
        history_functions.append(func_obj)

    return render_template(
        "functions.html",
        active="functions",
        todays_functions=todays_functions,
        history_functions=history_functions
    )


@app.route("/function_details", methods=["GET", "POST"])
@login_required
def function_details():
    id = request.args.get('function_id')
    function = Function.query.get(id)
    coefs = {
        'val_a': function.val_a,
        'val_bn': function.val_bn,
        'val_bd': function.val_bd,
        'val_v': function.val_v,
        'val_n': function.val_n,
        'val_k': function.val_k,
        'val_px': sp.sympify(function.val_px) if function.val_px not in (None, 'None') else None,
        'val_py': sp.sympify(function.val_py) if function.val_py not in (None, 'None') else None}

    if function.type == 'logarithmic':
        func_obj = func.Logarithmic(coefs)
    else:
        func_obj = func.Exponential(coefs)

    func_obj.id = function.id
    
    return render_template("function_details.html", func=func_obj)


@app.route("/function_details/get_img/<int:function_id>", methods=["GET", "POST"])
@login_required
def get_img(function_id):
    id = function_id
    function = Function.query.get(id)
    coefs = {
        'val_a': function.val_a,
        'val_bn': function.val_bn,
        'val_bd': function.val_bd,
        'val_v': function.val_v,
        'val_n': function.val_n,
        'val_k': function.val_k,
        'val_px': sp.sympify(function.val_px) if function.val_px not in (None, 'None') else None,
        'val_py': sp.sympify(function.val_py) if function.val_py not in (None, 'None') else None}

    if function.type == 'logarithmic':
        func_obj = func.Logarithmic(coefs)
    else:
        func_obj = func.Exponential(coefs)

    img = func_obj.plot()

    return send_file(img, mimetype="image/png")

# ---------------- LOGOUT ----------------
@login_required
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

with app.app_context():
    db.create_all()

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
