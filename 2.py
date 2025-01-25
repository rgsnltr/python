name = 'SJ'
if name == '':
    raise NotImplementedError('Put your name')



import requests
from bs4 import BeautifulSoup
from typing import List
from typing import Generator
import random
import unittest

def get_all_links(url: str) -> List[str]:
    """
    Get all the links in the webpage at the given URL

    :param url: A string that is the URL of the webpage where we need to find the links
    :return: A list with all the links of the given webpage
    """
    links = []

    try:
        response = requests.get(url)
        response.raise_for_status()  
        soup = BeautifulSoup(response.text, 'html.parser')

        for a_tag in soup.find_all('a', href=True):
            links.append(a_tag['href'])


    except requests.exceptions.MissingSchema:
        print(f"Invalid URL: {url}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")

    return links


print(get_all_links('https://en.wikipedia.org')[:10])







class TestGetNeighborPages(unittest.TestCase):

    def test_valid_url(self):
        generator = get_neighbor_pages('https://en.wikipedia.org/wiki/Main_Page')
        html_content = next(generator)  
        self.assertGreater(len(html_content), 0, "Should return HTML content for a valid URL.")

    def test_invalid_url(self):
        generator = get_neighbor_pages('ht://invalid-url.com')
        with self.assertRaises(StopIteration):
            next(generator) 

    def test_empty_url(self):
        generator = get_neighbor_pages('')
        with self.assertRaises(StopIteration):
            next(generator) 





def get_neighbor_pages(url: str) -> Generator[str, None, None]:
    """
    Go through the links in the webpage at the given URL
    and yield the html content of each of them

    :param url: A string that is the URL of the webpage
    """
    try:
  
        response = requests.get(url)
        response.raise_for_status() 
        soup = BeautifulSoup(response.text, 'html.parser')


        for a_tag in soup.find_all('a', href=True):
            link = a_tag['href']
        
            if not link.startswith('http'):
                link = requests.compat.urljoin(url, link)

            try:

                print(f"Fetching {link}") 
                page_response = requests.get(link)
                page_response.raise_for_status()
                yield page_response.text
            except requests.exceptions.RequestException as e:
                print(f"Error fetching {link}: {e}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")


for page_html in get_neighbor_pages('https://en.wikipedia.org/wiki/Main_Page'):
    print(page_html[:100])  
    break  




def get_pages_depth(url: str, depth: int) -> Generator[str, None, None]:
    """
    Go as deep as the given depth, through the links in the webpage at the given URL
    and yield the html content of each of them,

    :param url: A string that is the URL of the webpage
    :param depth: An integer that is the depth until which the function searches
    """
    visited = set() 

    def helper(url: str, current_depth: int):

        if current_depth > depth:
            return

        if url in visited:  
            return
        visited.add(url)

        try:
            response = requests.get(url)
            response.raise_for_status()  
            yield response.text  

            soup = BeautifulSoup(response.text, 'html.parser')

            for a_tag in soup.find_all('a', href=True):
                link = a_tag['href']


                if not link.startswith('http'):
                    link = requests.compat.urljoin(url, link)


                yield from helper(link, current_depth + 1)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")

    yield from helper(url, 1)


pages = get_pages_depth(depth=2, url='https://en.wikipedia.org/wiki/Main_Page')

for _ in range(5):
    print(next(pages)[:100])  # 打印每个页面HTML的前100个字符



class ComputerScientist:
    def __init__(self, name: str, birthdate: str, major_achievements: str, alma_mater: str):
        self.name = name
        self.birthdate = birthdate
        self.major_achievements = major_achievements
        self.alma_mater = alma_mater

    def __str__(self):
        return f"{self.name}, Born: {self.birthdate}, Major Achievements: {self.major_achievements}, Alma Mater: {self.alma_mater}"

    def update_achievements(self, achievements: str):
        self.major_achievements = achievements

    def update_alma_mater(self, alma_mater: str):
        self.alma_mater = alma_mater

    def get_summary(self):
        return f"Name: {self.name}, Birthdate: {self.birthdate}, Achievements: {self.major_achievements}, Alma Mater: {self.alma_mater}"


def get_scientists_from_page(url: str, num_scientists: int = 100):
    scientists = []

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    wikitable  = soup.find('table', {'class': 'wikitable'})
    if wikitable is None:
        print("Table with class 'wikitable' not found.")
        return []

    rows = wikitable.find_all('tr')

    selected_scientists = random.sample(rows[1:], num_scientists)  # 从第二行开始，因为第一行是表头

    for row in selected_scientists:
        columns = row.find_all('td')

        if len(columns) > 2:  
            name = columns[0].get_text(strip=True)  
            birthdate = columns[1].get_text(strip=True) if len(columns) > 1 else "Unknown"  # 获取出生日期
            major_achievements = columns[2].get_text(strip=True) if len(columns) > 1 else "Unknown"
            alma_mater = columns[3].get_text(strip=True) if len(columns) > 1 else "Unknown"

            cs = ComputerScientist(name, birthdate, major_achievements, alma_mater)
            scientists.append(cs)

    return scientists


scientists_list = get_scientists_from_page("https://en.wikipedia.org/wiki/List_of_computer_scientists")

for scientist in scientists_list[:5]:
    print(scientist.get_summary())
