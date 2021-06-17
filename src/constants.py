import os

SERVICE_ACCOUNT_PATH = '/home/maksym/git/gs_test/var/for-tests-304014-d5320cdfef53.json'

DB_CREDENTIALS = {
    'host': '3.82.236.61',
    'db_name': 'postgres',
    'user': 'postgres',
    'password': os.environ['DB_PASSWORD'],
}
