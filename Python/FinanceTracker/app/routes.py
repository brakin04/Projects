from flask import Blueprint, render_template, current_app, session, request, redirect, url_for, flash
from .models import db, User, Expense, Income, Budget, Category
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from app.logging_config import logger, savedLevel
from sqlalchemy import func, select
import markdown
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import logging
import requests
import os

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    logger.debug(f"Home function entered in routes.py Session ID: {session.get('session_id')}")
    logger.info("Home page requested")

    # get README.md content
    # readme_file = get_file_content(os.getcwd() + '/README.md')

    logger.debug("Home function exited in routes.py")
    return render_template('home.html')#, content=readme_file)


security_questions = ["What is your hometown?", "What was the name of your first pet?", "What is your mother's maiden name?"]


# ------------------------------
@bp.route('/register', methods=['GET', 'POST'])
def register():
    logger.debug(f"Register function entered in routes.py method: {request.method}")
    logger.info("Registration attempt initiated")
    logger.debug(f"Session ID: {session.get('session_id')}")
    if request.method == 'POST':
        email = request.form['email']
        nickname = request.form['nickname']
        password = request.form['password']
        answer1 = request.form['answer1']
        answer2 = request.form['answer2']
        answer3 = request.form['answer3']
        # role = request.form.get('role') or 'user'

        # Check for existing email and nickname
        if User.query.filter_by(email=email).first():
            logger.warning("Registration failed: Email already taken")
            logger.debug("Register function exited with failure in routes.py")
            flash("Email already taken!", "warning")
            return redirect(url_for('main.register'))

        if User.query.filter_by(nickname=nickname).first():
            logger.warning("Registration failed: Nickname already taken")
            logger.debug("Register function exited with failure in routes.py")
            flash("Nickname already taken!", "warning")
            return redirect(url_for('main.register'))

        # Hash password, add user data to db
        hashed_password = generate_password_hash(password)
        user = User(email=email, nickname=nickname, password=hashed_password, security_answers=[answer1, answer2, answer3])#, role=role)
        db.session.add(user)
        db.session.commit()
        logger.debug(f"User {nickname} registered in database")
        logger.info(f"New user registered: {nickname}")

        flash("Registration successful! Please login.", "success")
        logger.debug("Register function exited with success in routes.py")
        return redirect(url_for('main.login'))
    
    logger.debug("Register function exited from GET request in routes.py")
    return render_template('register.html', security_questions=security_questions)


# ------------------------------
@bp.route('/login', methods=['GET', 'POST'])
def login():
    logger.debug(f"Login function entered in routes.py method: {request.method}")
    if request.method == 'POST':
        logger.info("Login attempt")
        logger.debug(f"Session ID: {session.get('session_id')}")
        identity = request.form['identity']
        password = request.form['password']

        # Search for user using nickname / email
        user = User.query.filter((User.email == identity) | (User.nickname == identity)).first()
        logger.debug(f"User found: {user.nickname if user else 'None'}")

        # Make sure the password matches
        if user and check_password_hash(user.password, password):
            login_user(user)
            logger.info(f"Authentication success for user: {user.nickname}")
            flash("Welcome back!", "success")
            logger.debug("Login function exited with success as user in routes.py")
            return redirect(url_for('main.dashboard'))

        else:
            logger.warning(f"Authentication failure for: {identity}")
            flash("Invalid credentials, try again.", "warning")
            logger.debug("Login function exited with authentication failure in routes.py")
            return redirect(url_for('main.login'))

    logger.debug("Login function exited from GET request in routes.py")
    return render_template('login.html')


#-------------------------------
@bp.route('/login/security', methods=['GET', 'POST'])
def login_security():
    logger.debug(f"Login security function entered in routes.py method: {request.method}")
    if request.method == 'POST':
        email = request.form['email']
        nickname = request.form['nickname']
        security_question = request.form['security_question']
        security_answer = request.form['security_answer']

        # Search for user info matching what was given
        user = User.query.filter_by(nickname=nickname, email=email).first()
        logger.debug(f"User found for security question: {user.nickname if user else 'None'}")
        
        # Check security question answer
        if user and user.security_answers[security_questions.index(security_question)].lower() == security_answer.lower():
            login_user(user)
            logger.info(f"Security question authentication success for user: {user.nickname}")
            flash("Welcome back!", "success")
            logger.debug("Login security function exited with success as user in routes.py")
            return redirect(url_for('main.dashboard'))
        else:
            logger.warning(f"Security question authentication failure for: {nickname} email: {email}")
            flash("Invalid credentials", "warning")
            logger.debug("Login security function exited with authentication failure in routes.py")
            return redirect(url_for('main.login_security'))

    logger.debug("Login security function exited from GET request in routes.py")
    return render_template('login_security.html', security_questions=security_questions)


# ------------------------------
@bp.route('/logout')
@login_required
def logout():
    logger.debug("Logout function entered in routes.py")
    logger.info(f"User logged out: {current_user.nickname}")
    logout_user()
    flash("You have been logged out.", "info")
    logger.debug("Logout function exited in routes.py")

    return redirect(url_for('main.login'))


