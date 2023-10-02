import json

import psycopg2


def create_database(params: dict, db_name: str) -> None:
    """ Create database """

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
    cur.execute(f"CREATE DATABASE {db_name}")

    conn.close()


def execute_sql_script(cur, script_file) -> None:
    """ To fill database with data"""

    # Open and read the file as a single buffer
    fd = open(script_file, 'r')
    sql_file = fd.read()
    fd.close()

    # sqlFile is splitting per """ ); """ as simple """ ; """ limiting to perform instruction execution
    sql_commands = sql_file.split(');')
    for command in sql_commands[:-1]:

        # command is adding """ ) """ to have relevant syntax to execute instruction
        needed_command = command + ')'
        cur.execute(needed_command)


def create_suppliers_table(cur) -> None:
    """Create a table suppliers"""

    cur.execute("""
               CREATE TABLE suppliers
                   (
                    supplier_id SERIAL PRIMARY KEY,
                    company_name VARCHAR(255) NOT NULL,
                    contact_name VARCHAR(100) NOT NULL,
                    contact_title VARCHAR(50) NOT NULL,
                    country VARCHAR(50) NOT NULL,
                    state_or_region VARCHAR(50),
                    post_code VARCHAR(50),
                    city VARCHAR(50),
                    street VARCHAR(50),
                    phone VARCHAR(50),
                    fax VARCHAR(50),
                    homepage TEXT,
                    products VARCHAR(50)
                   )
                """
                )


def get_suppliers_data(json_file: str) -> list[dict]:
    """ Getting data from json file and return list of dicts"""

    with open(json_file, 'r', encoding='UTF-8') as json_file:
        data = json.load(json_file)
    return data


def insert_suppliers_data(cur, suppliers: list[dict]) -> None:
    """ Populating data to table suppliers from list of dicts."""

    for sup in suppliers:

        # key 'products' does have value as list of strings
        for product in sup["products"]:
            company_name = sup["company_name"]

            # key 'contact' does have value as string with different info, split by """ ; """
            contact_name = sup["contact"].split(', ')[0]
            contact_title = sup["contact"].split(', ')[1]

            # key 'address' does have value as string with different info, split by """ ; """
            country = sup["address"].split('; ')[0]
            state_or_region = sup["address"].split('; ')[1]
            post_code = sup["address"].split('; ')[2]
            city = sup["address"].split('; ')[3]
            street = sup["address"].split('; ')[4]
            phone = sup["phone"]
            fax = sup["fax"]
            homepage = sup["homepage"]
            products = product

            cur.execute(""" INSERT INTO suppliers 
                            (
                             company_name, 
                             contact_name,
                             contact_title,
                             country,
                             state_or_region,
                             post_code,
                             city,
                             street,
                             phone,
                             fax, 
                             homepage,
                             products
                             )
                            VALUES 
                            (
                             %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                             )                           
                         """,
                        (
                         company_name, contact_name, contact_title, country, state_or_region, post_code, city,
                         street, phone, fax, homepage, products
                         )
                        )


def add_foreign_keys(cur, json_file) -> None:
    """ Adding foreign key to the table products with reference to supplier_id"""

    # Create a new column supplier_id in the table products
    cur.execute(""" 
                    ALTER TABLE products ADD COLUMN supplier_id INTEGER
                """)

    # Creating list of dicts from json file
    data = get_suppliers_data(json_file)

    # Setting supplier_id as 0, which is incrementing each iteration
    supplier_id = 0

    # Adding to the table products supplier_id with matching products name in table products
    for sup in data:
        for product in (sup['products']):
            supplier_id += 1
            cur.execute("""
                            UPDATE products SET supplier_id = %s where product_name = %s
                        """, (supplier_id, product)
                        )
    # Adding foreign key to the table products with reference to supplier_id in the table suppliers
    cur.execute(""" 
                    ALTER TABLE products ADD CONSTRAINT fk_products_suppliers 
                    FOREIGN KEY(supplier_id) REFERENCES suppliers(supplier_id)
                """)
