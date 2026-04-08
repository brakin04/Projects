# Holds routes for home page, profile, dashboard, and logging info page

from shlex import split

from flask import Blueprint, render_template, current_app, session, request, redirect, url_for, flash
from ..models import db, User, Expense, Income
from werkzeug.security import generate_password_hash
from flask_login import login_required, current_user
from app.logging_config import logger, savedLevel
from ..utils import get_file_content, check_dates, get_pie_chart, get_line_graph
from sqlalchemy import func
from datetime import datetime, timedelta
import logging
import os

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    logger.debug(f"Home function entered in main.py Session ID: {session.get('session_id')}")
    logger.info("Home page requested")

    # get README.md content
    # readme_file = get_file_content(os.getcwd() + '/README.md')

    logger.debug("Home function exited in main.py")
    return render_template('home.html')#, content=readme_file)


#-------------------------------
@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    logger.debug(f"Profile function entered in main.py with method: {request.method}")

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
        logger.debug("Profile function exited with success in main.py")
        return redirect(url_for('main.profile'))
    
    # GET request handling
    userInfo = {'email': current_user.email, 'nickname': current_user.nickname}
    return render_template('profile.html', userInfo=userInfo)


###
### Dashboard functions
###


# ------------------------------
@main_bp.route('/dashboard')
@login_required
def dashboard():
    logger.debug("Dashboard function entered in main.py")
    expenses = session.get('dashboard_expenses', {})
    incomes = session.get('dashboard_incomes', {})
    compares = session.get('dashboard_compares', {})
    timeframes = ["None", "1 day", "3 days", "5 days", "7 days", "1 month", "6 months", "1 year", "All time"]
    return render_template('dashboard.html', expenses=expenses, incomes=incomes, 
                           compare=compares, timeframes=timeframes)


# Combine all 3 into one
#-------------------------------
@main_bp.route('/dashboard/filter', methods=['POST'])
@login_required
def filter_dashboard():
    logger.debug("Filter dashboard function entered in main.py")
    kind = request.args.get('kind').lower()

    if kind not in ['expenses', 'incomes', 'compares']:
        logger.warning(f"Invalid filter kind: {kind}")
        flash("Invalid filter type!", "warning")
        return redirect(url_for('main.dashboard'))
    
    # Clear previous filters
    session[f'dashboard_{kind}'] = {}

    if 'clear' in request.form:
        logger.debug(f"Clearing {kind} filters as per request")
        return redirect(url_for('main.dashboard'))

    # Add filters to dictionary
    timeframe = request.form['timeframe']
    form_start_date = request.form['start_date']
    form_end_date = request.form['end_date']

    timeAnswers = check_dates(timeframe=timeframe, form_start_date=form_start_date, 
                              form_end_date=form_end_date, for_what=kind)

    # expenses = timeAnswers[3]
    # incomes = timeAnswers[2]
    if kind == "compares":
    #     incTotal = 0
    #     expTotal = 0
    #     if incomes:
    #         incTotal = incomes.with_entities(func.sum(Income.amount)).scalar() or 0
    #     if expenses:
    #         expTotal = expenses.with_entities(func.sum(Expense.amount)).scalar() or 0
    #     profit = incTotal - expTotal

        # Add em to map
        session['dashboard_compares'] = {
            "timeframe": timeframe,
            "profit": timeAnswers[2] if timeAnswers[2] else 0,
            "start_date": timeAnswers[0].strftime("%Y-%m-%d") if timeAnswers[0] else None,
            "end_date": timeAnswers[1].strftime("%Y-%m-%d") if timeAnswers[1] else None
        }
    else:
        # Add em to map
        session[f'dashboard_{kind}'] = {
            "timeframe": timeframe,
            "total": timeAnswers[2] if timeAnswers[2] else 0,
            # "category_chart": get_pie_chart(data=category_breakdown, type=kind),
            # "line_chart": get_line_graph(data=line_data, type=kind),
            "start_date": timeAnswers[0].strftime("%Y-%m-%d") if timeAnswers[0] else None,
            "end_date": timeAnswers[1].strftime("%Y-%m-%d") if timeAnswers[1] else None
        }

    return redirect(url_for('main.dashboard'))


#-------------------------------
@main_bp.route('/dashboard/expenses/filter', methods=['POST'])
@login_required
def filter_dashboard_expenses():
    logger.debug("Filter dashboard expenses function entered in main.py")

    # Clear previous filters
    session['dashboard_expenses'] = {}

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
    session['dashboard_expenses'] = {
        "timeframe": timeframe,
        "total": total,
        "category_chart": get_pie_chart(data=category_breakdown, type="Expenses"),
        "line_chart": get_line_graph(data=line_expenses, type="Expenses"),
        "start_date": timeAnswers[0].strftime("%Y-%m-%d") if timeAnswers[0] else None,
        "end_date": timeAnswers[1].strftime("%Y-%m-%d") if timeAnswers[1] else None
    }

    return redirect(url_for('main.dashboard'))

    
#-------------------------------
@main_bp.route('/dashboard/incomes/filter', methods=['POST'])
@login_required
def filter_dashboard_incomes():
    logger.debug("Filter dashboard incomes function entered in main.py")

    # Clear previous filters
    session['dashboard_incomes'] = {}

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
    session['dashboard_incomes'] = {
        "timeframe": timeframe,
        "total": total,
        "category_chart": get_pie_chart(data=category_breakdown, type="Incomes"),
        "line_chart": get_line_graph(data=line_incomes, type="Incomes"),
        "start_date": timeAnswers[0].strftime("%Y-%m-%d") if timeAnswers[0] else None,
        "end_date": timeAnswers[1].strftime("%Y-%m-%d") if timeAnswers[1] else None
    }

    return redirect(url_for('main.dashboard'))


#-------------------------------
@main_bp.route('/dashboard/compare/filter', methods=['POST'])
@login_required
def filter_dashboard_comparatives():
    logger.debug("Filter dashboard comparatives function entered in main.py")

    # Clear previous filters
    session['dashboard_compares'] = {}

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
    session['dashboard_compares'] = {
        "timeframe": timeframe,
        "profit": profit,
        "start_date": timeAnswers[0].strftime("%Y-%m-%d") if timeAnswers[0] else None,
        "end_date": timeAnswers[1].strftime("%Y-%m-%d") if timeAnswers[1] else None
    }

    return redirect(url_for('main.dashboard'))


###
### Other routes (logging)
###

logLevel = logging.DEBUG
# ------------------------------
# Used to change the log level at runtime from the logging info page
@main_bp.route('/logging-info', methods=['GET', 'POST'])
@login_required
def logging_info():
    logger.debug(f"logging_info function entered in main.py method: {request.method}")
    # Get the handler and check if its found
    file_handler = current_app.config.get('FILE_HANDLER')

    if not file_handler:
        logger.warning("logging_info function exited (handler not found)")
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
    logger.debug("logging_info function exited in main.py")
    return render_template('logging_info.html', current_level=logging.getLevelName(file_handler.level), log_file=log_file)