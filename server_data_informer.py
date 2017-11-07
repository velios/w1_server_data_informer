import json
import csv
import os
import pandas as pd

# Изменить имена файлов если нужно
ALL_SERVER_FILE_PATH = '1_allservers.txt'
SESSIONS_FILE_PATH = '2_sessions.txt'
USERS_FILE_PATH = '3_users.txt'


def load_json_data(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r') as file_handler:
        return pd.read_json(file_handler)


def load_csv_data_like_json(filepath, delimeter=''):
    csv_rows = []
    with open(filepath) as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        title = reader.fieldnames
        for row in reader:
            csv_rows.extend([{title[i]:row[title[i]] for i in range(len(title))}])
        return csv_rows


def fetch_last_sessions_list(sessions_list):
    # Файл сессий читается с конца
    session_id_compare_list, last_sessions_list = [], []
    for session in reversed(sessions_list):
        if not session['session_id'] in session_id_compare_list:
            last_sessions_list.append(session)
            session_id_compare_list.append(session['session_id'])
    return last_sessions_list


def prepare_data():
    all_servers_dataframe = load_json_data(ALL_SERVER_FILE_PATH)
    sessions_list = load_csv_data_like_json(SESSIONS_FILE_PATH, delimeter='\t')
    users_dataframe = load_json_data(USERS_FILE_PATH)
    last_sessions_list = fetch_last_sessions_list(sessions_list)
    last_sessions_dataframe = pd.read_json(json.dumps(last_sessions_list))
    prepare_list_of_dicts = last_sessions_dataframe.merge(users_dataframe,
                                                          left_on='user_id',
                                                          right_on='ID',
                                                          how='left')
    final_list_of_dicts = prepare_list_of_dicts.merge(all_servers_dataframe,
                                                      left_on='instance_id',
                                                      right_on='ID',
                                                      how='left').T.to_dict().values()
    return final_list_of_dicts


def print_last_session_machine_list(final_list_of_dicts):
    print('{:<3}  {:<40}    {:<40}   {:<30}   {:<20}   {:<70}   {:<30}'.format('№', 'Session_№', 'Server_id', 'Server_name',
                                                                      'Host','User_Id', 'User_name'))
    for index, server_data in enumerate(final_list_of_dicts, start=1):
        print(
            '{index:<3}: {session_id:<40} => {server_id:<40} - {server_name:<30} - {host:<20} - {user_id:<70} - {user_name:<30}'.format(
                index=index,
                session_id=server_data['session_id'],
                server_id=server_data['ID_y'],
                server_name=server_data['Name_y'],
                host=server_data['Host'],
                user_name=server_data['Name_x'],
                user_id=server_data['ID_x']
                ))


if __name__ == '__main__':
    final_list_of_dicts = prepare_data()
    print_last_session_machine_list(final_list_of_dicts)