#-------------------------------
@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    logger.debug(f"Profile function entered in routes.py with method: {request.method}")

    if request.method == 'POST':
        email = request.form['email']
        nickname = request.form['nickname']
        new_pw = request.form['new_password']
        confirm_pw = request.form['confirm_password']

        # Check for email or nickname conflicts
        if email != current_user.email:
            if User.query.filter(User.email == email, User.id != current_user.id).first():
                logger.warning("Profile update failed: Email already taken")
                flash("Email already taken!", "warning")
                return redirect(url_for('main.profile'))

        if nickname != current_user.nickname:
            if User.query.filter(User.nickname == nickname, User.id != current_user.id).first():
                logger.warning(f"Profile update failed: Nickname \"{nickname}\" already taken")
                flash("Nickname already taken!", "warning")
                return redirect(url_for('main.profile'))
            
        # Check if user wants to change password
        if new_pw and confirm_pw:
            if new_pw == confirm_pw:
                current_user.password_hash = generate_password_hash(new_pw)
                logger.info(f"Password updated for user: {current_user.nickname}")
            else:
                flash("Passwords do not match!", "danger")
                return redirect(url_for('main.profile'))
        elif new_pw and not confirm_pw:
            logger.debug("No confirm password provided")
            flash("Please confirm your new password!", "warning")
            return redirect(url_for('main.profile'))

        # Update user info
        current_user.email = email
        current_user.nickname = nickname
        db.session.commit()
        logger.info(f"Profile updated for user: {current_user.nickname}")
        flash("Profile updated successfully!", "success")
        logger.debug("Profile function exited with success in routes.py")
        return redirect(url_for('main.profile'))
    
    # GET request handling
    userInfo = {'email': current_user.email, 'nickname': current_user.nickname}
    return render_template('profile.html', userInfo=userInfo)


###
### Dashboard functions
###

dashboard_expenses = {}
dashboard_incomes = {}
dashboard_comparatives = {}


# ------------------------------
@bp.route('/dashboard')
@login_required
def dashboard():
    logger.debug("Dashboard function used in routes.py")
    timeframes = ["None", "1 day", "3 days", "5 days", "7 days", "1 month", "6 months", "1 year", "All time"]
    return render_template('dashboard.html', expenses=dashboard_expenses, incomes=dashboard_incomes, 
                           compare=dashboard_comparatives, timeframes=timeframes)


#-------------------------------
@bp.route('/dashboard/expenses/filter', methods=['POST'])
@login_required
def filter_dashboard_expenses():
    logger.debug("Filter dashboard expenses function entered in routes.py")

    # Clear previous filters
    dashboard_expenses.clear()

    if 'clear' in request.form:
        logger.debug("Clearing expense filters as per request")
        return redirect(url_for('main.dashboard'))

    # Add filters to dictionary
    timeframe = request.form['timeframe']
    form_start_date = request.form['start_date']
    form_end_date = request.form['end_date']

    timeAnswers = check_dates(timeframe=timeframe, form_start_date=form_start_date, 
                              form_end_date=form_end_date, for_what="expenses")

    expenses = timeAnswers[3]
    total = 0
    if expenses:
        total = expenses.with_entities(func.sum(Expense.amount)).scalar() or 0
        # count = expenses.with_entities(func.count(Expense.amount)).scalar() or 0
        category_totals = expenses.with_entities(Expense.category, func.sum(Expense.amount)).group_by(Expense.category).all()

    # Line graph data
    line_expenses = {}
    current_date = timeAnswers[0]
    end_date = timeAnswers[1]
    if current_date:
        line_expenses[current_date.strftime('%Y-%m-%d')] = 0
    if end_date:
        line_expenses[end_date.strftime('%Y-%m-%d')] = 0

    # Loop through each date in the range
    if current_date and end_date:
        while current_date <= end_date:
            line_expenses[current_date.strftime('%Y-%m-%d')] = 0
            current_date += timedelta(days=1)
    
    # Add values from each expense date
    if expenses:
        for expense in expenses:
            date_key = expense.date.strftime('%Y-%m-%d')
            line_expenses[date_key] = line_expenses.get(date_key, 0) + expense.amount

    category_breakdown = {}
    if total > 0:
        for category, amount in category_totals:
            percentage = (amount / total) * 100
            category_breakdown[category] = {'total': amount, 'percentage': round(percentage, 2)}

    # Add em to map
    dashboard_expenses['timeframe'] = timeframe
    dashboard_expenses['total'] = total
    # dashboard_expenses['count'] = count
    dashboard_expenses['category_chart'] = get_pie_chart(data=category_breakdown, type="Expenses")
    dashboard_expenses['line_chart'] = get_line_graph(data=line_expenses, type="Expenses")

    return redirect(url_for('main.dashboard'))

    
#-------------------------------
@bp.route('/dashboard/incomes/filter', methods=['POST'])
@login_required
def filter_dashboard_incomes():
    logger.debug("Filter dashboard incomes function entered in routes.py")

    # Clear previous filters
    dashboard_incomes.clear()

    if 'clear' in request.form:
        logger.debug("Clearing income filters as per request")
        return redirect(url_for('main.dashboard'))

    # Get filters
    timeframe = request.form['timeframe']
    form_start_date = request.form['start_date']
    form_end_date = request.form['end_date']

    timeAnswers = check_dates(timeframe=timeframe, form_start_date=form_start_date, 
                              form_end_date=form_end_date, for_what="incomes")

    # Add values from each income date
    incomes = timeAnswers[2]
    total = 0
    if incomes:
        total = incomes.with_entities(func.sum(Income.amount)).scalar() or 0
        # count = incomes.with_entities(func.count(Income.amount)).scalar() or 0
        category_totals = incomes.with_entities(Income.category, func.sum(Income.amount)).group_by(Income.category).all()
        
    # Line graph data
    line_incomes = {}
    current_date = timeAnswers[0]
    end_date = timeAnswers[1]
    if current_date:
        line_incomes[current_date.strftime('%Y-%m-%d')] = 0
    if end_date:
        line_incomes[end_date.strftime('%Y-%m-%d')] = 0

    # Loop through each date in the range
    if current_date and end_date:
        while current_date <= end_date:
            line_incomes[current_date.strftime('%Y-%m-%d')] = 0
            current_date += timedelta(days=1)

    # Add values from each income date
    if incomes:
        for income in incomes:
            date_key = income.date.strftime('%Y-%m-%d')
            line_incomes[date_key] = line_incomes.get(date_key, 0) + income.amount

    # Pie chart breakdown
    category_breakdown = {}
    if total > 0:
        for category, amount in category_totals:
            percentage = (amount / total) * 100
            category_breakdown[category] = {'total': amount, 'percentage': round(percentage, 2)}

    # Add em to map
    dashboard_incomes['total'] = total
    dashboard_incomes['timeframe'] = timeframe
    # dashboard_incomes['count'] = count
    dashboard_incomes['category_chart'] = get_pie_chart(data=category_breakdown, type="Incomes")
    dashboard_incomes['line_chart'] = get_line_graph(data=line_incomes, type="Incomes")

    return redirect(url_for('main.dashboard'))


