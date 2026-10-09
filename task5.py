"""Student Rank Processing Engine
3Develop a Python application that reads student records from User input.
Each record contains:
Roll No
Name
Marks in 5 subjects
The program must:
Compute total and percentage.
Assign grades.
Handle ties while assigning ranks (students with equal marks receive the same rank).
Display the next rank correctly (e.g., 1,2,2,4)."""


students = {}

subjects = ["Python", "linux", "Data structure", "java", "Computer Network"]

k = int(input("Enter number of students (minimum 5): "))

while k < 5:
    print("Please enter at least 5 students.")
    k = int(input("Enter number of students (minimum 5): "))

for i in range(k):
    roll = input("Roll No: ")
    name = input("Name: ")

    marks = []

    for sub in subjects:
        marks.append(int(input("Enter " + sub + " mark: ")))

    total = sum(marks)
    per = total / 5

    if per >= 90:
        grade = "A+"
    elif per >= 80:
        grade = "A"
    elif per >= 70:
        grade = "B"
    elif per >= 50:
        grade = "C"
    elif per >= 40:
        grade = "D"
    else:
        grade = "F"

    students[roll] = [name, total, per, grade]

data = sorted(students.items(), key=lambda x: x[1][1], reverse=True)

rank = 0
last = -1

print("\nRoll\tName\tTotal\tPercentage\tGrade\trank")

for i, (roll, s) in enumerate(data):

    if s[1] != last:
        rank = i + 1

    print(roll, "\t", s[0], "\t", s[1], "\t", s[2], "\t\t", s[3],"\t",rank)

    last = s[1]
    