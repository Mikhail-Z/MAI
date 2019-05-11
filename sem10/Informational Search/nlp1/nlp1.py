import nltk
import os
import time
from collections import Counter
import json

articles_root_folder = "/home/mikhail/Documents/InformationSearch"
root_folder_to_save_good_tokens = "../good_tokens"
root_folder_to_save_bad_tokens = "../bad_tokens"
bad_tokens = ["-", ",", "—", "«", "»", ".", "@", "!", "–", ";", "<", ">", "'", "?", ")", "("]

all_good_tokens_count = 0
all_good_tokens_length = 0
all_bad_tokens_count = 0
all_bad_tokens_length = 0


def split_text_in_good_tokens(text):
    l = [x for x in set(nltk.word_tokenize(text)) if x not in bad_tokens]
    global all_good_tokens_count
    global all_good_tokens_length
    all_good_tokens_count += len(l)
    all_good_tokens_length += sum(list(map(len, l)))
    return Counter([x for x in nltk.word_tokenize(text) if x not in bad_tokens]).most_common()


def split_text_in_bad_tokens(text):
    l = [x for x in set(nltk.word_tokenize(text))]
    global all_bad_tokens_count
    global all_bad_tokens_length
    all_bad_tokens_count += len(l)
    all_bad_tokens_length += sum(list(map(len, l)))
    return Counter([x for x in nltk.word_tokenize(text)]).most_common()


def read_file(filename):
    with open(filename, "r") as f:
        return f.read()


def generate_bad_tokens():
    for cur_dir, dirs, files in os.walk(articles_root_folder):
        for file in files:
            folder_to_save_tokens = os.path.join(root_folder_to_save_bad_tokens, cur_dir.split("/")[-1])
            if not os.path.exists(folder_to_save_tokens):
                os.mkdir(folder_to_save_tokens)
            with open(os.path.join(folder_to_save_tokens, file + ".json"), "w+") as f:
                text = read_file(os.path.join(cur_dir,  file))
                f.write(json.dumps(split_text_in_bad_tokens(text), ensure_ascii=False, indent=4))


def generate_good_tokens():
    for cur_dir, dirs, files in os.walk(articles_root_folder):
        for file in files:
            folder_to_save_tokens = os.path.join(root_folder_to_save_good_tokens, cur_dir.split("/")[-1])
            if not os.path.exists(folder_to_save_tokens):
                os.mkdir(folder_to_save_tokens)
            with open(os.path.join(folder_to_save_tokens, file + ".json"), "w+") as f:
                text = read_file(os.path.join(cur_dir,  file))
                f.write(json.dumps(split_text_in_good_tokens(text), ensure_ascii=False, indent=4))


def main():
    time1 = time.time()
    generate_bad_tokens()
    time2 = time.time()
    print("Кол-во всех токенов: {}".format(all_bad_tokens_count))
    print("Средняя длина всех токенов: {}".format(all_bad_tokens_length / all_bad_tokens_count))
    print('{:s} function took {:.3f} ms'.format(generate_bad_tokens.__name__, (time2 - time1) * 1000.0))

    time1 = time.time()
    generate_good_tokens()
    time2 = time.time()
    print("Кол-во хороших токенов: {}".format(all_good_tokens_count))
    print("Средняя длина хороших токенов", all_good_tokens_length / all_good_tokens_count)
    print('{:s} function took {:.3f} ms'.format(generate_good_tokens.__name__, (time2 - time1) * 1000.0))


if __name__=="__main__":
    main()