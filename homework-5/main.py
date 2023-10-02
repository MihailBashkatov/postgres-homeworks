from config import *

from utils import *


def main():
    """ Execution main script"""

    # Getting parametres for connection with database
    params = config()

    # Creating database
    create_database(params, db_name)
    print(f"Database {db_name} created successfully")

    # Adding new database as constanta to parameters
    params.update({'dbname': db_name})

    try:
        # Connection to new database
        with psycopg2.connect(**params) as conn:

            # Creating cursor
            with conn.cursor() as cur:

                # Fill in database
                execute_sql_script(cur, script_file)
                print(f"Database {db_name} filled successfully")

                # Create table supplier
                create_suppliers_table(cur)
                print("Table suppliers created successfully")

                # Get list of dicts from json_file
                suppliers = get_suppliers_data(json_file)

                # Add data from json_file to the table suppliers
                insert_suppliers_data(cur, suppliers)
                print("Data added successfully to the table suppliers")

                # Adding foreign key to the table products with reference supplier_id to the table suppliers
                add_foreign_keys(cur, json_file)
                print(f"FOREIGN KEY added successfully")

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    # Running script
    main()
