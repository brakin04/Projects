# Holds all routes related to finances (expenses, incomes, budgets, categories)

from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models import db, Expense, Income, Budget, Category
from flask_login import login_required, current_user
from app.logging_config import logger
from ..utils import get_all_categories, get_pie_chart, category_in_use
from sqlalchemy import func
from datetime import datetime

finance_bp = Blueprint('finance', __name__)

###
### Expense routes
###

expense_filters = {}
expense_places = ""


# ------------------------------
@finance_bp.route('/expenses')
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
@finance_bp.route('/expenses/filter', methods=['POST', 'GET'])
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
            return redirect(url_for('finance.filter_expenses'))

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
        return redirect(url_for('finance.expenses'))

    categories = get_all_categories(type="expense")
    logger.debug(f"filter_expenses in routes.py exited (GET) with filters: {expense_filters}")
    return render_template('filter_expenses.html', filters=expense_filters, 
                           places=expense_places , categories=categories)

#-------------------------------
@finance_bp.route('/expenses/edit', methods=['GET', 'POST'])
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

        return redirect(url_for('finance.expenses'))

    expense = Expense.query.get(expense_id)
    categories = get_all_categories(type="expense")
    logger.debug("edit_expense function exited from GET request in routes.py")
    return render_template('edit_expense.html', expense=expense, categories=categories)


# ------------------------------
@finance_bp.route('/expenses/add', methods=['GET', 'POST'])
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
        return redirect(url_for('finance.expenses'))
    
    categories = get_all_categories(type="expense")
    logger.debug("add_expense function exited from GET request in routes.py")
    return render_template('add_expense.html', categories=categories)


# ------------------------------
@finance_bp.route('/expenses/delete', methods=['GET', 'POST'])
@login_required
def delete_expense():
    logger.debug(f"delete_expense function entered in routes.py method: {request.method}")
    expense_id = request.args.get('expense_id')
    if request.method == 'POST':
        expense_id = request.form.get('id')
        expense_to_delete = Expense.query.get(expense_id)
        if expense_to_delete:
            db.session.delete(expense_to_delete)
            db.session.commit()
            flash("Expense deleted successfully!", "success")
            logger.debug("delete_expense function (POST) exited with success in routes.py")
        else:   
            flash("Expense not found!", "failure")
            logger.info("delete_expense function (POST) exited with failure in routes.py")
        return redirect(url_for('finance.expenses'))
    
    expense = Expense.query.get(expense_id)
    to_see = f"At {expense.where} on {expense.date}"
    logger.debug("delete_expense function exited from GET request in routes.py")
    return render_template('delete.html', cancel_location='expenses', to_see=to_see, type='expense', id=expense_id)

###
### Income routes    
###

income_filters = {}
income_sources = ""


# ------------------------------
@finance_bp.route('/incomes')
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
@finance_bp.route('/incomes/filter', methods=['GET', 'POST'])
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
            return redirect(url_for('finance.filter_incomes'))
        
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
        return redirect(url_for('finance.incomes'))
    
    categories = get_all_categories(type="income")
    logger.debug(f"filter_incomes (GET) in routes.py exited with filters: {income_filters}")
    return render_template('filter_incomes.html', filters=income_filters, 
                           sources=income_sources, categories=categories)


#-------------------------------
@finance_bp.route('/incomes/edit', methods=['GET', 'POST'])
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
        return redirect(url_for('finance.incomes'))
    
    income = Income.query.get(income_id)
    categories = get_all_categories(type="income")
    logger.debug("edit_income function exited from GET request in routes.py")
    return render_template('edit_income.html', income=income, categories=categories)


# ------------------------------
@finance_bp.route('/incomes/add', methods=['GET', 'POST'])
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
        return redirect(url_for('finance.incomes'))
    
    categories = get_all_categories(type="income")
    logger.debug("add_income function exited from GET request in routes.py")
    return render_template('add_income.html', categories=categories)

    
# ------------------------------
@finance_bp.route('/incomes/delete', methods=['GET', 'POST'])
@login_required
def delete_income():
    logger.debug(f"delete_income function entered in routes.py method: {request.method}")
    income_id = request.args.get('income_id')

    if request.method == 'POST':
        income_id = request.form.get('id')
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
        return redirect(url_for('finance.incomes'))
    
    income = Income.query.get(income_id)
    to_see = f"From {income.source} on {income.date}"
    return render_template('delete.html', cancel_location='incomes', to_see=to_see, type='income', id=income_id)


###
### Budget routes
###


#-------------------------------
@finance_bp.route('/budget')
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
@finance_bp.route('/budget/edit', methods=['GET', 'POST'])
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
        return redirect(url_for('finance.budget'))
    
    categories = get_all_categories(type="expense")
    logger.debug("edit_budget function exited from GET request in routes.py")
    return render_template('edit_budget.html', budget=budget_to_update, categories=categories)


