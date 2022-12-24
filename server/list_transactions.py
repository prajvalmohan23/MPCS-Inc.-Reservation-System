from io import TextIOWrapper
import sys

ATTRIBUTES = ["Transaction ID", "Transaction Type", "Timestamp", "User ID"]
ATTRIBUTE_INDEX = [0, 1, 13, 14]
COLUMN_WIDTH = [16, 18, 18, 0]


def main():
    data_file = sys.argv[1]
    with open(data_file, "r") as data:
        transactions = parse_data(data)
        list_transactions(transactions)


def parse_data(data: TextIOWrapper):
    reached_transactions = False # a flag used to skip reservation data
    transactions = []
    lines = data.readlines()
    for line in lines:
        line = line.split()
        if len(line) == 0:
            # empty line is indicating end of file
            break
        if line[0] == '#': # delimeter between reservations and transactions
            reached_transactions = True
            continue
        if not reached_transactions:
            # skip reservation data
            continue
        transactions.append(parse_line(line))
    return transactions


def parse_line(line):
    transaction = []
    for i in range(len(ATTRIBUTES)):
        transaction.append(line[ATTRIBUTE_INDEX[i]])
    return transaction


def list_transactions(transactions):
    # print the title
    print_formatted_line(ATTRIBUTES, ' | ')
    # print transactions
    for transaction in transactions:
        print_formatted_line(transaction)


def print_formatted_line(line, delimeter='   '):
    new_line = []
    for i in range(len(ATTRIBUTES)):
        if i == 1:
            # handle the special case: "CANCELLATION$refund"
            new_line.append(line[i].split('$')[0].center(COLUMN_WIDTH[i]))
        elif i < len(ATTRIBUTES) - 1:
            # center all columns but the last one
            new_line.append(line[i].center(COLUMN_WIDTH[i]))
        else:
            # left just the last column
            new_line.append(line[i].ljust(COLUMN_WIDTH[i]))
    print(delimeter.join(new_line))


if __name__ == '__main__':
    main()