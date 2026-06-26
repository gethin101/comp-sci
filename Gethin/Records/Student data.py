from dataclasses import dataclass
@dataclass

class Student: #define as Student
    #record info
    first_name:str
    last_name:str
    student_id:int
    school_year:int
    working_at_grade:0.0 #default
    email:str
    #(fields)

#----- students -----#

student1 = Student("Gethin", "Grice", 13579, 10, 4.0, "gethingrice@hotmail.com")
student2 = Student("Random", "Person", 24680, 9, 3.5, "random_person@yahoo.co.uk") #missing last as default


#----- access -------#

print()
print("========== Students: ============")
print()
print("Student 1:")
print (f'Student 1 name: {student1.first_name} {student1.last_name}')
print (f'Student 1 ID: {student1.student_id}')
print (f'Student 1 school year: {student1.school_year}')
print (f'Student 1 working at grade: {student1.working_at_grade}')
print (f'Student 1 email: {student1.email}')
print()

print("Student 2:")
print (f'Student 2 name: {student2.first_name} {student2.last_name}')
print (f'Student 2 ID: {student2.student_id}')
print (f'Student 2 school year: {student2.school_year}')
print (f'Student 2 working at grade: {student2.working_at_grade}')
print (f'Student 2 email: {student2.email}')
print()

#---- modifying a field ----#

print("====== Name modifications: =======")
student1.first_name="Gethino"
print (f'Student 1 name changed to: {student1.first_name}')
print("==================================")
print()

