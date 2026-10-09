"""Student Rank Processing Engine using Functions and Modules
Develop a Python application to process and rank student records stored in an Excel file. 
Organize the application using user-defined modules and functions.
Input
The input Excel file contains the following fields:
Roll No
Name
Marks in Subject 1
Marks in Subject 2
Marks in Subject 3
Marks in Subject 4
Marks in Subject 5
Create the following modules:
student.py
Implement functions to:
Read student records from an Excel file.
Calculate the total marks and percentage for each student.
Assign grades based on the percentage.
Return the processed student records.
ranking.py
Implement functions to:
Rank students based on total marks.
Handle tied ranks correctly (e.g., 1, 2, 2, 4).
Sort students in descending order of marks.
Return the ranked student records.
report.py
Implement functions to:
Display the ranked student records in a formatted table.
Export the ranked results to a new Excel file.
main.py
The main program should:
1.Import the required functions from all modules.
2.Read student records from the input Excel file.
3.Calculate total marks, percentage, and grade for each student.
4.Generate student ranks while correctly handling ties.
5.Display the ranked result in rank order.
6.Export the final ranked result to another Excel file.
7.Handle file-related errors and invalid data using exception handling.
"""
from student import get_students, save_csv
from ranking import rank_students
from report import display_students, save_ranked_csv


try:

    students = get_students()

    if students:

        save_csv(students)

        students = rank_students(students)

        display_students(students)

        save_ranked_csv(students)

        print("\nCSV files created successfully.")

except ValueError:

    print("Please enter valid data.")

except FileNotFoundError:

    print("File not found.")
