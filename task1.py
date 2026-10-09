#practical no.1.py
#Consecutive duplicate detector
#Accept N integers.
#Display only those number that appear consecutively more than once.
#inpute:
#1 2 2 3 4 4 4 5
#output:
#2
#4
a=(1,2,2,3,4,4,4,5)
for i in set(a):
    if a.count(i) > 1:
        print(i)
