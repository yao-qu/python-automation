import os
import csv
import argparse
from argparse import ArgumentParser
import os.path
import re
parser = ArgumentParser()
parser.add_argument('--i', dest='TXT_LOCATION',
                    help='Kindle clippings txt file')
parser.add_argument('--o', dest='CSV_LOCATION', help='Output file location')

parser.add_argument('--e', dest='EXISTS', default=1, type=int, choices=[0, 1],
                    help='0 to add highlight to existing file, 1 to create new file')


if __name__ == "__main__":
    args = parser.parse_args()

    OUTPUT = "Clippings saved successfully in " + args.CSV_LOCATION

    preExist = 1 if args.EXISTS == 1 else 0
    if args.EXISTS == 1:

        if os.path.exists(args.CSV_LOCATION):
            print("Cannot create a new CSV output, file already exists!")

        else:
            COLUMNS = ['Title', 'Author', 'Location', 'Added', 'Highlight']

            with open(args.CSV_LOCATION, 'w', newline='') as CSV:
                writer = csv.writer(CSV)
                writer.writerow(COLUMNS)

            args.EXISTS = 0
            preExist = 0

    if args.EXISTS == 0 and os.path.exists(args.TXT_LOCATION) and os.path.exists(args.CSV_LOCATION):
        try:

            with open(args.TXT_LOCATION, mode='r', encoding='utf-8-sig') as TXT:
                content = [x.strip() for x in TXT.readlines()]

                for i in range(0, len(content), 5):
                    title_author = content[i].split(' (')
                    title, author = title_author[0].replace(
                        '\ufeff', ''), title_author[1][:-1]
                    location_date = content[i+1].split('|')
                    location = re.findall('[0-9]\w+', location_date[0])
                    location = "-".join(location)
                    date = location_date[1].split(', ')[1]
                    highlight = content[i+3]
                    with open(args.CSV_LOCATION, 'a', encoding='utf-8') as CSV:
                        writer = csv.writer(CSV)
                        writer.writerow(
                            [title, author, location, date, highlight])
            print(OUTPUT)
        except OSError as e:
            print(e.errno)

    else:
        print("ERROR: check file paths")
        if preExist == 0:
            os.remove(args.CSV_LOCATION)
