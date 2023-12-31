import os
import difflib
import json

ROOT = os.environ["SQL_ROOT_DIR"]


def search_closest_filenames(root_dir, filename, num_matches=5):
    searchTerm = filename.replace('.sql', '')
    sql_files = []
    content_matches = []
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.sql'):
                full_path = os.path.join(subdir, file)
                sql_files.append((file, full_path.replace(ROOT, '')))
                with open(full_path, 'r',  encoding="utf8") as fileRead:
                    if searchTerm in fileRead.read():
                        content_matches.append(full_path.replace(ROOT, ''))

    # Extract just the filenames for matching
    file_names = [f[0] for f in sql_files]

    # Find closest matches based on filenames
    closest_names = difflib.get_close_matches(filename, file_names, n=num_matches)

    # Retrieve full paths in the order of the closest matches
    closest_files_ordered = []
    for name in closest_names:
        for file_name, full_path in sql_files:
            if name == file_name:
                closest_files_ordered.append(full_path)
                break

    return {
        "file_name_search": closest_files_ordered,
        "file_contents_search": content_matches
    }

def search_sql_file(searchTerm):
    try:
        return json.dumps(search_closest_filenames(ROOT, searchTerm))
    except Exception as e:
        return json.dumps({"error": str(e)})

def read_sql_file(root_dir, file_path):
    # Convert both paths to absolute paths
    absolute_root = os.path.abspath(root_dir)
    file_path = os.path.join(ROOT, file_path)
    absolute_file_path = os.path.abspath(file_path)

    # Check if the file is within the root directory
    if not absolute_file_path.startswith(absolute_root):
        raise ValueError("Access to the file outside the root directory is not allowed")

    if absolute_file_path.endswith('.sql') and os.path.isfile(absolute_file_path):
        with open(absolute_file_path, 'r') as file:
            return file.read()
    else:
        raise FileNotFoundError(f"No SQL file found at {file_path}")

def get_sql_file(location):
    try:
        return read_sql_file(ROOT, location)
    except Exception as e:
        return json.dumps({"error": str(e)})

# print(search_sql_file('EmployeeBookedHours'))
# print(get_sql_file('dbo\\Tables\\Facts\\FactEmployeeHours.sql'))