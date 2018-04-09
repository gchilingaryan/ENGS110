import json

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

    name = raw_input("Please, input your name ")
    id = raw_input("Please, input your id ")

    return student_grades, name, id

def askForAssignmentMarks(grades, student_grades, id):
    current_grades = {id: {}}

    for key in grades:
        if id in student_grades.keys():
            if student_grades[id][key] > -1 :
                student_answer = raw_input("Your grade for " + key + " is " + str(student_grades[id][key]) + ". Do you want to change it? ")
                if student_answer == "Yes" or student_answer == "yes":
                    student_new_grade = int(raw_input("What is your Current Grade for " + key + ". Please insert -1 if you don't have a grade yet "))
                    checkNumber(key, current_grades, student_new_grade, id)
                else:
                    current_grades[id][key] = student_grades[id][key]
        else:
            student_new_grade = int(raw_input("What is your Current Grade for " + key + ". Please insert -1 if you don't have a grade yet "))
            checkNumber(key, current_grades, student_new_grade, id)
    return current_grades

def checkNumber(key, current_grades, student_new_grade, id):
    while True:
        if (student_new_grade < 0 or student_new_grade > 100) and student_new_grade != -1:
            print "Wrong input! Input number from 0 to 100"
            student_new_grade = int(raw_input("What is your Current Grade for " + key + ". Please insert -1 if you don't have a grade yet "))
        else:
            current_grades[id][key] = student_new_grade
            break


def saveGrades(student_grades, current_grades, name, id):
    student_grades[current_grades.keys()[0]] = current_grades[current_grades.keys()[0]]
    student_grades[id]['name'] = name
    print (json.dumps(student_grades))
    file = open("gc_grades.json", "w")
    file.write(json.dumps(student_grades))
    file.close()

def printCurrentGrade(grades, current_grades, name, id):
    curr_grade = 0
    for key in current_grades[id]:
        if current_grades[id][key] != -1:
            if not current_grades[id][key] == name:
                calc_grade = float(current_grades[id][key]) * grades[key] / 100
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
    student_grades, name, id = loadStudentGrades()
    current_grades = askForAssignmentMarks(grades, student_grades, id)
    saveGrades(student_grades, current_grades, name, id)
    curr_grade = printCurrentGrade(grades, current_grades, name, id)
    matrix(curr_grade, conv_matrix)
main()