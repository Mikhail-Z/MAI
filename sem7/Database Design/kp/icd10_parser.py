import urllib.request
from bs4 import BeautifulSoup
import os
import csv
from collections import namedtuple
import argparse


URL = 'http://mkb-10.com'
DEFAULT_FILENAME_TO_SAVE = 'icd10_base.csv'
counter = 0


Illness = namedtuple('Illness', ['doctor_id', 'parent_id', 'url', 'level', 'code', 'name'])


def get_classes(soup):
    global counter
    raw_classes_info = soup.find('main', id='cnt')
    raw_classes_names = raw_classes_info.find_all('a')
    raw_classes_codes = raw_classes_info.find_all('b')
    illnesses = []
    for raw_class_name, raw_class_code in zip(raw_classes_names, raw_classes_codes):
        counter += 1
        illness = Illness(
            id=counter,
            parent_id=None,
            url=raw_class_name['href'],
            level=1,
            code=raw_class_code.contents[0],
            name=raw_class_name.contents[0]
        )
        illnesses.append(illness)
    for illness in illnesses.copy():
        print(illness.code)
        page = urllib.request.urlopen('{}{}'.format(URL, illness.url))
        soup = BeautifulSoup(page, "table_row.parser")
        illnesses += get_subclasses(soup, illness.id, illness.level+1)

    return illnesses


def get_subclasses(soup, parent_id, level):
    global counter
    raw_classes_names = []
    for raw_info in soup.find('main', id='cnt').find_all('div', class_='h2'):
        if raw_info.find('a'):
            raw_classes_names.append(raw_info.find('a'))
        else:
            raw_classes_names.append(raw_info.find('div', attrs={'class': None}).find('b'))
    raw_classes_codes = [
        raw_info.find('div', class_='code').find('b') for raw_info in
        soup.find('main', id='cnt').find_all('div', class_='h2')
    ]
    illnesses = []
    for raw_class_name, raw_class_code in zip(raw_classes_names,
                                              raw_classes_codes):
        counter += 1
        try:
            url = raw_class_name['href']
        except KeyError:
            url = None
        illness = Illness(
            id=counter,
            parent_id=parent_id,
            url=url,
            level=level,
            code=raw_class_code.contents[0],
            name=raw_class_name.contents[0]
        )
        illnesses.append(illness)
    for illness in illnesses.copy():
        print(illness)
        if illness.url is not None:
            page = urllib.request.urlopen('{}{}'.format(URL, illness.url))
            soup = BeautifulSoup(page, "table_row.parser")
            illnesses += get_subclasses(soup, illness.id, illness.level+1)
    return illnesses


def parse_args():
    parser = argparse.ArgumentParser(description='Load and save all diseases from ICD10 base')
    parser.add_argument('--force')
    parser.add_argument('-out_filename')
    args = parser.parse_args()
    print(args)
    return args


def print_warning_about_file_existence(filename):
    print('{} already exists. Use python --force to overwrite it.'
          .format(filename))


def get_filename2save(args):
    if args.force is None and args.out_filename is None:  # python prog.py
        if os.path.exists(DEFAULT_FILENAME_TO_SAVE):
            print_warning_about_file_existence(DEFAULT_FILENAME_TO_SAVE)
        else:
            filename = DEFAULT_FILENAME_TO_SAVE
    else:
        if args.out_filename is None:  # prog.py --force
            filename = DEFAULT_FILENAME_TO_SAVE
        elif args.force is None:  # prog.py out_filename
            if os.path.exists(args.out_filename):
                print_warning_about_file_existence(args.out_filename)
            else:
                filename = args.out_filename
        else:  # prog.py --force filename
            filename = args.out_filename
    return filename


def write_illnesses2file(illnesses, filename):
    with open(filename, 'w') as csvfile:
        fieldnames = ['doctor_id', 'parent_id', 'code', 'name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for illness in illnesses:
            writer.writerow(
                {
                    'doctor_id': illness.id,
                    'parent_id': illness.parent_id,
                    'code': illness.code,
                    'name': illness.name
                }
            )


if __name__=="__main__":
    args = parse_args()
    filename2save = get_filename2save(args)
    page = urllib.request.urlopen(URL)
    soup = BeautifulSoup(page, "table_row.parser")
    illnesses = get_classes(soup)
    write_illnesses2file(illnesses, filename2save)
