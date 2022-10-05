import sys

from datacenter.models import Lesson, Schoolkid, Chastisement, Commendation, Mark


def get_schoolkid(schoolkid_name):
    try:
        return Schoolkid.objects.get(full_name__contains=schoolkid_name)
    except:
        sys.exit(f'Ученик с именем {schoolkid_name} не найден')
        


def get_lessons(schoolkid, lesson_name):
    try:
        return Lesson.objects.get(
            year_of_study=schoolkid.year_of_study, 
            group_letter=schoolkid.group_letter, 
            subject__title__contains=lesson_name)
    except:
        sys.exit(f'Урок с именем {lesson_name} не найден')
        


def fix_marks(schoolkid_name):
    schoolkid = get_schoolkid(schoolkid_name)
    for mark in Mark.objects.filter(schoolkid=schoolkid.id, points__lte=3):
        mark.points = 5
        mark.save()


def remove_chastisements(schoolkid_name):
    schoolkid = get_schoolkid(schoolkid_name)
    chastisement = Chastisement.objects.filter(schoolkid=schoolkid.id)
    chastisement.delete()


def create_commendation(schoolkid_name, lesson_name, text='хвалю'):
    schoolkid = get_schoolkid(schoolkid_name)
    lesson = get_lessons(schoolkid, lesson_name)[0]
    commendation = Commendation()
    commendation.schoolkid = schoolkid
    commendation.teacher = lesson.teacher
    commendation.subject = lesson.subject
    commendation.text = text
    commendation.created = lesson.date
    commendation.save()