#-------------------------------
@bp.route('/dashboard/compare/filter', methods=['POST'])
@login_required
def filter_dashboard_comparatives():
    logger.debug("Filter dashboard comparatives function entered in routes.py")

    dashboard_comparatives.clear()

    if 'clear' in request.form:
        logger.debug("Clearing income filters as per request")
        return redirect(url_for('main.dashboard'))

    # Add filters to dictionary
    timeframe = request.form['timeframe']
    form_start_date = request.form['start_date']
    form_end_date = request.form['end_date']

    timeAnswers = check_dates(timeframe=timeframe, form_start_date=form_start_date, 
                              form_end_date=form_end_date, for_what="compares")

    incomes = timeAnswers[2]
    expenses = timeAnswers[3]

    incTotal = 0
    expTotal = 0
    if incomes:
        incTotal = incomes.with_entities(func.sum(Income.amount)).scalar() or 0
    if expenses:
        expTotal = expenses.with_entities(func.sum(Expense.amount)).scalar() or 0

    # Add em to map
    profit = incTotal - expTotal
    dashboard_comparatives['profit'] = profit
    dashboard_comparatives['timeframe'] = timeframe

    return redirect(url_for('main.dashboard'))


###
### Expense routes
###

expense_filters = {}
expense_places = ""


# ------------------------------
@bp.route('/expenses')
@login_required
def expenses():
    logger.debug("Expenses function entered in routes.py")
    expenses = Expense.query.filter_by(user_id=current_user.id)
    logger.debug(f"Expenses filtered by user ID")

    # Apply filters to the expenses query
    if 'start_date' in expense_filters:
        expenses = expenses.filter(Expense.date >= expense_filters['start_date'])
    if 'end_date' in expense_filters:
        expenses = expenses.filter(Expense.date <= expense_filters['end_date'])
    if 'min_amount' in expense_filters:
        expenses = expenses.filter(Expense.amount >= expense_filters['min_amount'])
    if 'max_amount' in expense_filters:
        expenses = expenses.filter(Expense.amount <= expense_filters['max_amount'])
    if 'categories' in expense_filters:
        lower_categories = [cat.lower() for cat in expense_filters['categories']]
        expenses = expenses.filter(func.lower(Expense.category).in_(lower_categories))
    if 'where' in expense_filters:
        lower_places = [place.lower() for place in expense_filters['where']]
        expenses = expenses.filter(func.lower(Expense.where).in_(lower_places))

    logger.debug(f"Expenses filtered with current filters: {expense_filters}")

    # Info about expenses
    total = expenses.with_entities(func.sum(Expense.amount)).scalar() or 0
    avg = expenses.with_entities(func.avg(Expense.amount)).scalar() or 0
    avg = round(avg, 2)

    expenses = expenses.order_by(Expense.date.desc())

    logger.debug("Expenses function exited in routes.py")
    return render_template('expenses.html', expenses=expenses, total=total, avg=avg)


#-------------------------------
@bp.route('/expenses/filter', methods=['POST', 'GET'])
@login_required
def filter_expenses():
    logger.debug(f"filter_expenses function entered in routes.py method: {request.method}")
    global expense_places

    if request.method == 'POST':

        # Clear previous filters
        expense_filters.clear()
        expense_places = ""

        if 'clear' in request.form:
            logger.debug("Clearing expense filters as per request")
            return redirect(url_for('main.filter_expenses'))

        # Add filters to dictionary
        if request.form['start_date']:
            start_date = request.form['start_date']
            expense_filters['start_date'] = datetime.strptime(start_date, '%Y-%m-%d').date()
        if request.form['end_date']:
            end_date = request.form['end_date']
            expense_filters['end_date'] = datetime.strptime(end_date, '%Y-%m-%d').date()
        if request.form['min_amount']:
            min_amount = request.form['min_amount']
            expense_filters['min_amount'] = float(min_amount)
        if request.form['max_amount']:
            max_amount = request.form['max_amount']
            expense_filters['max_amount'] = float(max_amount)

        # Split places & categories
        if request.form['where']:
            # Save it to be used as default value
            expense_places = request.form['where'] 

            where = request.form['where'] + ","  # to ensure split even if empty
            places = where.split(',')
            places = [place.strip().capitalize() for place in places]
            expense_filters['where'] = places

        if request.form.getlist('categories'):
            # Save it to be used as default value
            categories = request.form.getlist('categories')
            categories = [cat.strip() for cat in categories]
            expense_filters['categories'] = categories

        logger.debug(f"filter_expenses (POST) in routes.py applied filters: {expense_filters}")
        return redirect(url_for('main.expenses'))

    categories = get_all_categories(type="expense")
    logger.debug(f"filter_expenses in routes.py exited (GET) with filters: {expense_filters}")
    return render_template('filter_expenses.html', filters=expense_filters, 
                           places=expense_places , categories=categories)

