from datetime import datetime


from sqlalchemy.orm import joinedload, subqueryload
from sqlalchemy import and_


from src.db import session
from src.models import ContactPerson, Student, Teacher, TeacherStudent


# many to many
def get_student():
    students = session.query(Student).join(Student.teachers).all()
    for st in students:
        print(f'id: {st.id}, name: {st.first_name} {st.last_name}, email: {st.email}')
        print(f'{[t.full_name for t in st.teachers]}')
    

    #  один раз до бази
def get_student_load():
    students = session.query(Student).options(joinedload(Student.teachers)).all()
    for st in students:
        print(f'id: {st.id}, name: {st.first_name} {st.last_name}, email: {st.email}')
        print(f'{[t.full_name for t in st.teachers]}')

            
#  без дублей 2 зпроса из-за join
def get_student_sub():
    students = session.query(Student).options(subqueryload(Student.teachers)).all()
    for st in students:
        print(f'id: {st.id}, name: {st.first_name} {st.last_name}, email: {st.email}')
        print(f'{[t.full_name for t in st.teachers]}')



def get_contacts_load():
    students = session.query(Student).options(joinedload(Student.teachers), joinedload(Student.contacts))\
        .limit(5).all()
    for st in students:
        print(f'id: {st.id}, name: {st.first_name} {st.last_name}, email: {st.email}')
        print(f'{[t.full_name for t in st.teachers]}')
        print(f'{[c.full_name for c in st.contacts]}')
        

def get_teachers():
    teachers = session.query(Teacher).options(subqueryload(Teacher.students))\
        .filter(and_(Teacher.start_work > datetime(year = 2021, month = 6, day = 15),
                     Teacher.start_work > datetime(year = 2022, month = 1, day = 1))).all()
    for t in teachers:
        print(f'id: {t.id}, name: {t.first_name} {t.last_name}, email: {t.email}')
        print(f'{[st.full_name for st in t.students]}')
                            

# все через табличку звязку
def get_students_full():
    students = session.query(Student.id, Student.full_name, Teacher.full_name, ContactPerson.full_name)\
        .select_from(Student).join(TeacherStudent).join(Teacher).join(ContactPerson).all()
    print(students)


if __name__ == '__main__':
   get_students_full()