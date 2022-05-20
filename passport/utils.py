import os


def create_folder_if_not_exist(data_file_path):
    dir_name = os.path.dirname(data_file_path)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name, exist_ok=True)
