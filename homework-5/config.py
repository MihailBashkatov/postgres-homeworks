from configparser import ConfigParser

# Constanta with sql_database, json_file and name of database
script_file = 'fill_db.sql'
json_file = 'suppliers.json'
db_name = 'my_new_db'


def config(filename="database.ini", section="postgresql"):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db
