#!/bin/sh
# Splitting procedure for the Post CSV file containing multiple tables

# Parse arguments
FOLDER=$1
CSV_FILE=$2

# Split the files
for i in 0 1 2 3 4 5 6 7 8
do
  echo "LOG | Extracting rows for table 0$i"
  grep -E "^0$i;*" "$FOLDER/$CSV_FILE" > "$FOLDER/0$i.csv"
done