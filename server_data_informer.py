import json
import csv
import os
import pprint

import listorm as ls
import texttable


ALL_SERVER_FILE_PATH = '1_allservers.txt'
SESSIONS_FILE_PATH = '2_sessions.txt'
USERS_FILE_PATH = '3_users.txt'


def load_json_data(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r') as file_handler:
        return json.load(file_handler)


def load_csv_data_in_json_format(filepath, delimeter=''):
    csv_rows = []
    with open(filepath) as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        title = reader.fieldnames
        for row in reader:
            csv_rows.extend([{title[i]:row[title[i]] for i in range(len(title))}])
        return csv_rows


def fetch_last_sessions_list(sessions_list):
    session_id_compare_list, last_sessions_list = [], []
    for session in reversed(sessions_list):
        if not session['session_id'] in session_id_compare_list:
            last_sessions_list.append(session)
            session_id_compare_list.append(session['session_id'])
    return last_sessions_list
    

def print_last_session_instances():
    column_query = ['session_id', 'instance_id', 'instance_name', 'Host', 'user_id', 'user_name']
    
    join_sessions_servers_and_users_lists = last_sessions_list.join(
        servers_list.rename(ID='instance_id', Name='instance_name'),
        on='instance_id',
        how='left').join(
            users_list.rename(ID='user_id', Name='user_name'),
            on='user_id',
            how='left'
            ).select(*column_query)
    

    table = texttable.Texttable(max_width=150)
    table_head = [column_query]
    
    table_body = join_sessions_servers_and_users_lists.row_values(*column_query)

    table.add_rows(table_head + table_body)
    print(table.draw())
    
    join_sessions_servers_and_users_lists.to_csv(filename='last_session_instances.csv')



if __name__ == '__main__':
    servers_list = ls.Listorm(load_json_data(ALL_SERVER_FILE_PATH))
    sessions_list = load_csv_data_in_json_format(SESSIONS_FILE_PATH,
                                                 delimeter='\t')
    users_list = ls.Listorm(load_json_data(USERS_FILE_PATH))
    last_sessions_list = ls.Listorm(fetch_last_sessions_list(sessions_list))
    
    print_last_session_instances()