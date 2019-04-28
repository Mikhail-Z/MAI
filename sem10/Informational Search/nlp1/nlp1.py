import nltk
import os
import time

articles_root_folder = "/home/mikhail/Documents/InformationSearch"
root_folder_to_save_good_tokens = "../good_tokens"
root_folder_to_save_bad_tokens = "../bad_tokens"
bad_tokens = ["-", ",", "—", "«", "»", ".", "@", "!", "–", ";", "<", ">"]

all_tokens_count = 0
all_tokens_length = 0

def split_text_in_good_tokens(text):
    #print(len([x for x in nltk.word_tokenize(text) if x not in bad_tokens]))
    #print(len(nltk.word_tokenize(text)))
    l = [x for x in set(nltk.word_tokenize(text)) if x not in bad_tokens]
    global all_tokens_count
    global all_tokens_length
    all_tokens_count += len(l)
    all_tokens_length += sum(list(map(len, l)))
    return "\n".join([x for x in set(nltk.word_tokenize(text)) if x not in bad_tokens])


def split_text_in_tokens(text):
    return "\n".join(nltk.word_tokenize(text))


def read_file(filename):
    with open(filename, "r") as f:
        return f.read()


def generate_bad_tokens():
    for cur_dir, dirs, files in os.walk(articles_root_folder):
        for file in files:
            folder_to_save_tokens = os.path.join(root_folder_to_save_bad_tokens, cur_dir.split("/")[-1])
            if not os.path.exists(folder_to_save_tokens):
                os.mkdir(folder_to_save_tokens)
            with open(os.path.join(folder_to_save_tokens, file + ".txt"), "w+") as f:
                text = read_file(os.path.join(cur_dir,  file))
                f.write(split_text_in_tokens(text))


def generate_good_tokens():
    for cur_dir, dirs, files in os.walk(articles_root_folder):
        for file in files:
            folder_to_save_tokens = os.path.join(root_folder_to_save_good_tokens, cur_dir.split("/")[-1])
            if not os.path.exists(folder_to_save_tokens):
                os.mkdir(folder_to_save_tokens)
            with open(os.path.join(folder_to_save_tokens, file + ".txt"), "w+") as f:
                text = read_file(os.path.join(cur_dir,  file))
                f.write(split_text_in_good_tokens(text))


def main():
    #time1 = time.time()
    #generate_bad_tokens()
    #time2 = time.time()
    #print('{:s} function took {:.3f} ms'.format(generate_bad_tokens.__name__, (time2 - time1) * 1000.0))

    time1 = time.time()
    generate_good_tokens()
    time2 = time.time()
    print('{:s} function took {:.3f} ms'.format(generate_good_tokens.__name__, (time2 - time1) * 1000.0))
    print(all_tokens_count)
    print(all_tokens_length / all_tokens_count)


if __name__=="__main__":
    main()