#-------------------------------
@bp.route('/expenses/edit', methods=['GET', 'POST'])
@login_required
def edit_expense():
    logger.debug(f"edit_expense function entered in routes.py method: {request.method}")
    expense_id = request.args.get('expense_id')
    if request.method == 'POST':
        # Process form data and update expense
        date = request.form['date']
        amount = request.form['amount']
        where = request.form['where']
        category = request.form['category']
        description = request.form.get('description')
        # recurring = bool(request.form.get('recurring'))

        # Put date in valid format so SQLite will accept it
        pyDate = datetime.strptime(date, '%Y-%m-%d').date()

        expense_to_update = Expense.query.get(expense_id)
        
        if expense_to_update:
            # Update fields
            expense_to_update.date = pyDate
            expense_to_update.amount=amount
            expense_to_update.where=where.capitalize()
            expense_to_update.category=category.capitalize()
            expense_to_update.description=description
            # expense_to_update.recurring=recurring
            
            db.session.commit()
            flash("Expense changed successfully!", "success")
            logger.debug("add_expense function (POST) exited with success in routes.py")
        else:
            flash("Expense not found!", "failure")
            logger.info("edit_expense function (POST) exited with failure in routes.py")

        return redirect(url_for('main.expenses'))

    expense = Expense.query.get(expense_id)
    categories = get_all_categories(type="expense")
    logger.debug("edit_expense function exited from GET request in routes.py")
    return render_template('edit_expense.html', expense=expense, categories=categories)


# ------------------------------
@bp.route('/expense/add', methods=['GET', 'POST'])
@login_required
def add_expense():
    logger.debug(f"add_expense function entered in routes.py method: {request.method}")
    if request.method == 'POST':
        logger.info(f"Adding expense for user: {current_user.nickname}")
        date = request.form['date']
        amount = request.form['amount']
        where = request.form['where'].capitalize()
        category = request.form['category'].capitalize()
        description = request.form.get('description')
        # recurring = bool(request.form.get('recurring'))

        # Put date in valid format so SQLite will accept it
        pyDate = datetime.strptime(date, '%Y-%m-%d').date()

        expense = Expense(date=pyDate, amount=amount, where=where, category=category,
                          description=description, recurring=False, user_id=current_user.id)
        db.session.add(expense)
        db.session.commit()
        flash("Expense added successfully!", "success")
        logger.debug("add_expense function (POST) exited with success in routes.py")
        return redirect(url_for('main.expenses'))
    
    categories = get_all_categories(type="expense")
    logger.debug("add_expense function exited from GET request in routes.py")
    return render_template('add_expense.html', categories=categories)


# ------------------------------
@bp.route('/expense/delete', methods=['GET', 'POST'])
@login_required
def delete_expense():
    logger.debug(f"delete_expense function entered in routes.py method: {request.method}")
    expense_id = request.args.get('expense_id')
    if request.method == 'POST':
        expense_to_delete = Expense.query.get(expense_id)
        if expense_to_delete:
            db.session.delete(expense_to_delete)
            db.session.commit()
            flash("Expense deleted successfully!", "success")
            logger.debug("delete_expense function (POST) exited with success in routes.py")
        else:   
            flash("Expense not found!", "failure")
            logger.info("delete_expense function (POST) exited with failure in routes.py")
        return redirect(url_for('main.expenses'))
    
    expense = Expense.query.get(expense_id)
    logger.debug("delete_expense function exited from GET request in routes.py")
    return render_template('delete_expense.html', expense=expense)

###
### Income routes    
###

income_filters = {}
income_sources = ""


# ------------------------------
@bp.route('/incomes')
@login_required
def incomes():
    logger.debug("Incomes function entered in routes.py")
    incomes = Income.query.filter_by(user_id=current_user.id)
    logger.debug(f"Incomes filtered by user ID")

    # Apply filters to the expenses query
    if 'start_date' in income_filters:
        incomes = incomes.filter(Income.date >= income_filters['start_date'])
    if 'end_date' in income_filters:
        incomes = incomes.filter(Income.date <= income_filters['end_date'])
    if 'min_amount' in income_filters:
        incomes = incomes.filter(Income.amount >= income_filters['min_amount'])
    if 'max_amount' in income_filters:
        incomes = incomes.filter(Income.amount <= income_filters['max_amount'])
    if 'source' in income_filters:
        lower_sources = [source.lower() for source in income_filters['source']]
        incomes = incomes.filter(func.lower(Income.source).in_(lower_sources))
    if 'categories' in income_filters:
        lower_categories = [cat.lower() for cat in income_filters['categories']]
        incomes = incomes.filter(func.lower(Income.category).in_(lower_categories))
    logger.debug(f"Incomes filtered with current filters: {income_filters}")

    # Info about incomes
    total = incomes.with_entities(func.sum(Income.amount)).scalar() or 0
    avg = incomes.with_entities(func.avg(Income.amount)).scalar() or 0
    avg = round(avg, 2)

    incomes = incomes.order_by(Income.date.desc())

    logger.debug("Incomes function exited in routes.py")
    return render_template('incomes.html', incomes=incomes, total=total, avg=avg)


