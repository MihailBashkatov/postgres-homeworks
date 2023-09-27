import psycopg2
customer_file = '../homework-1/north_data/customers_data.csv'
employees_file = '../homework-1/north_data/employees_data.csv'
order_file = '../homework-1/north_data/orders_data.csv'
base_connection = psycopg2.connect(host='localhost', database='north', user='postgres', password='12345')