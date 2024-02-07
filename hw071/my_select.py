from sqlalchemy import func, desc

from src.models import Teacher, Student, Discipline, Grade, Group
from src.db import session


def select_1():
    result = session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
        .select_from(Grade)\
        .join(Student)\
        .group_by(Student.id)\
        .order_by(desc('avg_grade'))\
        .limit(5).all()
    return result

def select_2(discipline_id: int):
    result = session.query(Discipline.name, Student.fullname, func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
        .select_from(Grade)\
        .join(Student)\
        .join(Discipline)\
        .filter(Discipline.id == discipline_id)\
        .group_by(Student.id, Discipline.name)\
        .order_by(desc('avg_grade'))\
        .limit(1).all()
    return result

def select_3(discipline_id: int):
    result = session.query(Group.name, func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
        .select_from(Grade)\
        .join(Student)\
        .join(Discipline)\
        .join(Group)\
        .filter(Discipline.id == discipline_id)\
        .group_by(Group.name)\
        .all()
    return result

def select_4():
    result = session.query(func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
        .select_from(Grade)
    return result

def select_5(teacher_id: int):
    result = session.query(Discipline.name.label('discipline'))\
        .select_from(Discipline)\
        .join(Teacher)\
        .filter(Teacher.id == teacher_id)\
        .all()
    return result

def select_6(group_id: int):
    result = session.query(Student.fullname.label('student'))\
        .select_from(Student)\
        .join(Group)\
        .filter(Group.id == group_id)\
        .all()
    return result

def select_7(group_id: int, discipline_id: int):
    result = session.query(Student.fullname.label('student'), Grade.grade.label('grade'))\
        .select_from(Grade)\
        .join(Student)\
        .join(Discipline)\
        .join(Group)\
        .filter(Group.id == group_id, Discipline.id == discipline_id)\
        .order_by('student')\
        .all()
    return result

def select_8(teacher_id: int):
    result = session.query(Discipline.name.label('discipline'), func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
        .select_from(Grade)\
        .join(Discipline)\
        .join(Teacher)\
        .filter(Teacher.id == teacher_id)\
        .group_by(Discipline.name)\
        .order_by('discipline')\
        .all()
    return result

def select_9(student_id: int):
    result = session.query(Discipline.name.label('discipline'))\
        .select_from(Grade)\
        .join(Discipline)\
        .join(Student)\
        .filter(Student.id == student_id)\
        .group_by(Discipline.name)\
        .order_by('discipline')\
        .all()
    return result

def select_10(student_id: int, teacher_id: int):
    result = session.query(Discipline.name.label('discipline'))\
        .select_from(Grade)\
        .join(Discipline)\
        .join(Teacher)\
        .join(Student)\
        .filter(Student.id == student_id, Teacher.id == teacher_id)\
        .group_by(Discipline.name)\
        .order_by('discipline')\
        .all()
    return result

if __name__ == '__main__':
    result = select_10(4, 2)
    print(result)
    # for row in result:
    #     print(row)