#-------------------------------
@bp.route('/incomes/filter', methods=['GET', 'POST'])
@login_required
def filter_incomes():
    logger.debug(f"filter_incomes function entered in routes.py method: {request.method}")
    global income_sources

    if request.method == 'POST':

        # Clear previous filters
        income_filters.clear()
        income_sources = ""
        
        if 'clear' in request.form:
            logger.debug("Clearing income filters as per request")
            return redirect(url_for('main.filter_incomes'))
        
        # Add filters to dictionary
        if request.form['start_date']:
            start_date = request.form['start_date']
            income_filters['start_date'] = datetime.strptime(start_date, '%Y-%m-%d').date()
        if request.form['end_date']:
            end_date = request.form['end_date']
            income_filters['end_date'] = datetime.strptime(end_date, '%Y-%m-%d').date()
        if request.form['min_amount']:
            min_amount = request.form['min_amount']
            income_filters['min_amount'] = float(min_amount)
        if request.form['max_amount']:
            max_amount = request.form['max_amount']
            income_filters['max_amount'] = float(max_amount)

        # Split sources & categories
        if request.form['source']:
            # Save to be used as default value
            income_sources = request.form['source']

            source = request.form['source'] + ","
            places = source.split(',')
            places = [place.strip().capitalize() for place in places]
            income_filters['source'] = places

        if request.form.getlist('categories'):
            # Save to be used as default value
            categories = request.form.getlist('categories')
            categories = [cat.strip() for cat in categories]
            income_filters['categories'] = categories

        logger.debug(f"filter_incomes (POST) in routes.py applied filters: {income_filters}")
        return redirect(url_for('main.incomes'))
    
    categories = get_all_categories(type="income")
    logger.debug(f"filter_incomes (GET) in routes.py exited with filters: {income_filters}")
    return render_template('filter_incomes.html', filters=income_filters, 
                           sources=income_sources, categories=categories)


#-------------------------------
@bp.route('/incomes/edit', methods=['GET', 'POST'])
@login_required
def edit_income():
    logger.debug(f"edit_income function entered in routes.py method: {request.method}")
    income_id = request.args.get('income_id')
    if request.method == 'POST':

        # Process form data and update income
        date = request.form['date']
        amount = request.form['amount']
        source = request.form['source']
        category = request.form['category']
        description = request.form.get('description')
        # recurring = bool(request.form.get('recurring'))

        # Put date in valid format so SQLite will accept it
        pyDate = datetime.strptime(date, '%Y-%m-%d').date()

        income_to_update = Income.query.get(income_id)
        
        if income_to_update:
            # Update fields
            income_to_update.date = pyDate
            income_to_update.amount = amount
            income_to_update.source = source.capitalize()
            income_to_update.category = category
            income_to_update.description = description
            # income_to_update.recurring=recurring
            
            db.session.commit()
            flash("Income changed successfully!", "success")
            logger.debug("add_income function (POST) exited with success in routes.py")
        else:
            flash("Income not found!", "failure")
            logger.warning(f"edit_income function (POST) exited with failure in routes.py for Income ID: {income_id}")
        return redirect(url_for('main.incomes'))
    
    income = Income.query.get(income_id)
    categories = get_all_categories(type="income")
    logger.debug("edit_income function exited from GET request in routes.py")
    return render_template('edit_income.html', income=income, categories=categories)


# ------------------------------
@bp.route('/income/add', methods=['GET', 'POST'])
@login_required
def add_income():
    logger.debug(f"add_income function entered in routes.py method: {request.method}")
    if request.method == 'POST':
        logger.info(f"Adding income for user: {current_user.nickname}")
        date = request.form['date']
        amount = request.form['amount']
        category = request.form['category']
        source = request.form['source']
        description = request.form.get('description')
        # recurring = bool(request.form.get('recurring'))

        # Put date in valid format so SQLite will accept it
        pyDate = datetime.strptime(date, '%Y-%m-%d').date()

        income = Income(date=pyDate, amount=amount, source=source.capitalize(),
                        description=description, category=category, recurring=False, user_id=current_user.id)
        db.session.add(income)
        db.session.commit()
        flash("Income added successfully!", "success")
        logger.info(f"Income added successfully for user: {current_user.nickname}")
        logger.debug("add_income function exited with success in routes.py")
        return redirect(url_for('main.incomes'))
    
    categories = get_all_categories(type="income")
    logger.debug("add_income function exited from GET request in routes.py")
    return render_template('add_income.html', categories=categories)

    
# ------------------------------
@bp.route('/income/delete', methods=['GET', 'POST'])
@login_required
def delete_income():
    logger.debug(f"delete_income function entered in routes.py method: {request.method}")
    income_id = request.args.get('income_id')

    if request.method == 'POST':
        income_to_delete = Income.query.get(income_id)

        if income_to_delete:
            db.session.delete(income_to_delete)
            db.session.commit()
            flash("Income deleted successfully!", "success")
            logger.info(f"Income deleted successfully for user: {current_user.nickname}")
            logger.debug("delete_income function exited with success in routes.py")
        else:   
            flash("Income not found!", "failure")
            logger.warning(f"delete_income function (POST) exited with failure in routes.py for Income ID: {income_id}")
        return redirect(url_for('main.incomes'))
    
    income = Income.query.get(income_id)
    return render_template('delete_income.html', income=income)


###
### Budget routes
###


#-------------------------------
@bp.route('/budget')
@login_required
def budget():
    logger.debug("budget function entered in routes.py")
    budgets = Budget.query.filter_by(user_id=current_user.id)

    total = budgets.with_entities(func.sum(Budget.amount)).scalar() or 0
    budgets = budgets.order_by(Budget.amount.desc())

    byCategory = {}
    # Make pie chart data
    if total > 0:
        for (category, amount) in budgets.with_entities(Budget.category, Budget.amount).all():
            byCategory[category] = {'total': amount, 'percentage': round((amount / total) * 100, 2)}
    
    budget_chart = get_pie_chart(data=byCategory, type="Budgets")
    logger.debug("budget function exited in routes.py")
    return render_template('budget.html', budgets=budgets, total=total, budget_chart=budget_chart)


