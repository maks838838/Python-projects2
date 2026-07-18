import csv
from collections import Counter
humans = []
scounter = Counter()
fcounter = Counter()
counter = Counter()
survived_counter = Counter()
with open("train.csv") as file:
    reader = csv.reader(file)
    next(reader)  # Skip header
    for line in reader:
        PassengerId, Survived, Pclass, Name, Sex, Age, SibSp, Parch, Ticket, Fare, Cabin, Embarked = line
        people = {"PassengerId": PassengerId, "Survived": Survived, "Pclass": Pclass, "Name": Name, "Sex": Sex , "Age": Age, "SibSp": SibSp, "Parch": Parch, "Ticket":Ticket, "Fare": Fare, "Cabin": Cabin, "Embarked": Embarked
}   
        humans.append(people)
        survived_counter[Survived] += 1

        if Survived == "1":
            counter[Sex] +=1
        scounter[Sex] +=1
            

print(survived_counter) 
print(counter)
print(scounter)
male_percent = counter["male"] / scounter["male"] * 100
female_percent = counter["female"] / scounter["female"] * 100

print(f"Male survival rate: {male_percent:.2f}%")
print(f"Female survival rate: {female_percent:.2f}%")
   ## for people in humans:
    ##    print(f"{people['Survived']}")
    

