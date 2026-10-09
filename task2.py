#practical no.2.py
#Missing Roll Number
#roll number should be from 1 to N.
#one roll number is missing.
#find the missing roll number without sorting.
#example:
#1 2 3 5 6
#output:
#4
k=(1,2,3,5,6)
for i in range(1,7):
    if i not in k:
        print(i) 