#-------------------------------
@bp.route('/budget/edit', methods=['GET', 'POST'])
@login_required
def edit_budget():
    logger.debug(f"edit_budget function entered in routes.py method: {request.method}")
    budget_id = request.args.get('budget_id')
    budget_to_update = Budget.query.get(budget_id)

    if request.method == 'POST':
        # Process form data and update budget
        new_amount = request.form['amount']
        new_category = request.form['category'].capitalize()
        
        if budget_to_update:

            # Check for a budget with this category already
            existing_budget = Budget.query.filter(Budget.category == new_category, 
                                                    Budget.user_id == current_user.id,
                                                    Budget.id != budget_to_update.id).first()
            
            if existing_budget:
                logger.info(f"Budget for {new_category} already existes for user {current_user.nickname}")
                flash(f"Budget already exists for {new_category}", "warning")
                logger.debug(f"existing: {existing_budget.id} new: {budget_to_update.id}")
                categories = get_all_categories(type="expense")
                logger.info("edit_budget (POST) exited with failure in routes.py")
                return render_template('edit_budget.html', budget=budget_to_update, categories=categories)
            
            # Update fields
            budget_to_update.amount=new_amount
            budget_to_update.category=new_category
            
            db.session.commit()
            flash("Budget changed successfully!", "success")
            logger.debug("edit_budget function (POST) exited with success in routes.py")  
        else:
            flash("Budget not found!", "failure")
            logger.warning(f"edit_budget function (POST) exited with failure in routes.py for Budget ID: {budget_id}")
        return redirect(url_for('main.budget'))
    
    categories = get_all_categories(type="expense")
    logger.debug("edit_budget function exited from GET request in routes.py")
    return render_template('edit_budget.html', budget=budget_to_update, categories=categories)


# ------------------------------
@bp.route('/budget/add', methods=['GET', 'POST'])
@login_required
def add_budget():
    logger.debug(f"add_budget function entered in routes.py method: {request.method}")

    if request.method == 'POST':
        logger.info(f"Adding budget for user: {current_user.nickname}")

        new_amount = request.form['amount']
        new_category = request.form['category'].capitalize()

        # Check if category already has a budget
        existing_budget = Budget.query.filter(Budget.category == new_category, Budget.user_id == current_user.id).first()
            
        if existing_budget:
            logger.info(f"Budget for {new_category} already existes for user {current_user.nickname}")
            flash(f"Budget already exists for {new_category}. Edit it instead.", "warning")
            logger.debug(f"existing: {existing_budget.id}")
            categories = get_all_categories(type="expense")
            logger.info("add_budget (POST) exited with failure in routes.py")
            return render_template('add_budget.html', categories=categories)

        # Add the budget to db
        budget = Budget(amount=new_amount, category=new_category, user_id=current_user.id)
        db.session.add(budget)
        db.session.commit()
        flash("Budget added successfully!", "success")
        logger.info(f"Budget added successfully for user: {current_user.nickname}")
        logger.debug("add_budget function exited with success in routes.py")
        return redirect(url_for('main.budget'))

    categories = get_all_categories(type="expense")
    logger.debug("add_budget function exited from GET request in routes.py")
    return render_template('add_budget.html', categories=categories)


#-------------------------------
@bp.route('/budget/delete', methods=['GET', 'POST'])
@login_required
def delete_budget():
    logger.debug(f"delete_budget function entered in routes.py method: {request.method}")
    budget_id = request.args.get('budget_id')

    if request.method == 'POST':
        budget_to_delete = Budget.query.get(budget_id)
        if budget_to_delete:
            db.session.delete(budget_to_delete)
            db.session.commit()
            flash("Budget deleted successfully!", "success")
            logger.info(f"Budget deleted successfully for user: {current_user.nickname}")
            logger.debug("delete_budget function exited with success in routes.py")
        else:
            flash("Budget not found!", "failure")
            logger.warning(f"delete_budget function (POST) exited with failure in routes.py for Budget ID: {budget_id}")
        return redirect(url_for('main.budget'))
    
    budget = Budget.query.get(budget_id)
    logger.debug("delete_budget function exited from GET request in routes.py")
    return render_template('delete_budget.html', budget=budget)


###
### Category Routes
###


#-------------------------------
@bp.route('/categories', methods=['GET'])
@login_required
def categories():
    logger.debug("Categories function entered in routes.py")
    type_requested = request.args.get('types')
    categories = get_all_categories(type=type_requested)
    logger.debug("Categories function exited in routes.py")
    return render_template('categories.html', categories=categories)


#-------------------------------
@bp.route('/category/add', methods=['GET', 'POST'])
@login_required
def add_category():
    logger.debug(f"add_category function entered in routes.py method: {request.method}")

    if request.method == 'POST':
        new_category = request.form['category'].strip().capitalize()  
        description = request.form['description']
        type = request.form['type']

        # Check if the category exists already for this user
        exists = Category.query.filter_by(name=new_category, user_id=current_user.id, type=type.capitalize()).first()
        
        if exists:
            logger.info(f"Category '{new_category}' already exists for this type for user: {current_user.nickname}")
            flash(f"Category '{new_category}' already exists for this type!", "info")
            logger.debug("add_category function exited with failure in routes.py")
        else:
            # Add it to db
            category = Category(name=new_category, description=description, type=type.capitalize(), user_id=current_user.id)
            db.session.add(category)
            db.session.commit()
            flash(f"Category '{category.name}' added successfully!", "success")
            logger.info(f"Category '{category.name}' added by user: {current_user.nickname}")
            logger.debug("add_category function exited in routes.py")

        return redirect(url_for('main.categories'))

    logger.debug("add_category function exited from GET request in routes.py")
    return render_template('add_category.html')


