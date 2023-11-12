import json

import difflib
import os

def closest_measure_name(data, input_string):
    """
    This function takes a JSON object representing the Tabular model of a Data Warehouse
    and an input string. It uses a string distance measure to find and return the closest
    measure name from all measures present in the model.
    
    :param data: JSON object representing the Tabular model of a Data Warehouse
    :param input_string: The input string to compare against measure names
    :return: The closest measure name based on string distance
    """
    # List to store all the measure names
    measure_names = []
    
    # Loop through each table and collect all measure names
    for table in data['model']['tables']:
        if 'measures' in table:
            measure_names.extend(measure['name'] for measure in table['measures'])

    # Use difflib to find the closest match to the input string from the list of measure names
    closest_match = difflib.get_close_matches(input_string, measure_names, n=1)
    
    # Return the closest match, if found, otherwise return None
    return closest_match[0] if closest_match else None

# You can call this function with the JSON object and an input string to find the closest measure name.

import difflib

def closest_table_name(data, input_table_name):
    """
    This function takes a JSON object representing the Tabular model of a Data Warehouse
    and an input table name. It uses a string distance measure to find and return the closest
    table name from all tables present in the model.

    :param data: JSON object representing the Tabular model of a Data Warehouse
    :param input_table_name: The input table name to compare against table names
    :return: The closest table name based on string distance
    """
    # List to store all the table names
    table_names = [table['name'] for table in data['model']['tables']]

    # Use difflib to find the closest match to the input string from the list of table names
    closest_match = difflib.get_close_matches(input_table_name, table_names, n=1)

    # Return the closest match, if found, otherwise return None
    return closest_match[0] if closest_match else None

# You can call this function with the JSON object and an input table name to find the closest table name.

def find_table(data, input_table_name):
    input_table_name = closest_table_name(data, input_table_name)
    for table in data['model']['tables']:
        if table['name'] == input_table_name:
            return {
                "name": table['name'],
                "measures": [{'name': metric['name'], 'isHidden': metric.get('isHidden', False)} for metric in table.get('measures', [])],
                "dimensions": [{'name': column['name'], 'isHidden': column.get('isHidden', False)} for column in table.get('columns', [])],
                "partitions": [{'name': partition['name'], 'source': partition['source']} for partition in table['partitions']]
            }


def find_measure(data, measure_name):
    measure_name = closest_measure_name(data, measure_name)
    """
    This function takes a JSON object representing the Tabular model of a Data Warehouse
    and a measure name. It returns a tuple with the measure object and the name of the
    table that the measure is part of.
    
    :param data: JSON object representing the Tabular model of a Data Warehouse
    :param measure_name: The name of the measure to be found
    :return: Tuple containing the measure object and the table name
    """
    # Loop through each table in the model
    for table in data['model']['tables']:
        # Check if 'measures' key is present in the table
        if 'measures' in table:
            # Loop through each measure in the table
            for measure in table['measures']:
                # If the measure name matches the provided measure name, return measure object and table name
                if measure['name'] == measure_name:
                    return {'table': table['name'], 'measure': measure}
    
    # Measure not found, return None
    return None, None

def find_table_relationships(data, table_name):
    table_name = closest_table_name(data, table_name)
    """
    This function takes a JSON object representing the Tabular model of a Data Warehouse
    and a table name. It returns a list of relationship objects that the table is part of,
    either as a 'from' or 'to' table.
    
    :param data: JSON object representing the Tabular model of a Data Warehouse
    :param table_name: The name of the table to find relationships for
    :return: List of relationship objects involving the table
    """
    relationships_list = []
    
    # Loop through each relationship in the model
    for relationship in data['model']['relationships']:
        # Check if the table is part of the relationship, either as 'fromTable' or 'toTable'
        if relationship['fromTable'] == table_name or relationship['toTable'] == table_name:
            relationships_list.append(relationship)
    
    return {'table_name': table_name, 'relationships': relationships_list}

# You can call this function with the JSON object and a table name to find the relationships that include that table.

def get_tabular_measure(measureName):
    with open(os.environ['TABULAR_FILE_LOCATION']) as file:
        jsons = json.loads(file.read())
        return json.dumps(find_measure(jsons, measureName))

def get_tabular_table(tableName):
    with open(os.environ['TABULAR_FILE_LOCATION']) as file:
        jsons = json.loads(file.read())
        return json.dumps(find_table(jsons, tableName))

def get_tabular_table_relationships(tableName):
    with open(os.environ['TABULAR_FILE_LOCATION']) as file:
        jsons = json.loads(file.read())
        return json.dumps(find_table_relationships(jsons, tableName))
    
# print(get_tabular_table('utilisation'))