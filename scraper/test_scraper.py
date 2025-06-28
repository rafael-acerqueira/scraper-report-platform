from bs4 import BeautifulSoup

html = '''
<html>
  <body>
    <h1>Título Principal</h1>
    <h2>Subtítulo 1</h2>
    <h2>Subtítulo 2</h2>
    <a href="https://site.com">Site</a>
    <a href="https://github.com">GitHub</a>
    <div>
      <h3>Seção Especial</h3>
      <a href="https://google.com">Google</a>
    </div>
  </body>
</html>
'''

soup = BeautifulSoup(html, 'html.parser')

links = soup.find_all('a')

my_dict = {}

for tag in ['h1', 'h2', 'h3']:
    for elements in soup.find_all(tag):
        for element in elements:
            if tag not in my_dict.keys():
                my_dict[tag] = [element.getText(strip=True)]
            else:
                my_dict[tag].append(element.getText(strip=True))

for link in links:
    if 'links' not in my_dict:
        my_dict['links'] = []
    my_dict['links'].append(link.getText(strip=True))
print(my_dict)
"""{
  "h1": ["Texto do h1"],
  "h2": ["Texto do h2", ...],
  "h3": ["Texto do h3", ...],
  "links": ["Texto do link 1", "Texto do link 2", ...]
}"""