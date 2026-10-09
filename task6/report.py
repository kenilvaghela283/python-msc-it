import csv


def display_students(students):

    print("\n========== Rank List ==========")
    print("Index | Rank | Roll No | Name | Total | Percentage | Grade")
    print("-" * 65)

    index = 1

    for student in students:

        print(
            index, "|",
            student[5], "|",
            student[0], "|",
            student[1], "|",
            student[2], "|",
            round(student[3], 2), "% |",
            student[4]
        )

        index = index + 1


def save_ranked_csv(students):

    with open("ranked_students.csv", "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Index",
            "Rank",
            "Roll No",
            "Name",
            "Total",
            "Percentage",
            "Grade"
        ])

        index = 1

        for student in students:

            writer.writerow([
                index,
                student[5],
                student[0],
                student[1],
                student[2],
                round(student[3], 2),
                student[4]
            ])

            index = index + 1