import gspread

from src.constants import SERVICE_ACCOUNT_PATH
from src.db import Database

TASKS_RANGE = 'C4:C50'


class GSpread:

    def __init__(self, service_account_path=SERVICE_ACCOUNT_PATH):
        self.gs_client = gspread.service_account(service_account_path)

    def load_sheet_by_name(self, sheet_name):
        sheet = self.gs_client.open(sheet_name).sheet1
        return sheet

    def save_todo_tasks_to_db(self):
        todo_sheet = self.load_sheet_by_name('gspread test todo')
        result_values = todo_sheet.get(TASKS_RANGE)
        todo_tasks = [t[0] for t in result_values]
        with Database() as db:
            db.replace_tasks(todo_tasks)

    def load_db_tasks_to_spreadsheet(self):
        with Database() as db:
            tasks = db.load_tasks()
        todo_sheet = self.load_sheet_by_name('gspread test todo')
        todo_sheet.update(TASKS_RANGE, [[t] for t in tasks])
