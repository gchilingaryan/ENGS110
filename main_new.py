import json

def loadSetupData():
    with open('gc_setup.json') as data_file:
        course = json.load(data_file)

    grades = course["course_setup"]["grade_breakdown"]
    conv_matrix = course["course_setup"]["conv_matrix"]
    return grades, conv_matrix

def loadStudentGrades():
    with open('gc_grades.json') as data_file:
        student_grades = json.load(data_file)

    name = raw_input("Please, input your name ")

    return student_grades, name

def askForAssignmentMarks(grades, student_grades, name):
    current_grades = {name: {}}

    for key in grades:
        if student_grades[name][key] > -1 :
            student_answer = raw_input("Your grade for " + key + " is " + str(student_grades[name][key]) + ". Do you want to change it?")
            if student_answer == "Yes" or student_answer == "yes":
                student_new_grade = int(raw_input("Insert your new grade for " + key))
                if (student_new_grade >= 0 and student_new_grade <= 100) or student_new_grade == -1:
                    current_grades[name][key] = student_new_grade
                else:
                    print "Wrong input! Input number from 0 to 100"
            else:
                current_grades[name][key] = student_grades[name][key]
        else:
            student_current_grade = int(raw_input("What is your Current Grade for: " + key + " . Please insert -1 if you don't have a grade yet"))
            if (student_current_grade >= 0 or student_current_grade <= 100) or student_current_grade == -1:
                current_grades[name][key] = student_current_grade
            else:
                print "Wrong input! Input number from 0 to 100"
    return current_grades

def saveGrades(student_grades, current_grades):
    student_grades[current_grades.keys()[0]] = current_grades[current_grades.keys()[0]]
    print (json.dumps(student_grades))
    file = open("gc_grades.json", "w")
    file.write(json.dumps(student_grades))
    file.close()

def printCurrentGrade(grades, current_grades, name):
    curr_grade = 0
    for key in current_grades[name]:
        if current_grades[name][key] != -1:
            calc_grade = int(current_grades[name][key]) * grades[key] / 100
            curr_grade = curr_grade + calc_grade

    return curr_grade

def matrix(curr_grade, conv_matrix):
    for i in range(len(conv_matrix)):
        if float(curr_grade) >= int(conv_matrix[i]['min']):
            print float(curr_grade)
            print conv_matrix[i]['mark']
            break

def main():
    grades, conv_matrix = loadSetupData()
    student_grades, name = loadStudentGrades()
    current_grades = askForAssignmentMarks(grades, student_grades, name)
    saveGrades(student_grades, current_grades)
    curr_grade = printCurrentGrade(grades, current_grades, name)
    matrix(curr_grade, conv_matrix)

main()