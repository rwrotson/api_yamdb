#!/usr/bin/env python

"""
    Script to import book data from .csv file to Model Database DJango
    To execute this script run: 
                                1) manage.py shell
                                2) exec(open('import_data_csv.py').read())
                                
"""

import csv
from api.models import Category, Comment, Review, Title, CustomUser

CustomUser.objects.all().delete()
Title.objects.all().delete()
Category.objects.all().delete()
Review.objects.all().delete()
Comment.objects.all().delete()

CSV_PATH = '../data/users.csv'
contSuccess = 0
with open(CSV_PATH, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    next(spamreader)
    print('Loading...')
    for row in spamreader:
        CustomUser.objects.create(id=row[0], username=row[1], email=row[2], role=row[3])
        contSuccess += 1
    print(f'{str(contSuccess)} inserted successfully! ')

CSV_PATH = '../data/category.csv'
contSuccess = 0
with open(CSV_PATH, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    next(spamreader)
    print('Loading...')
    for row in spamreader:
        Category.objects.create(id=row[0], name=row[1], slug=row[2])
        contSuccess += 1
    print(f'{str(contSuccess)} inserted successfully! ')

CSV_PATH = '../data/titles.csv'
contSuccess = 0
with open(CSV_PATH, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    next(spamreader)
    print('Loading...')
    for row in spamreader:
        Title.objects.create(id=row[0], name=row[1], year=row[2], category=Category.objects.get(id=row[3]))
        contSuccess += 1
    print(f'{str(contSuccess)} inserted successfully! ')

CSV_PATH = '../data/review.csv'
contSuccess = 0
with open(CSV_PATH, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    next(spamreader)
    print('Loading...')
    for row in spamreader:
        Review.objects.create(id=row[0], title=Title.objects.get(id=row[1]), text=row[2], author=CustomUser.objects.get(id=row[3]), score=row[4], pub_date=row[5])
        contSuccess += 1
    print(f'{str(contSuccess)} inserted successfully! ')

CSV_PATH = '../data/comments.csv'
contSuccess = 0
with open(CSV_PATH, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    next(spamreader)
    print('Loading...')
    for row in spamreader:
        Comment.objects.create(id=row[0], review=Review.objects.get(id=row[1]), text=row[2], author=CustomUser.objects.get(id=row[3]), pub_date=row[4])
        contSuccess += 1
    print(f'{str(contSuccess)} inserted successfully! ')
