from .models import Expense, Income, Budget, Category
from app.logging_config import logger
from flask_login import  current_user
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy import func
from dateutil.relativedelta import relativedelta

#------------------------------
# Read files
def get_file_content(file_path: Optional[str] = "no path given"):
    logger.debug(f"get_file_content function entered in utils.py for file: {file_path}")
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
def get_all_categories(type: Optional[str] = 'all'):
    logger.debug(f"get_all_categories function entered in utils.py for type: {type}")
    categories = []
    if type == "income":
        categories = Category.query.filter_by(user_id=current_user.id, type="Income").order_by(Category.name.asc()).distinct().all()
    elif type == "expense":
        categories = Category.query.filter_by(user_id=current_user.id, type="Expense").order_by(Category.name.asc()).distinct().all()
    else:
        categories = Category.query.filter_by(user_id=current_user.id).order_by(Category.name.asc()).distinct().all()
    logger.debug("get_all_categories function exited in utils.py")
    return categories


# Gets all expenses or incomes in a date range for the current user. Used for dashboard filters and comparisons
def get_finances_by_date_range(start_date: Optional[datetime] = None, end_date: Optional[datetime] = None, 
                               finance_type: Optional[str] = None):
    logger.debug(f"get_finances_by_date_range function entered in utils.py for type: {finance_type}")
    query = None
    if finance_type == 'e':
        query = Expense.query.filter_by(user_id=current_user.id)
        if start_date:
            query = query.filter(Expense.date >= start_date)
        if end_date:
            query = query.filter(Expense.date <= end_date)
    elif finance_type == 'i':
        query = Income.query.filter_by(user_id=current_user.id)
        if start_date:
            query = query.filter(Income.date >= start_date)
        if end_date:
            query = query.filter(Income.date <= end_date)
    logger.debug(f"get_finances_by_date_range function exited in utils.py with query: {query is not None}")
    return query


# gets total amount from a query of expenses or incomes. Used for dashboard filters and comparisons
def get_total_from_query(query=None, kind: Optional[str] = None):
    logger.debug(f"get_total_from_query function entered in utils.py for kind: {kind}")
    total = 0
    if query and kind:
        if kind == 'i':
            total = query.with_entities(func.sum(Income.amount)).scalar() or 0
        elif kind == 'e':
            total = query.with_entities(func.sum(Expense.amount)).scalar() or 0
    logger.debug(f"get_total_from_query function exited in utils.py with total: {total}")
    return total


#-------------------------------
# Helper for repeat in dashboard filters. Checks input to get form dates based on 
#   timeframe then queries correct table for values in the date range 
#  returns [start date, end date, income query, expense query]
def check_dates(timeframe: Optional[str] = None, form_start_date: Optional[str] = None, 
                form_end_date: Optional[str] = None, for_what: Optional[str] = None):
    logger.debug(f"check_dates function entered in utils.py for: {for_what}")
    end_date = None
    start_date = None

    if timeframe and timeframe != "None":
        today = datetime.now()
        end_date = today.date()

        if timeframe == "1 day":
            start_date = (today - relativedelta(days=1)).date()
        elif timeframe == "3 days":
            start_date = (today - relativedelta(days=3)).date()
        elif timeframe == "5 days":
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
        if not form_start_date and not form_end_date:
            logger.debug("No dates given exiting check_dates function in utils.py all 'None'")
            return [None, None, None, None]
        if form_start_date:
            start_date = datetime.strptime(form_start_date, '%Y-%m-%d').date()
            end_date = datetime.now().date()
        if form_end_date:
            end_date = datetime.strptime(form_end_date, '%Y-%m-%d').date()

    # Queries the correct table for expenses or incomes in the found date range
    expquery = None
    incquery = None
    total = 0
    if (for_what == "expenses" or for_what == "compares") and end_date:
        expquery = get_finances_by_date_range(start_date, end_date, 'e')
        if for_what == "compares":
            total -= get_total_from_query(expquery, 'e') if expquery else 0
        else:
            total += get_total_from_query(expquery, 'e') if expquery else 0
    elif (for_what == "incomes" or for_what == "compares") and end_date:
        incquery = get_finances_by_date_range(start_date, end_date, 'i')
        total += get_total_from_query(incquery, 'i') if incquery else 0

    logger.debug(f"Check dates function exited in utils.py expquery: {expquery is not None} and incquery: {incquery is not None}")
    return [start_date, end_date, total]


#-------------------------------
# Checks if a category is in use (before deleting or editing)
def category_in_use(category: Category, user_id: int):
    logger.debug(f"category_in_use function entered in utils.py for category: {category.name}")
    in_use = False
    if category.type.capitalize() == "Expense":
        in_use = Expense.query.filter_by(user_id=user_id, category=category.name.capitalize()).first()
        in_use = in_use or Budget.query.filter_by(user_id=user_id, category=category.name.capitalize()).first()
    else:
        in_use = Income.query.filter_by(user_id=user_id, category=category.name.capitalize()).first()
    logger.debug(f"category_in_use function exited in utils.py with in_use: {in_use is not None}")
    return in_use


