import urllib.request
import requests
from bs4 import BeautifulSoup
import os
from sys import argv
import csv

URL = 'http://mkb-10.com/'


def get_icd10_classes(soup):
    classes_raw_content = soup.find('div', class_='content').find_all('a')
    icd10_class_names_and_links = [[raw_icd10_class['href'], raw_icd10_class['title']] for raw_icd10_class in classes_raw_content]
    return icd10_class_names_and_links


def get_icd10_subclasses(soup):
    subclasses_raw_content = soup.find('div', class_='content').find_all('div', class_='h2')
    icd10_subclass_names_and_links = [[raw_icd10_subclass.find('a')['href'], raw_icd10_subclass.find('a').contents[0]] for raw_icd10_subclass in subclasses_raw_content]
    return icd10_subclass_names_and_links


def get_subclass_group(soup):
    groups_raw_content = soup.find('div', class_='content').find_all('div', class_='h2')
    group_names_and_links = []
    for raw_group in groups_raw_content:
        if raw_group.find('a'):
            group_names_and_links.append([raw_group.find('a')['href'], raw_group.find('a').contents[0]])
        else:
            group_names_and_links.append([None, raw_group.find('div', class_=None).find('b').contents[0]])
    return group_names_and_links


def get_subclass_subgroup(soup):
    subgroups_raw_content = soup.find('div', class_='content').find_all('div', class_='h2')
    illnesses_or_subgroups = []

    for raw_subgroup in subgroups_raw_content:
        if raw_subgroup.find('a'):
            illnesses_or_subgroups.append([raw_subgroup.find('a')['href'], raw_subgroup.find('a').contents[0]])
        else:
            illnesses_or_subgroups.append([None, raw_subgroup.find('div', class_=None).find('b').contents[0]])
    return illnesses_or_subgroups


def get_illness(soup):
    illnesses_raw_content = soup.find('div', class_='content').find_all('div', class_='h2')
    illnesses = []
    for raw_illness in illnesses_raw_content:
        if raw_illness.find('div', class_=None).find('b') is None:
            print(raw_illness)
        else:
            illnesses.append(raw_illness.find('div', class_=None).find('b').contents[0])
    return illnesses


if __name__=="__main__":
    if len(argv) == 1:
        print("Enter filename to save: ")
        filename = input()
    else:
        filename = argv[1]
    page = urllib.request.urlopen(URL)
    soup = BeautifulSoup(page, "html.parser")
    icd10_class_names_and_links = get_icd10_classes(soup)
    for idx, link_to_class in enumerate([icd_10_class_and_link[0] for icd_10_class_and_link in icd10_class_names_and_links]):
        if link_to_class is None:
            continue
        full_url = URL[:-1] + link_to_class
        page = urllib.request.urlopen(full_url)
        soup = BeautifulSoup(page, "html.parser")
        icd10_subclass_names_and_links = get_icd10_subclasses(soup)
        icd10_class_names_and_links[idx].append(icd10_subclass_names_and_links)
        for jdx, link_to_subclass in enumerate([icd10_subclass_and_link[0] for icd10_subclass_and_link in icd10_subclass_names_and_links]):
            if link_to_subclass is None:
                continue
            full_url = URL[:-1] + link_to_subclass
            page = urllib.request.urlopen(full_url)
            soup = BeautifulSoup(page, "html.parser")
            #a = icd10_subclass_names_and_links[jdx][1]
            group_names_and_links = get_subclass_group(soup)
            icd10_class_names_and_links[idx][2][jdx].append(group_names_and_links)
            for kdx, link_to_subclass in enumerate(
                [group_and_link[0] for group_and_link in group_names_and_links]):
                if link_to_subclass is None:
                    continue
                full_url = URL[:-1] + link_to_subclass
                page = urllib.request.urlopen(full_url)
                soup = BeautifulSoup(page, "html.parser")
                #b = [group_and_link1[1] for group_and_link1 in group_names_and_links if group_and_link1[0] is not None][kdx]
                illnesses = get_subclass_subgroup(soup)
                icd10_class_names_and_links[idx][2][jdx][2][kdx].append(illnesses)
                for ldx, link_to_illness in enumerate([illness[0] for illness in illnesses]):
                    if link_to_illness is None:
                        continue
                    full_url = URL[:-1] + link_to_illness
                    page = urllib.request.urlopen(full_url)
                    soup = BeautifulSoup(page, "html.parser")
                    illnesses2 = get_illness(soup)
                    icd10_class_names_and_links[idx][2][jdx][2][kdx][2][ldx].append(illnesses2)

                    # print(icd10_class_names_and_links)