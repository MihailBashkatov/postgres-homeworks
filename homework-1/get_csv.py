import csv


def get_file_reader(file):
    """ CSV file is opening for reading and return array with  CSV rows"""

    with open(file, encoding='utf-8') as r_file:
        file_reader = csv.reader(r_file, delimiter=",")
        table_strings: list = []

        # First line is not added to the arrau
        count = 0
        for row in file_reader:
            if count == 0:
                count = 1
                continue
            else:
                table_strings.append(row)
    return table_strings
