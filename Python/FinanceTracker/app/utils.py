from .models import Expense, Income, Budget, Category
from app.logging_config import logger
from flask_login import  current_user
from datetime import datetime, timedelta
from typing import Optional
import plotly.express as px
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
# Return all current categories of a specific type (expense, income, or all) as a list
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


#-------------------------------
# Gets all expenses or incomes in a date range for the current user. Used for dashboard filters and comparisons. 
#   Returns a list of expenses or incomes or None if there's none or type is wrong.
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
    return query.all() if query else None


#-------------------------------
# Gets total amount from a query of expenses or incomes. Used for dashboard filters and comparisons. 
#   Returns a double or 0 if none.
def get_total_from_query_list(query: Optional[list] = None):
    logger.debug(f"get_total_from_query function entered in utils.py")
    total = 0
    if query and len(query) > 0:
        total = sum(item.amount for item in query)
    logger.debug(f"get_total_from_query function exited in utils.py")
    return total


#-------------------------------
# Helper for repeat in dashboard filters. Checks input to get form 
#   dates based on timeframe. returns [start date, end date]
def check_dates(timeframe: Optional[str] = None, form_start_date: Optional[str] = None, 
                form_end_date: Optional[str] = None):
    logger.debug(f"check_dates function entered in utils.py")
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

    logger.debug(f"Check dates function exited in utils.py ")
    return [start_date, end_date]


#-------------------------------
# Checks if a category is in use (before deleting or editing). Returns a boolean.
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
# Creates pie chart for dashboard. Takes in a list of expenses or incomes and returns html
def get_pie_chart(query_data: Optional[list] = None, type: Optional[str] = 'No type'):
    logger.debug(f"get_pie_chart function entered in utils.py for: {type}")

    if not query_data or len(query_data) == 0:
        logger.debug("get_pie_chart function exited in utils.py because no data")
        return "No pie chart data"
    
    category_map = {}
    for item in query_data:
        category_map[item.category] = category_map.get(item.category, 0) + item.amount

    fig = px.pie(
        names=list(category_map.keys()), 
        values=list(category_map.values()),
        title=f'{type.capitalize()} by Category'
    )
    logger.debug("get_pie_chart function exited in utils.py with success")
    return fig.to_html(full_html=False, include_plotlyjs='cdn') # false is div only


#-------------------------------
# Creates bar graph for dashboard. Takes in a list of expenses or incomes and returns html
def get_bar_graph(start: Optional[datetime] = None, end: Optional[datetime] = None, 
                   query_data: Optional[list] = None, type: Optional[str] = 'no type'):
    logger.debug(f"get_bar_graph function entered in utils.py for: {type}")

    if not query_data or len(query_data) == 0:
        logger.debug("get_bar_graph function exited in utils.py because no data")
        return "No bar graph data"
    
    actual_start = start if start else min(d.date for d in query_data)
    actual_end = end if end else max(d.date for d in query_data)
    if hasattr(actual_start, 'date'): actual_start = actual_start.date()
    if hasattr(actual_end, 'date'): actual_end = actual_end.date()
    delta_days = (actual_end - actual_start).days

    fill_split = 1
    if delta_days > 365 * 20:
        fmt = '%Y'
        fill_split = 367
    elif delta_days > 365 * 2:
        fmt = '%Y-%m'
        fill_split = 32
    elif delta_days > 90:
        fmt = '%Y-w%W'
        fill_split=7
    else:
        fmt = '%Y-%m-%d'

    bar_data = {}
    if delta_days >= 0:
        current = actual_start
        if fill_split != 1:
            current = current.replace(day=1)
        while current <= actual_end:
            month_key = current.strftime(fmt)
            bar_data[month_key] = 0
            current = current + timedelta(days=fill_split)
            if fill_split != 7 and fill_split != 1:
                current = current.replace(day=1)
    
    for item in query_data:
        bucket_key = item.date.strftime(fmt)
        bar_data[bucket_key] = bar_data.get(bucket_key, 0) + item.amount

    sorted_keys = sorted(bar_data.keys())
    amounts = [bar_data[k] for k in sorted_keys]

    fig = px.bar(
        x=sorted_keys,
        y=amounts,
        title=f'{type.capitalize()} Over Time',
        labels={'x': 'Time Period', 'y': 'Total Amount'},
        template="plotly_white"
    )
    fig.update_layout(xaxis_tickangle=-45,              
            xaxis=dict(
            tickmode='auto',
            nticks=15,      # Limits the maximum number of labels shown
            type='category' # Keeps the bars centered over the labels
        ))

    logger.debug("get_bar_graph function exited in utils.py with finished graph")
    return fig.to_html(full_html=False, include_plotlyjs='cdn')