# ------------------------------
@finance_bp.route('/budget/add', methods=['GET', 'POST'])
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
        return redirect(url_for('finance.budget'))

    categories = get_all_categories(type="expense")
    logger.debug("add_budget function exited from GET request in routes.py")
    return render_template('add_budget.html', categories=categories)


#-------------------------------
@finance_bp.route('/budget/delete', methods=['GET', 'POST'])
@login_required
def delete_budget():
    logger.debug(f"delete_budget function entered in routes.py method: {request.method}")
    budget_id = request.args.get('budget_id')

    if request.method == 'POST':
        budget_id = request.form.get('id')
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
        return redirect(url_for('finance.budget'))
    
    budget = Budget.query.get(budget_id)
    logger.debug("delete_budget function exited from GET request in routes.py")
    return render_template('delete.html', cancel_location='budget', to_see=budget.category, type='budget', id=budget_id)


###
### Category Routes
###


#-------------------------------
@finance_bp.route('/categories', methods=['GET'])
@login_required
def categories():
    logger.debug("Categories function entered in routes.py")
    type_requested = request.args.get('types')
    categories = get_all_categories(type=type_requested)
    logger.debug("Categories function exited in routes.py")
    return render_template('categories.html', categories=categories)


#-------------------------------
@finance_bp.route('/category/add', methods=['GET', 'POST'])
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

        return redirect(url_for('finance.categories'))

    logger.debug("add_category function exited from GET request in routes.py")
    return render_template('add_category.html')


#-------------------------------
@finance_bp.route('/categories/edit', methods=['GET', 'POST'])
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
            return redirect(url_for('finance.categories'))
        
        # Check if the new name/type combination already exists
        existing_category = Category.query.filter(Category.name == new_name, Category.type == new_type, Category.user_id == current_user.id, Category.id != category_id).first()
        if existing_category:
            logger.warning(f"Category '{new_name}' already exists for {new_type} for user: {current_user.nickname}")
            flash(f"Category '{new_name}' already exists for this type!", "info")
            logger.debug("edit_category function exited with failure (existing name) in routes.py")
            return redirect(url_for('finance.categories'))
        
        # When changing type or name, check for existing categories with that type and name
        if new_type != category.type or new_name != category.name:
            in_use = category_in_use(category, current_user.id)
            if in_use:
                logger.warning(f"Can't change type of '{category.name}' because in use for: {current_user.nickname}")
                flash("Can't change category because it's in use!", "warning")
                logger.debug("edit_category function exited with failure (type in use) in routes.py")
                return redirect(url_for('finance.categories'))

        # Update database
        category.name = new_name
        category.description = new_description
        category.type = new_type
        db.session.commit()
        flash(f"Changed category '{category.name}'", "success")
        logger.info(f"Category '{category.id}' updated by user: {current_user.nickname}")
        logger.debug("edit_category function exited with success in routes.py")
        return redirect(url_for('finance.categories'))

    category = Category.query.get(category_id)
    logger.debug("edit_category function exited from GET request in routes.py")
    return render_template('edit_category.html', category=category)


#-------------------------------
@finance_bp.route('/categories/delete', methods=['GET', 'POST'])
@login_required
def delete_category():
    logger.debug(f"delete_category function entered in routes.py method: {request.method}")
    category_id = request.args.get('category_id')

    if request.method == 'POST':
        category_id = request.form.get('id')
        to_delete = Category.query.get(category_id)

        if not to_delete:
            logger.warning(f"Category not found for user: {current_user.nickname}")
            flash("Category not found!", "warning")
            logger.debug("delete_category function (POST) exited with not found in routes.py")
            return redirect(url_for('finance.categories'))

        # Check if the category is being used
        in_use = category_in_use(to_delete, current_user.id)
        if in_use:
            logger.warning(f"Can't delete '{to_delete.name}' because in use for: {current_user.nickname}")
            flash("Can't delete, category in use!", "warning")
            logger.debug("delete_category function (POST) exited with unable in routes.py")
            return redirect(url_for('finance.categories'))

        # Update db
        db.session.delete(to_delete)
        db.session.commit()
        flash(f"Deleted category '{to_delete.name}'", "success")
        logger.info(f"Category '{to_delete.name}' deleted by user: {current_user.nickname}")
        logger.debug("delete_category function (POST) exited with success in routes.py")
        return redirect(url_for('finance.categories'))

    to_delete = Category.query.get(category_id)
    logger.debug("delete_category function exited from GET request in routes.py")
    return render_template('delete.html', cancel_location='categories', to_see=to_delete.name, type='category', id=category_id)