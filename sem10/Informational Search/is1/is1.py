import os
from bs4 import BeautifulSoup
import requests
import urllib.parse

reviews_page_url = "http://mobile-review.com/review.shtml"

default_folder = "/home/mikhail/Documents/InformationSearch"
site = "http://mobile-review.com"


def get_main_review_page():
    return requests.get(reviews_page_url).text


def get_page(url):
    return requests.get(url).text


def delete_script_tag_inside_text(soup):
    [s.extract() for s in soup('script')]


def get_review_text(page):
    soup = BeautifulSoup(page, "html.parser")
    delete_script_tag_inside_text(soup)
    article = soup.find("div", "article")
    text = article.getText()
    title = article.find("h1").getText()
    return title, text


def get_reviews_urls(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    review_rubrics = get_reviews_rubrics(soup)
    all_urls = []
    for thematic_reviews_html_block in review_rubrics:
        html_tags = thematic_reviews_html_block.find_all("a", href=True)
        thematic_urls = []
        for html_tag in html_tags:
            thematic_urls.append(html_tag["href"])
        all_urls.append((thematic_reviews_html_block.find("h1").getText(), thematic_urls))
    return all_urls


def get_full_url(relative_url):
    return urllib.parse.urljoin(site, relative_url)


def get_reviews_rubrics(soup):
    return soup.find_all("div", "phonelist")


num = 0


def write_text_to_file(folder, filename, text):
    global num
    num += 1
    with open(os.path.join(folder, filename), "w+") as f:
        f.write(text)


def remove_blank_lines(text):
    return os.linesep.join([s for s in text.splitlines() if s])


def main():
    main_page = get_main_review_page()
    reviews_urls = get_reviews_urls(main_page)
    i = 0
    for reviews_category, urls in reviews_urls:
        folder = os.path.join(default_folder, reviews_category)
        if not os.path.exists(os.path.join(default_folder, reviews_category)):
            os.makedirs(folder)

        for url in urls:
            page = get_page(get_full_url(url))
            try:
                title, text = get_review_text(page)
                text = remove_blank_lines(text)
                write_text_to_file(folder, title, text)
            except:
                pass
        i+=1


if __name__ == "__main__":
    main()
    print(num)