import sys
import os
import json
from collections import Counter
from math import log
import matplotlib.pyplot as plt

tokens_root_folder = "../good_tokens"

С = 3

def read_tokens_counter_from_file(filename):
    with open(filename, "r") as f:
        return json.load(f)


def zipf(first_freq_value):
    return lambda x: С * first_freq_value / x


def generate_counter_for_all_tokens():
    common_counter = Counter()
    for dirpath, dirnames, filenames in os.walk(tokens_root_folder):
        for filename in filenames:
            common_counter.update(
                read_tokens_counter_from_file(
                    os.path.join(tokens_root_folder, dirpath, filename)))
    return common_counter


def save_file_with_counter_for_all_tokens(filename, counter):
    with open(filename, "w+") as f:
        json.dump(counter, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    all_tokens_counter_filename = "../token_counter.json"

    if len(sys.argv) >= 2:
        all_tokens_counter_filename = sys.argv[1]
    counter = Counter()

    if not os.path.exists(all_tokens_counter_filename):
        counter = generate_counter_for_all_tokens()
        save_file_with_counter_for_all_tokens(all_tokens_counter_filename, counter)
    else:
        counter = Counter(read_tokens_counter_from_file(all_tokens_counter_filename))

    xlog_points = list(map(lambda x: log(x), [x for x in range(1, len(counter) + 1)]))
    x_points = [x for x in range(1, len(counter) + 1)]
    ylog_points = list(map(lambda y: log(y), sorted(counter.values(), reverse=True)))
    y_points = sorted(counter.values(), reverse=True)
    zipf_func = zipf(y_points[0])
    zipf_ylog_points = list(map(lambda y: log(y), list(map(zipf_func, x_points))))
    zipf_y_points = list(map(zipf_func, x_points))
    fig1 = plt.figure(1)
    line, = plt.plot(xlog_points, ylog_points,
                     label="Соотношение ранга и частоты на основе моего примера")
    line2, = plt.plot(xlog_points, zipf_ylog_points,
                      label="Соотношние ранга и частоты по закону Ципфа")
    plt.grid(True)
    plt.title(u'Закон Ципфа на логарифмической шкале')
    plt.xlabel(u'Ранг')
    plt.ylabel(u'Частота')

    fig1 = plt.figure(2)
    line, = plt.plot(x_points, y_points,
                     label="Соотношение ранга и частоты на основе моего примера")
    line2, = plt.plot(x_points, zipf_y_points,
                      label="Соотношние ранга и частоты по закону Ципфа")
    plt.grid(True)
    plt.title(u'Закон Ципфа на линейной шкале')
    plt.xlabel(u'Ранг')
    plt.ylabel(u'Частота')
    plt.show()