#-------------------------------
@bp.route('/categories/edit', methods=['GET', 'POST'])
@login_required
def edit_category():
    logger.debug(f"edit_category function entered in routes.py method: {request.method}")
    category_id = request.args.get('category_id')

    if request.method == 'POST':
        new_name = request.form['category'].strip().capitalize()
        new_description = request.form['description']
        new_type = request.form['type'].capitalize()

        category = Category.query.filter_by(id=category_id, user_id=current_user.id).first()
        if not category:
            logger.warning(f"Category not found for user: {current_user.nickname}")
            flash("Category not found!", "warning")
            logger.debug("edit_category function exited with failure (not found) in routes.py")
            return redirect(url_for('main.categories'))
        
        # Check if the new name/type combination already exists
        existing_category = Category.query.filter(Category.name == new_name, Category.type == new_type, Category.user_id == current_user.id, Category.id != category_id).first()
        if existing_category:
            logger.warning(f"Category '{new_name}' already exists for {new_type} for user: {current_user.nickname}")
            flash(f"Category '{new_name}' already exists for this type!", "info")
            logger.debug("edit_category function exited with failure (existing name) in routes.py")
            return redirect(url_for('main.categories'))
        
        # When changing type or name, check for existing categories with that type and name
        if new_type != category.type or new_name != category.name:
            in_use = category_in_use(category, current_user.id)
            if in_use:
                logger.warning(f"Can't change type of '{category.name}' because in use for: {current_user.nickname}")
                flash("Can't change category because it's in use!", "warning")
                logger.debug("edit_category function exited with failure (type in use) in routes.py")
                return redirect(url_for('main.categories'))

        # Update database
        category.name = new_name
        category.description = new_description
        category.type = new_type
        db.session.commit()
        flash(f"Changed category '{category.name}'", "success")
        logger.info(f"Category '{category.id}' updated by user: {current_user.nickname}")
        logger.debug("edit_category function exited with success in routes.py")
        return redirect(url_for('main.categories'))

    category = Category.query.get(category_id)
    logger.debug("edit_category function exited from GET request in routes.py")
    return render_template('edit_category.html', category=category)


#-------------------------------
@bp.route('/categories/delete', methods=['GET', 'POST'])
@login_required
def delete_category():
    logger.debug(f"delete_category function entered in routes.py method: {request.method}")
    category_id = request.args.get('category_id')
    to_delete = Category.query.get(category_id)

    if request.method == 'POST':

        if not to_delete:
            logger.warning(f"Category not found for user: {current_user.nickname}")
            flash("Category not found!", "warning")
            logger.debug("delete_category function (POST) exited with not found in routes.py")
            return redirect(url_for('main.categories'))

        # Check if the category is being used
        in_use = category_in_use(to_delete, current_user.id)
        if in_use:
            logger.warning(f"Can't delete '{to_delete.name}' because in use for: {current_user.nickname}")
            flash("Can't delete, category in use!", "warning")
            logger.debug("delete_category function (POST) exited with unable in routes.py")
            return redirect(url_for('main.categories'))

        # Update db
        db.session.delete(to_delete)
        db.session.commit()
        flash(f"Deleted category '{to_delete.name}'", "success")
        logger.info(f"Category '{to_delete.name}' deleted by user: {current_user.nickname}")
        logger.debug("delete_category function (POST) exited with success in routes.py")
        return redirect(url_for('main.categories'))

    logger.debug("delete_category function exited from GET request in routes.py")
    return render_template('delete_category.html', category=to_delete)


###
### Other functions (logging, helpers, etc.)
###

logLevel = logging.DEBUG


# ------------------------------
# Used to change the log level at runtime from the logging info page
@bp.route('/logging-info', methods=['GET', 'POST'])
@login_required
def logging_info():
    logger.debug(f"logging_info function entered in routes.py method: {request.method}")
    # Get the handler and check if its found
    file_handler = current_app.config.get('FILE_HANDLER')

    if not file_handler:
        logger.warning("Set log level function exited (handler not found)")
        flash("Log handler not found!", "warning")
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        level = request.args.get('level').upper()

        levels = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING
            # 'ERROR': logging.ERROR
        }

        if level not in levels:
            logger.warning("Set log level function exited (not valid level)")
        else:
            file_handler.setLevel(levels[level])
            savedLevel("POST", level)
            flash(f"Log level changed to {level}", "info")
            logger.info(f"Log level changed to {level}")
            logger.debug("Set log level function exited with success")
        return redirect(url_for('main.dashboard'))

    # Renders logging info
    log_file = get_file_content(os.getcwd() + '/logs/finance.log')
    logger.debug("logging_info function exited in routes.py")
    return render_template('logging_info.html', current_level=logging.getLevelName(file_handler.level), log_file=log_file)


#------------------------------
# Read files
def get_file_content(file_path):
    logger.debug(f"get_file_content function entered in routes.py for file: {file_path}")
    try:
        with open(file_path, 'r') as f:
            logger.debug(f"Successfully opened and read file: {file_path}")
            return f.read()
    except FileNotFoundError:
        logger.warning(f"File not found: {file_path}")
        return "File not found."
    except IOError as e:
        logger.warning(f"Error reading file: {e}")
        return "Error reading file."
    

#-------------------------------
# Return all current categories of a specific type (expense, income, or all)
def get_all_categories(type=str):
    logger.debug(f"get_all_categories function entered in routes.py for type: {type}")
    categories = []
    if type == "income":
        categories = Category.query.filter_by(user_id=current_user.id, type="Income").order_by(Category.name.asc()).distinct().all()
    elif type == "expense":
        categories = Category.query.filter_by(user_id=current_user.id, type="Expense").order_by(Category.name.asc()).distinct().all()
    else:
        categories = Category.query.filter_by(user_id=current_user.id).order_by(Category.name.asc()).distinct().all()
    logger.debug("get_all_categories function exited in routes.py")
    return categories


