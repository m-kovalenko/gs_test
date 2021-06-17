import json

from flask import Blueprint, Response, Request
from loguru import logger

from src.gspread import GSpread

simple_page = Blueprint('api_page', __name__)


@logger.catch
@simple_page.get("/api/load")
def load_data():
    gspread = GSpread()
    gspread.load_db_tasks_to_spreadsheet()
    return Response(status=200)


@logger.catch
@simple_page.get("/api/save")
def add_order():
    gspread = GSpread()
    gspread.save_todo_tasks_to_db()
    return Response(status=200)
