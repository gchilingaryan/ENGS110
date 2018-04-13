import json
import hashlib

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

def askForUserInfo(student_grades):
    name = raw_input("Please, input your name ")
    id = raw_input("Please, input your id ")
    password = raw_input("Please, input your password ")

    return name, id, password

def checkPassword(id, name, password, student_grades):
    m = hashlib.sha224(password).hexdigest()
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

    return m

def askForAssignmentMarks(grades, student_grades, id):
    current_grades = {id: {"user" : {}, "grades" : {}}}

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

def saveGrades(student_grades, current_grades, name, id, m):
    student_grades[current_grades.keys()[0]] = current_grades[current_grades.keys()[0]]
    student_grades[id]['user']['name'] = name
    student_grades[id]['user']['password'] = m
    file = open("gc_grades.json", "w")
    file.write(json.dumps(student_grades))
    file.close()

def printCurrentGrade(grades, current_grades, name, id):
    curr_grade = 0
    for key in current_grades[id]["grades"]:
        if current_grades[id]["grades"][key] != -1:
            calc_grade = float(current_grades[id]["grades"][key]) * grades[key] / 100
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
    name, id, password = askForUserInfo(student_grades)
    m = checkPassword(id, name, password, student_grades)
    current_grades = askForAssignmentMarks(grades, student_grades, id)
    saveGrades(student_grades, current_grades, name, id, m)
    curr_grade = printCurrentGrade(grades, current_grades, name, id)
    matrix(curr_grade, conv_matrix)
main()