#-------------------------------
# Helper for repeat in dashboard filters. Checks input to get form dates based on timeframe then queries correct
#   table for values in the date range 
def check_dates(timeframe: str, form_start_date: str, form_end_date: str, for_what: str):
    logger.debug(f"check_dates function entered in routes.py for: {for_what}")
    end_date = None
    start_date = None

    if timeframe:
        if timeframe != "None":
            today = datetime.now()
            end_date = today.date()

            if timeframe == "1 day":
                start_date = (today - relativedelta(days=1)).date()
            elif timeframe == "3 days":
                start_date = (today - relativedelta(days=3)).date()
            elif timeframe == "5 day":
                start_date = (today - relativedelta(days=5)).date()
            elif timeframe == "7 days":
                start_date = (today - relativedelta(days=7)).date()
            elif timeframe == "1 month":
                start_date = (today - relativedelta(months=1)).date()
            elif timeframe == "6 months":
                start_date = (today - relativedelta(months=6)).date()
            elif timeframe == "1 year":
                start_date = (today - relativedelta(years=1)).date()
            elif timeframe == "All time":
                start_date = None

    # This means specific dates were chosen or none were at all
    if end_date == None:
        logger.debug("No timeframe")
        if request.form['start_date']:
            form_start_date = request.form['start_date']
            start_date = datetime.strptime(form_start_date, '%Y-%m-%d').date()
            end_date = datetime.now().date()
        if request.form['end_date']:
            form_end_date = request.form['end_date']
            end_date = datetime.strptime(form_end_date, '%Y-%m-%d').date()

    # Queries the correct table for expenses or incomes in the found date range
    expquery = None
    incquery = None
    if for_what == "expenses" and end_date:
        logger.debug("Querying expenses")
        expquery = Expense.query.filter_by(user_id=current_user.id)
        if start_date:
            expquery = expquery.filter(Expense.date >= start_date)
            dashboard_expenses['start_date'] = start_date
        else: 
            start_date = expquery.with_entities(func.min(Expense.date)).scalar()
            dashboard_expenses['start_date'] = start_date if start_date else date.today()
        if end_date:
            expquery = expquery.filter(Expense.date <= end_date)
            dashboard_expenses['end_date'] = end_date

    elif for_what == "incomes" and end_date:
        logger.debug("Querying incomes")
        incquery = Income.query.filter_by(user_id=current_user.id)
        if start_date:
            incquery = incquery.filter(Income.date >= start_date)
            dashboard_incomes['start_date'] = start_date
        else: 
            start_date = incquery.with_entities(func.min(Income.date)).scalar()
            dashboard_incomes['start_date'] = start_date if start_date else date.today()
        if end_date:
            incquery = incquery.filter(Income.date <= end_date)
            dashboard_incomes['end_date'] = end_date

    elif for_what == "compares" and end_date:
        logger.debug("Querying both expenses and incomes")
        expquery = Expense.query.filter_by(user_id=current_user.id)
        incquery = Income.query.filter_by(user_id=current_user.id)
        if start_date:
            expquery = expquery.filter(Expense.date >= start_date)
            incquery = incquery.filter(Income.date >= start_date)
            dashboard_comparatives['start_date'] = start_date 
        if end_date:
            expquery = expquery.filter(Expense.date <= end_date)
            incquery = incquery.filter(Income.date <= end_date)
            dashboard_comparatives['end_date'] = end_date

    logger.debug(f"Check dates function exited in routes.py expquery: {expquery is not None} and incquery: {incquery is not None}")
    return [start_date, end_date, incquery, expquery]


#-------------------------------
# Checks if a category is in use (before deleting or editing)
def category_in_use(category: Category, user_id: int):
    logger.debug(f"category_in_use function entered in routes.py for category: {category.name}")
    in_use = False
    if category.type.capitalize() == "Expense":
        in_use = Expense.query.filter_by(user_id=user_id, category=category.name.capitalize()).first()
        in_use = in_use or Budget.query.filter_by(user_id=user_id, category=category.name.capitalize()).first()
    else:
        in_use = Income.query.filter_by(user_id=user_id, category=category.name.capitalize()).first()
    logger.debug(f"category_in_use function exited in routes.py with in_use: {in_use is not None}")
    return in_use


import plotly.express as px
#-------------------------------
# Creates charts for dashboard
def get_pie_chart(data=map, type=str):
    logger.debug(f"get_pie_chart function entered in routes.py for: {type}")
    fig = px.pie(
        names=list(data.keys()), 
        values = [v['percentage'] for v in data.values()],
        title=f'{type} by Category {"- no data" if len(data) == 0 else ""}'
    )
    chart_div = fig.to_html(full_html=False, include_plotlyjs='cdn') # false is div only
    logger.debug("get_pie_chart function exited in routes.py")
    return chart_div


#-------------------------------
# Creates graph for dashboard
def get_line_graph(data=map, type=str):
    logger.debug(f"get_line_graph function entered in routes.py for: {type}")
    dates = sorted(data.keys())
    amounts = [data[date] for date in dates]

    # This happens if timeframe is none and no dates are specified 
    if len(dates) == 0:
        logger.debug("get_line_graph function exited in routes.py because no dates")
        return "No line graph data"
    
    fig = px.line(
        x=dates,
        y=amounts,
        title=f'{type} Over Time {"- no data" if len(data) == 0 else ""}',
        labels={'x': 'Date', 'y': 'Amount'}
    )

    chart_div = fig.to_html(full_html=False, include_plotlyjs='cdn')
    logger.debug("get_line_graph function exited in routes.py with finished graph")
    return chart_div