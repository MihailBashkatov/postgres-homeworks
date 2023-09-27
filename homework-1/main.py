"""Скрипт для заполнения данными таблиц в БД Postgres."""
# import csv
import get_csv
import config


def create_database():
    """ Function is operating for fill data into sql tables from csv_files"""

    try:

        # Connection to db
        with config.base_connection:
            with config.base_connection.cursor() as working_cursor:

                # Getting array from csv file
                customer_data = get_csv.get_file_reader(config.customer_file)

                # Filling data to sql table from array
                for row in customer_data:
                    working_cursor.execute('INSERT INTO customers VALUES (%s, %s, %s)', row)

                # Getting array from csv file
                employees_data = get_csv.get_file_reader(config.employees_file)

                # Filling data to sql table from array
                for row in employees_data:
                    working_cursor.execute('INSERT INTO employees VALUES (%s, %s, %s, %s, %s, %s)', row)

                # Getting array from csv file
                orders_data = get_csv.get_file_reader(config.order_file)

                # Filling data to sql table from array
                for row in orders_data:
                    working_cursor.execute('INSERT INTO orders VALUES (%s, %s, %s, %s, %s)', row)

    # Closing bd connection
    finally:
        config.base_connection.close()


if __name__ == "__main__":
    create_database()
