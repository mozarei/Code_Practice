import csv


f = "/Users/moe/Desktop/Code_Practice/SCale_Interview_Practice/Day_1_ML_Coding_Practice/output/train.csv"
with open(f, "r") as file:
    reader = csv.DictReader(file)

    # print(f"Type {type(reader)}")
    num_row = 0
    for row in reader:
        num_row += 1

    num_col = len(reader.fieldnames)

    print(f"Shape is: {num_row, num_col}")
