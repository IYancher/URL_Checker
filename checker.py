import os
import requests
import re
from bs4 import BeautifulSoup


FILE = os.path.join(os.path.dirname(__file__), "Согласование_проекта_Интерфейс_администрирования_АИС_Молодёжь_России.html")
headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36'}

status_ok = 0
status_part_ok = 0
status_not_found = 0
status_404 = 0

def project_name_shorter(project):
    short_name = ""
    list_name = project.split(" ")
    for i in list_name:
        short_name += i[0:-3].lower() + "\S+" + " "
    return short_name.strip()

def url_checker(media, link):
    global status_ok
    global status_part_ok
    global status_not_found
    global status_404
    
    status = ""
    
    response = requests.get(link, headers=headers)
    row_prefix = f"""
<tr>
    <td>{media}</td>
    <td><a href="{link}" target="_blank">{link}</a></td>

        """ 
    row_postfix = f"""    
</tr>
        """    
    if response.ok == False:
        status_404 += 1
        status = '<td style="color:white; background-color:#6e6e6e;">Страница не существует</td>'
        return row_prefix + status + row_postfix
    
    elif response.text.lower().count(project_name.lower()) > 0:
        status_ok += 1
        status = '<td style="color:white; background-color:#61b661;">OK</td>'
        return row_prefix + status + row_postfix
        
    elif re.search(short_project_name, response.text.lower()):
        status_part_ok += 1
        status = '<td style="color:393939; background-color:#f6ec80;">Частичное совпадение</td>'
        return row_prefix + status + row_postfix
    
    else:
        status_not_found += 1
        status = '<td style="color:white; background-color:#f26363;">Совпадений не найдено</td>'
        return row_prefix + status + row_postfix
    


with open(FILE, encoding="UTF-8") as f:
    html = BeautifulSoup(f, "html.parser")

project_name = html.find_all("div", class_ = "sub-navbar__name")[0].string.strip()
short_project_name = project_name_shorter(project_name)


links = {}

last_table = html.find_all("div", class_ = "report-table")[-1]
tr = last_table.tbody.find_all("tr")
for i in range(len(tr)):
    
    if tr[i].find_all("td")[-1].string.count("https") > 0:
        links[str(i+1) + ". " + (tr[i].find_all("td")[1].string.strip())] = tr[i].find_all("td")[-1].string.strip()
    


 
css_style = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Charis+SIL:wght@700&family=Open+Sans:wght@400;600;800&family=Roboto+Slab&display=swap" rel="stylesheet">
<style>

body{
font-family: 'Charis SIL', serif;
font-family: 'Open Sans', sans-serif;
font-family: 'Roboto Slab', serif;
    padding: 0;
	margin:0;
	    background: #f4f4f4;
}
a{
color: #000;
}
a:hover{
color:#be0303;
}
 a:visited {
    color: #acacac;
   }
.header{
    height: 75px;
    background: #fff;
    padding: 0 6%;
    box-shadow: 2px 2px 10px #bebebe;
}
.logo {
    width: 239px;
    height: 75px;
    background: url(https://rscenter.ru/local/templates/remc/img/logo.png) no-repeat;
    -webkit-background-size: contain;
    background-size: contain;
    display: block;
	}
.container{
padding: 0 6%;
margin: 10px;
}
table{
border-collapse:collapse;
}
tbody tr:nth-child(odd){
background-color:#ededed
}
td, th{
padding: 10px;
}
td:nth-child(3){
text-align: center;
}
.stata{
    background: #fff;
    padding: 20px;
    margin-top: 20px;
    display: inline-block;
	line-height: 2;
}
h3{
margin:0;
}
</style>
"""
  
html_prefix = f"""
<div class="header">
    <span class="logo"></span>
</div>
<div class="container">
<h2>{project_name}</h2>
<table style="width: 100%;">
    <thead>
        <tr>
            <th>Название СМИ</th>
            <th>Ссылка</th>
            <th>Статус</th>
        </tr>
    </thead>
    <tbody>
"""   

table_row = ""   
for next_link in links.keys():
    table_row += url_checker(next_link, links.get(next_link)) + "\n"
    
 

html_postfix = f"""
    </tbody>
</table>

    <div class="stata">
        <h3>Статистика:</h3>
        Всего источников: {len(links)}<br>
        Найдено полностью: {status_ok}<br>
        Найдено частично: {status_part_ok}<br>
        Битых ссылок: {status_404}
    </div>
</div>
"""
    

with open("C:\\Work\\Python\\URL_Checker\\URL_Checker\\URL_Checker\\result.html", "w") as f:
    f.write(css_style + html_prefix + table_row + html_postfix)