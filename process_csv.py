# Standard imports
import csv
import sys


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(
            "Missing CSV file input, example `python3 {} example.csv`".format(
                sys.argv[0]
            )
        )

    with open(sys.argv[1], "r") as _file:
        reader = csv.DictReader(_file)
        for row in reader:
            data = {
                key.lower().strip(): value.replace("$", "")
                for key, value in row.items()
            }
            # sqlalchemy insert data
