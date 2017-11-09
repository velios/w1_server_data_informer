import json
import csv
import os
import pprint

import listorm as ls


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


if __name__ == '__main__':
    all_servers_list = load_json_data(ALL_SERVER_FILE_PATH)
    sessions_list = load_csv_data_in_json_format(SESSIONS_FILE_PATH,
                                                 delimeter='\t')
    users_list = load_json_data(USERS_FILE_PATH)
    last_sessions_list = fetch_last_sessions_list(sessions_list)
    
    print(all_servers_list)

    # print(all_servers_list)
    # pprint.pprint(sessions_list)
    # print(users_dataframe)
    # print(last_sessions_list)
    # print(len(last_sessions_list))
    
    # print(len(first_merge))
    # pprint.pprint(first_merge)