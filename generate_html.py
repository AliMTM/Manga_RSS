import requests
from bs4 import BeautifulSoup
import time

# manga list
manga_data = []

for i in range(1,20):

    if (i == 1):
        url = 'https://manganato.com/genre-all'
    else:
        url = f'https://manganato.com/genre-all/{i}'
    response = requests.get(url)

    # parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(response.text, 'html.parser')

    # find the HTML elements that contain the manga titles, latest chapter, and ratings
    manga_list = soup.find('div', {'class': 'panel-content-genres'})
    manga_items = manga_list.find_all('div', {'class': 'content-genres-item'})

    # extract the titles, latest chapter, and ratings from the HTML elements
    for item in manga_items:
        a = item.find('a', {'class': 'genres-item-img bookmark_check'})
        a_ch = item.find('a', {'class': 'genres-item-chap text-nowrap a-h'})
        img = item.find('img', {'class': 'img-loading'})
        title = a.get('title')
        link = rf"{a.get('href')}"
        rating = a.text.strip()
        chapter = ""
        img_url = ""
        try:
            chapter = a_ch.text.strip()
        except:
            chapter = "N/A"

        if rating >= "4.8" and chapter != "N/A":

            try:
                img_url = img.get('src')
            except:
                img_url = "N/A"

            manga_data.append({'title': title, 'latest_chapter': chapter, 'rating': rating, 'image_url': img_url, 'link': link})
    time.sleep(0.5)

# create an HTML table with the manga data
table_html = "<table>\n"
table_html += """<thead>
        <tr>
            <th>Title</th>
            <th>Latest Chapter</th>
            <th>Rating</th>
            <th>Image URL</th>
        </tr>
    </thead>\n"""
table_html += "<tbody>"
for manga in manga_data:
    table_html += "<tr>\n"
    table_html += f"<td style='border: 1px solid black;'><img src='{manga['image_url']}' alt='{manga['title']}'></td>"
    table_html += f"<td style='border: 1px solid black';> <a href=\"{manga['link']}\">{manga['title']}</a></td>"
    table_html += f"<td style='border: 1px solid black;'>{manga['latest_chapter']}</td>"
    table_html += f"<td style='border: 1px solid black;'>{manga['rating']}</td>"
    table_html += "</tr>\n"
table_html += "</tbody>\n"
table_html += "</table>"

# create an HTML file and write the table to it
html_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Manga List</title>
    <style>
        table {{
            border-collapse: collapse;
            width: 100%;
        }}
        th, td {{
            text-align: left;
            padding: 8px;
        }}
        tr:nth-child(even){{background-color: #f2f2f2}}
        th {{
            background-color: #4CAF50;
            color: white;
        }}
    </style>
</head>
<body>
    <h1>Manga List</h1>
    {table}
</body>
</html>
"""
html_output = html_template.format(table=table_html)
with open('manga_list2.html', 'w', encoding='utf-8') as f:
    f.write(html_output)

# open the HTML file in a web browser
import webbrowser
webbrowser.open('manga_list2.html')
