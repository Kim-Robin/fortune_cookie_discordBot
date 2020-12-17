from bs4 import BeautifulSoup
import requests
import json

# with open('')

# content =

# soup = BeautifulSoup(content, 'lxml')

r = requests.get("https://joshmadison.com/2008/04/20/fortune-cookie-fortunes/")
soup = BeautifulSoup(r.content, 'lxml')

tags = soup.find('article')
lists = tags.find_all('li')

print(len(lists))
print(type(lists))

values = []

for li in lists:
    print(li.string)
    fortune = li.string.strip()
    values.append({"fortune": fortune})

with open('fortune.json', 'w') as fp:
    fp.write(json.dumps(values))
# print(json.loads(str(lists)))