#-------------------------------
#gets category totals
def get_category_totals(query=None, kind: Optional[str] = None):
    category_totals = []
    if query and kind:
        if kind == 'e':
            category_totals = query.with_entities(Expense.category, func.sum(Expense.amount)).group_by(Expense.category).all()
        elif kind == 'i':
            category_totals = query.with_entities(Income.category, func.sum(Income.amount)).group_by(Income.category).all()
    return category_totals


import plotly.express as px
#-------------------------------
# Creates charts for dashboard
def get_pie_chart(data: Optional[map] = {}, type: Optional[str] = 'no type'):
    logger.debug(f"get_pie_chart function entered in utils.py for: {type}")
    fig = px.pie(
        names=list(data.keys()), 
        values = [v['percentage'] for v in data.values()],
        title=f'{type.capitalize()} by Category {"- no data" if len(data) == 0 else ""}'
    )
    chart_div = fig.to_html(full_html=False, include_plotlyjs='cdn') # false is div only
    logger.debug("get_pie_chart function exited in utils.py")
    return chart_div


#-------------------------------
# Creates graph for dashboard
def get_line_graph(start: Optional[datetime] = None, end: Optional[datetime] = None, 
                   type: Optional[str] = 'no type'):
    logger.debug(f"get_line_graph function entered in utils.py for: {type}")
    
    typeChar = 'e' if type == "expenses" else 'i'
    theData = get_finances_by_date_range(start, end, typeChar)

    total = 0
    category_totals = get_category_totals(theData, typeChar)
    # if type == "expenses" and expenses:
    #     total = expenses.with_entities(func.sum(Expense.amount)).scalar() or 0
    #     # count = expenses.with_entities(func.count(Expense.amount)).scalar() or 0
    #     category_totals = expenses.with_entities(Expense.category, func.sum(Expense.amount)).group_by(Expense.category).all()
    # elif type == "incomes" and incomes:
    #     total = incomes.with_entities(func.sum(Income.amount)).scalar() or 0
    #     # count = incomes.with_entities(func.count(Income.amount)).scalar() or 0
    #     category_totals = incomes.with_entities(Income.category, func.sum(Income.amount)).group_by(Income.category).all()
    # Line graph data
    line_data = {}
    if start:
        line_data[start.strftime('%Y-%m-%d')] = 0
    if end:
        line_data[end.strftime('%Y-%m-%d')] = 0

    # Loop through each date in the range
    split = 1
    if start and end:
        dateDelta = (start - end).days
        if (end - start).days > 360:
            dateDelta = (start - end).days
            split = int(max((dateDelta / 180) * 2, 1))

        if start_date and end_date:
            temp_date = start_date
            while temp_date <= end_date:
                line_data[temp_date.strftime('%Y-%m-%d')] = 0
                temp_date += timedelta(days=split)
        
        # Sum values from each date
        # turns into multiple days combined when all time is selected to avoid overcrowding the graph
        #     split is determined by how long the date range is
        # if theData:
        #     sum = [0, 0, timeAnswers[0].strftime('%Y-%m-%d')]
        #     for data in theData:
        #         if (sum[2] - data.date.strftime('%Y-%m-%d')).days :
        #         sum[1] += 1
        #         sum[0] += data.amount
        #         if (sum[1] >= split):
        #             date_key = data.date.strftime('%Y-%m-%d')
        #             line_data[date_key] = line_data.get(date_key, 0) + sum[0]
        #             sum = [0, 0]
    if theData:
        # Pre-convert keys to date objects once for efficiency
        available_buckets = [datetime.strptime(k, '%Y-%m-%d').date() for k in line_data.keys()]
        for data in theData:
            closest_bucket_date = min(available_buckets, key=lambda x: abs((x - data.date).days))
            date_key = closest_bucket_date.strftime('%Y-%m-%d')
            print(f"closest bucket: {date_key} for data date: {data.date}")
            line_data[date_key] += data.amount

    # Pie chart data
    category_breakdown = {}
    if total > 0:
        for category, amount in category_totals:
            percentage = (amount / total) * 100
            category_breakdown[category] = {'total': amount, 'percentage': round(percentage, 2)}

    dates = sorted(data.keys())
    amounts = [data[date] for date in dates]

    # This happens if timeframe is none and no dates are specified 
    if len(dates) == 0:
        logger.debug("get_line_graph function exited in utils.py because no dates")
        return "No line graph data"
    
    fig = px.line(
        x=dates,
        y=amounts,
        title=f'{type.capitalize()} Over Time {"- no data" if len(data) == 0 else ""}',
        labels={'x': 'Date', 'y': 'Amount'}
    )

    chart_div = fig.to_html(full_html=False, include_plotlyjs='cdn')
    logger.debug("get_line_graph function exited in utils.py with finished graph")
    return chart_div