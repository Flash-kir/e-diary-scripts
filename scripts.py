import sys
import random

from datacenter.models import Lesson, Schoolkid, Chastisement, Commendation, Mark


def get_schoolkid(schoolkid_name):
    schoolkid = Schoolkid.objects.filter(full_name__contains=schoolkid_name)
    if len(schoolkid) > 1:
        sys.exit('Найдено несколько учеников с таким именем, уточните имя')
    elif len(schoolkid) == 0:
        sys.exit(f'Ученик с именем "{schoolkid_name}" не найден, попробуйте снова')
    return schoolkid[0]


def get_random_lesson(schoolkid, lesson_name):
    lessons = Lesson.objects.filter(
            year_of_study=schoolkid.year_of_study, 
            group_letter=schoolkid.group_letter, 
            subject__title__contains=lesson_name)
    if len(lessons) == 0:
        sys.exit(f'Урок с именем "{lesson_name}" не найден, попробуйте снова')
    lesson = lessons[random.randint(0, len(lessons)-1)]
    return lesson
        

def get_random_commendation_text():
    commendations = Commendation.objects.all()
    return commendations[random.randint(0, len(commendations)-1)].text


def fix_marks(schoolkid_name):
    schoolkid = get_schoolkid(schoolkid_name)
    Mark.objects.filter(schoolkid=schoolkid.id, points__lte=3).update(points=5)


def remove_chastisements(schoolkid_name):
    schoolkid = get_schoolkid(schoolkid_name)
    chastisement = Chastisement.objects.filter(schoolkid=schoolkid.id)
    chastisement.delete()


def create_commendation(schoolkid_name, lesson_name, text=''):
    schoolkid = get_schoolkid(schoolkid_name)
    lesson = get_random_lesson(schoolkid, lesson_name)
    commendation = Commendation(
        schoolkid = schoolkid,
        teacher = lesson.teacher,
        subject = lesson.subject
    )
    if not text:
        commendation.text = get_random_commendation_text()
    else:
        commendation.text = text
    commendation.created = lesson.date
    commendation.save()
