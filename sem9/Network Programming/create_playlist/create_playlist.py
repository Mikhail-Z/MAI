import xml.etree.ElementTree as ET
import sys
import jinja2
import json


def create_html(text, output_filename):
    with open(output_filename, "w") as f:
        f.write(text)


def create_html_file(songs_info: dict):
    with open("./templates/playlist.html") as f:
        text = f.read()
        template = jinja2.Template(text)
        rendered_text = template.render(songs_info)
        output_filename = input_filename.split(".")[0] + ".html"
        create_html(rendered_text, output_filename)


def xml2html(filename: str):
    tree = ET.parse(filename)
    root = tree.getroot()
    songs = []
    for song in root:
        song_info = {}
        for _, info in enumerate(song, 1):
            song_info[info.tag] = info.text
        songs.append(song_info)
        create_html_file({"playlist": songs})
    sys.exit(0)


def check_if_xml(filename:str):
    if filename.endswith(".xml"):
        return True
    return False


def check_if_json(filename: str):
    if filename.endswith(".json"):
        return True
    return False


def json2html(filename: str):
    songs_info = {}
    with open(filename) as f:
        songs_info = json.load(f)
        create_html_file(songs_info)


if __name__ == '__main__':
    input_filename = sys.argv[1]
    if check_if_xml(input_filename):
        xml2html(input_filename)
    elif check_if_json(input_filename):
        json2html(input_filename)
    else:
        print("wrong input file")
