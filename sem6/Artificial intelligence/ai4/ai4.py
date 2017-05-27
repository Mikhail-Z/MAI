#!/usr/bin/python
apikey = ''
import vk
from dateutil import parser, relativedelta
import datetime
import cognitive_face as FaceAPI
import time
import json
import csv
import re
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
FaceAPI.Key.set(apikey)
APP_ID = None
api = None
user_id = 187398690
avg_age = 21
import http.client, urllib.request, urllib.parse, urllib.error, base64

headers = {
    # Request headers. Replace the key below with your subscription key.
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': apikey,
}

params = urllib.parse.urlencode({
    # Request parameters. All of them are optional.
    # 'visualFeatures': 'Categories',
    # 'details': 'Celebrities',
    # 'language': 'en',
})


def get_user_password():
    password = input()
    print()
    return password


def get_friends(login, password):
    global api
    global avg_age
    session = vk.AuthSession(
        app_id=APP_ID,
        user_login=login,
        user_password=password
    )
    api = vk.API(session)
    data = api.users.get(user_id=user_id, fields="bdate")
    if 'bdate' in data[0] and re.match(r"[\d]{1,2}\.[\d]{1,2}\.[\d]{2,4}", data[0]['bdate']):
        str_date = re.sub(r'[.]', '', data[0]['bdate'])
        date = datetime.datetime.strptime(str_date, "%d%m%Y")
        avg_age = relativedelta.relativedelta(datetime.date.today(), date.date()).years

    friends = api.friends.get(user_id=user_id, order="hints")
    return friends


def get_most_score_obj(categories):
    imax = 0
    max_score = 0.0
    n = len(categories)
    if n == 0:
        return None

    for i in range(len(categories)):
        score = float(categories[i]["score"])
        if score > max_score:
            imax = i
            max_score = score
    return categories[imax]["name"]


def pretty_print_json(data):
    print(json.dumps(data, ensure_ascii=False, indent=4))


import linecache
import sys

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))


def get_user_info(person):
    id = person
    global avg_age
    data = None
    while data is None:
        try:
            data = api.users.get(user_id=id, fields="sex")
        except:
            time.sleep(2)
    if 'deactivated' in data[0]:
        return None
    if data[0]["sex"] == 1:
        sex = 1
    elif data[0]["sex"] == 2:
        sex = 2
    else:
        sex = 0
    data = None
    while data is None:
        try:
            data = api.users.get(user_id=id, fields="bdate")
        except:
            time.sleep(2)

    print(data[0])
    if 'bdate' in data[0] and re.match(r"[\d]{1,2}\.[\d]{1,2}\.[\d]{2,4}", data[0]['bdate']):
        str_date = re.sub(r'[.]', '', data[0]['bdate'])
        date = datetime.datetime.strptime(str_date, "%d%m%Y")
        age = relativedelta.relativedelta(datetime.date.today(), date.date()).years
        if int(age) > 100:
            age = avg_age
    else:
        age = avg_age
    friends_num = None
    while friends_num is None:
        try:
            friends_num = len(api.friends.get(user_id=id))
        except:
            time.sleep(2)

    photos = None
    while photos is None:
        try:
            photos = api.photos.get(owner_id=id, album_id="wall", count=100)
        except:
            time.sleep(5)
    count = 0
    time.sleep(1)
    info = {"uid": id, "age": age, "sex": sex, "friends count": friends_num}
    conn = http.client.HTTPSConnection('westeurope.api.cognitive.microsoft.com')
    for i in range(len(photos)):
        photo_src = photos[i]['src']
        body = "{'url': '" + photo_src + "'}"
        try:
            conn.request("POST", "/vision/v1.0/analyze?%s" % params, body, headers)
            response = conn.getresponse()
            data = response.read().decode()
            decoded_json = json.loads(data)
            while 'statusCode' in decoded_json and decoded_json['statusCode'] == 429:
                time.sleep(2)
                conn.request("POST", "/vision/v1.0/analyze?%s" % params, body, headers)
                response = conn.getresponse()
                data = response.read().decode()
                decoded_json = json.loads(data)
            print(decoded_json)
            categories_list = decoded_json["categories"]
            if "animal_cat" in categories_list[0]['name']:
                count += 1
            conn.close()
        except:
            PrintException()
        time.sleep(1)
    info["cats count"] = count
    return info


def get_friends_info(users):
    info_list = []
    for f in users:
        i = get_user_info(f)
        if i is not None:
            info_list.append(i)
    return info_list


def save_info(filename, info):
    csv_file = open(filename, 'w')
    dictwriter = csv.DictWriter(csv_file, fieldnames=["uid", "age", "sex", "friends count", "cats count"])
    dictwriter.writeheader()
    dictwriter.writerows(info)
    csv_file.close()


def load_info(filename):
    csv_file = open("vkdata.csv", 'r')
    dictReader = csv.DictReader(csv_file)
    data = []
    for row in dictReader:
        data.append(dict(row))
    csv_file.close()
    return data


def catsCounter(params, cats_counts):
    counter = {}
    for i in range(len(params)):
        if params[i] == 2:
            print(cats_counts[i])
        if params[i] in counter:
            counter[params[i]] += cats_counts[i]
        else:
            counter[params[i]] = cats_counts[i]

    return counter


if __name__ == "__main__":
    login = get_user_login()
    password = get_user_password()
    friends = get_friends(login, password)
    friends_info = get_friends_info(friends)
    save_info("vkdata.csv", friends_info)
    data = load_info("vkdata.csv")
    ages = []
    sexes = []
    friends_counts = []
    cats_counts = []
    for human in data:
        ages.append(int(human["age"]))
        sexes.append(int(human["sex"]))
        friends_counts.append(int(human["friends count"]))
        cats_counts.append(int(human["cats count"]))

    fig = plt.figure(edgecolor="black", frameon=True)
    cats_counter_from_age = catsCounter(ages, cats_counts)
    items_list = [cats_counter_from_age[x] for x in cats_counter_from_age.keys()]
    plt.title("Dependence of the number of cats on age")
    bar = plt.bar(list(cats_counter_from_age.keys()), items_list, color="green")
    plt.xlabel('age')
    plt.ylabel('count of cats')
    plt.grid(True)

    fig = plt.figure(edgecolor="black", frameon=True)
    cats_counter_from_sex = catsCounter(sexes, cats_counts)
    items_list = [cats_counter_from_sex[x] for x in cats_counter_from_sex.keys()]
    plt.title("Dependence of the number of cats on sex")
    plt.xticks([0, 1, 2], ["N/A", "female", "male"])
    bar = plt.bar(list(cats_counter_from_sex.keys()), items_list, color="red")
    plt.xlabel('sex')
    plt.ylabel('count of cats')
    plt.grid(True)

    fig = plt.figure(edgecolor="black", frameon=True)
    cats_counter_from_friends = catsCounter(friends_counts, cats_counts)
    items_list = [cats_counter_from_friends[x] for x in cats_counter_from_friends.keys()]
    plt.title("Dependence of the number of cats on number of friends")
    line = plt.scatter(list(cats_counter_from_friends.keys()), items_list, color="blue")
    plt.xlabel('friends count')
    plt.ylabel('count of cats')
    plt.grid(True)

    plt.show()


