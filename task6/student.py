import csv


def get_students():

    n = int(input("Enter Number of Students (Minimum 5): "))

    if n < 5:
        print("Please enter at least 5 students.")
        return []

    students = []

    subject = ["Python", "Java", "PHP", "Linux", "DSA"]

    for i in range(n):

        print("\n--- Student", i + 1, "---")

        roll = int(input("Roll No: "))
        name = input("Name: ")

        total = 0

        for sub in subject:

            mark = int(input("Enter Marks in " + sub + ": "))

            if mark < 0 or mark > 100:
                print("Invalid Mark")
                return []

            total += mark

        percentage = total / 5

        if percentage >= 90:
            grade = "Distinction"
        elif percentage >= 80:
            grade = "First Division"
        elif percentage >= 70:
            grade = "Second Division"
        elif percentage >= 60:
            grade = "Pass"
        elif percentage >= 50:
            grade = "pass"
        else:
            grade = "Fail"

        students.append([roll, name, total, percentage, grade])

    return students


def save_csv(students):

    with open("students.csv", "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Roll No", "Name", "Total", "Percentage", "Grade"
        ])

        writer.writerows(students)