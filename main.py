import json
import hashlib

# Satenik password - 1111
# All students passwords - 1234


def loadSetupData():
    with open('gc_setup.json') as data_file:
        course = json.load(data_file)

    grades = course["course_setup"]["grade_breakdown"]
    conv_matrix = course["course_setup"]["conv_matrix"]
    return grades, conv_matrix

def loadStudentGrades():
    try:
        file = open('gc_grades.json', 'r+')

        if file.readlines() == []:
            file.write("{}")
            file.close()
    except:
        file = open('gc_grades.json', 'w')
        file.write("{}")
        file.close()

    with open('gc_grades.json') as data_file:
        student_grades = json.load(data_file)

    return student_grades

def loadTeachers():
    try:
        file = open('gc_teachers.json', 'r+')

        if file.readlines() == []:
            file.write("{}")
            file.close()
    except:
        file = open('gc_teachers.json', 'w')
        file.write("{}")
        file.close()

    with open('gc_teachers.json') as data_file:
        teachers = json.load(data_file)

    return teachers

def askForUserInfo():
    user = raw_input("How you want to login as a teacher or as a student? ")
    name = raw_input("Please, input your name ")
    id = raw_input("Please, input your id ")
    password = raw_input("Please, input your password ")

    return user, name, id, password

def checkPassword(id, name, password, student_grades, teachers):
    m = hashlib.sha224(password).hexdigest()
    #SM - user type is provided by the user in step 1 and it is available in main. should be checked like this if user == "teacher":
    if id in student_grades.keys():
        try:
            while True:
                if m == student_grades[id]['user']['password']:
                    print "Welcome " + name
                    break
                else:
                    password = raw_input("Try again! ")
                    m = hashlib.sha224(password).hexdigest()
        except:
            pass
    else:
        try:
            while True:
                if m == teachers[id]['user']['password']:
                    print "Welcome " + name
                    break
                else:
                    password = raw_input("Try again! ")
                    m = hashlib.sha224(password).hexdigest()
        except:
            pass

    return m

def askForAssignmentMarks(user, grades, student_grades, id):
    if user == "Student" or user == "student":
        current_grades = {id: {"user": {}, "grades": {}}}
        for key in grades:
            if id in student_grades.keys():
                if student_grades[id]["grades"][key] > -1 :
                    student_input = raw_input("Your grade for " + key + " is " + str(student_grades[id]["grades"][key]) + ". Do you want to change it? ")
                    if student_input == "Yes" or student_input == "yes":
                        student_input = raw_input("What is your Current Grade for " + key + ". Please insert -1 if you don't have a grade yet ")
                        student_input = ValidInput(key, student_input)
                        ValidNumber(key, current_grades, student_input, id)
                    else:
                        current_grades[id]["grades"][key] = student_grades[id]["grades"][key]
                else:
                    student_input = raw_input("You have no grade for " + key + ". Please insert a grade or -1 again if you don't have a grade yet ")
                    student_input = ValidInput(key, student_input)
                    ValidNumber(key, current_grades, student_input, id)
            else:
                student_input = raw_input("What is your Current Grade for " + key + ". Please insert -1 if you don't have a grade yet ")
                student_input = ValidInput(key, student_input)
                ValidNumber(key, current_grades, student_input, id)
        return current_grades

def ValidNumber(key, current_grades, student_input, id):
    while True:
        if (student_input < 0 or student_input > 100) and student_input != -1:
            print "Wrong input! Input number from 0 to 100"
            student_input = raw_input("What is your Current Grade for " + key + ". Please insert -1 if you don't have a grade yet ")
            student_input = ValidInput(key, student_input)
        else:
            current_grades[id]["grades"][key] = student_input
            break

def ValidInput(key, student_input):
    while True:
        try:
            student_input = int(student_input)
            break
        except:
            print "Input a number!"
            student_input = raw_input("What is your Current Grade for " + key + ". Please insert -1 if you don't have a grade yet ")

    return student_input

def Teachers(teachers, student_grades, user, id, name, m):
    if user == "Teacher" or user == "teacher":
        if id in teachers.keys():
            print "Here is the list of all students and their grades:"
            for key in student_grades:
                print "Student id:", key
                print "Student name:", student_grades[key]['user']['name']
                print "Grades:"
                for i in student_grades[key]["grades"]:
                    print i,"-",student_grades[key]["grades"][i]
                print

            teacher_input = raw_input("Want to change someone's grade? ")
            if teacher_input == "Yes" or teacher_input == "yes":
                teacher_input = raw_input("Input the id of student whose grades you want to change ")
                assignment = raw_input("For which assignment you want to change the grade? Input end when finished ")
                while assignment != "end":
                    student_grades[teacher_input]["grades"][assignment] = int(raw_input("The current grade is " \
                                                                  + str(student_grades[teacher_input]["grades"][assignment]) + ". Enter the new grade "))
                    assignment = raw_input("For which assignment you want to change the grade? Input end when finished ")
            else:
                print "Have a nice day!"
        else:
            teachers[id] = {}
            teachers[id]['user'] = {}
            teachers[id]['user']['name'] = name
            teachers[id]['user']['password'] = m
            file = open("gc_teachers.json", "w")
            file.write(json.dumps(teachers))
            file.close()

    return student_grades

def saveGrades(student_grades, current_grades, name, id, m):
    try:
        student_grades[current_grades.keys()[0]] = current_grades[current_grades.keys()[0]]
        student_grades[id]['user']['name'] = name
        student_grades[id]['user']['password'] = m
        file = open("gc_grades.json", "w")
        file.write(json.dumps(student_grades))
        file.close()
    except:
        file = open("gc_grades.json", "w")
        file.write(json.dumps(student_grades))
        file.close()

def printCurrentGrade(grades, student_grades, id):
    curr_grade = 0
    for key in student_grades[id]["grades"]:
        if student_grades[id]["grades"][key] != -1:
            calc_grade = float(student_grades[id]["grades"][key]) * grades[key] / 100
            curr_grade = curr_grade + calc_grade

    return curr_grade

def matrix(curr_grade, conv_matrix):
    for i in range(len(conv_matrix)):
        if curr_grade >= int(conv_matrix[i]['min']):
            print curr_grade
            print conv_matrix[i]['mark']
            break

def main():
    grades, conv_matrix = loadSetupData()
    student_grades = loadStudentGrades()
    teachers = loadTeachers()
    user, name, id, password = askForUserInfo()
    #SM - Variable manes should be meaningful
    m = checkPassword(id, name, password, student_grades, teachers)
    current_grades = askForAssignmentMarks(user, grades, student_grades, id)
    student_grades = Teachers(teachers, student_grades, user, id, name, m)
    saveGrades(student_grades, current_grades, name, id, m)
    try:
        curr_grade = printCurrentGrade(grades, student_grades, id)
        matrix(curr_grade, conv_matrix)
    except:
        pass
main()