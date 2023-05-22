import os
from time import sleep
import requests
import re
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import filedialog
from tkinter import ttk

window = Tk()

FILE = ""

LABEL_FONT = ("Calibri", 14)
MESSAGE_FONT = ("Calibri", 12)


HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36'}

status_ok = 0
status_part_ok = 0
status_not_found = 0
status_404 = 0

def message():
    if FILE == "":
        message.config(text="Файл не выбран")
        return
    else:
        message.config(text="Не закрывайте окно до завершения работы")
        sleep(3)
        main()

def open_file():
    global status_ok
    global status_part_ok
    global status_not_found
    global status_404
    global FILE
    status_ok = 0
    status_part_ok = 0
    status_not_found = 0
    status_404 = 0
    with open(filedialog.askopenfilename(), encoding="UTF-8") as f:
        FILE =  f.read()
        message.config(text=f"Загружен файл\n{f.name.split('/')[-1]}")
    

def project_name_shorter(project):
    short_name = ""
    list_name = project.split(" ")
    for i in list_name:
        short_name += i[0:-3].lower() + "\S+" + " "
    return short_name.strip()

def url_checker(media, link, project_name, short_project_name):
    global status_ok
    global status_part_ok
    global status_not_found
    global status_404
    
    
    
    status = ""
    
    response = requests.get(link, headers=HEADERS)
    row_prefix = f"""
<tr>
    <td>{media}</td>
    <td><a href="{link}" target="_blank">{link}</a></td>

        """ 
    row_postfix = f"""    
</tr>
        """    
    
    
    html_for_analyze = response.text.lower().replace("\"", "")
    html_for_analyze = html_for_analyze.replace("\\", "")    
    
    if response.ok == False:
        status_404 += 1
        status = '<td style="color:white; background-color:#6e6e6e;">Страница не существует</td>'
        return row_prefix + status + row_postfix
    
    elif html_for_analyze.count(project_name.lower()) > 0:
        status_ok += 1
        status = '<td style="color:white; background-color:#61b661;">OK</td>'
        return row_prefix + status + row_postfix
        
    elif re.search(short_project_name, html_for_analyze):
        status_part_ok += 1
        status = '<td style="color:393939; background-color:#f6ec80;">Частичное совпадение</td>'
        return row_prefix + status + row_postfix
    
    else:
        status_not_found += 1
        status = '<td style="color:white; background-color:#f26363;">Совпадений не найдено</td>'
        
        return row_prefix + status + row_postfix
    
def main():
    
    
    
    try:
        
        html = BeautifulSoup(FILE, "html.parser")

        project_name = html.find_all("div", class_ = "sub-navbar__name")[0].string.strip().replace("\"", "")
        short_project_name = project_name_shorter(project_name)


        links = {}

        last_table = html.find_all("div", class_ = "report-table")[-1]
        tr = last_table.tbody.find_all("tr")
        for i in range(len(tr)):
            if tr[i].find_all("td")[-1].string[0:5].count("http") > 0:
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
            try:
                table_row += url_checker(next_link, links.get(next_link), project_name, project_name_shorter(project_name)) + "\n"
            except Exception:
                print(f"Не могу открыть адрес {links.get(next_link)}")
        html_postfix = f"""
    </tbody>
</table>

    <div class="stata">
        <h3>Статистика:</h3>
        Всего источников: {len(links)}<br>
        Найдено полностью: {status_ok}<br>
        Найдено частично: {status_part_ok}<br>
        Не найдено: {status_not_found}<br>
        Битых ссылок: {status_404}
    </div>
</div>
    """
      
        

        root_folder = os.path.dirname(__file__) 
        results_folder = os.path.join(root_folder, "results") 
        if not os.path.exists(results_folder):
            os.makedirs(results_folder)
            print(f"{results_folder} has been created")
        
        filepath = filedialog.asksaveasfilename(defaultextension="html", initialfile=project_name)
        if filepath != "":
            try:
                with open(filepath, "w") as file:
                    file.write(css_style + html_prefix + table_row + html_postfix)    
            except:
                message.config(text="Файл не сохранен!")
            else:
                message.config(text="Готово!")

    except Exception as error:
        message.config(text="Ошибка. Файл невозможно анализировать")  
        print(error)
        


window.geometry("450x300+0+0")
window.resizable(True, True)
icon_path = os.path.join(os.path.dirname(__file__), "logo.ico")
try:
    window.iconbitmap(default= icon_path)
except Exception as error:
    print(error)
window.title("РМЦ Link Checker 1.0.2")

top_frame = Frame()
top_frame.pack(padx=10, pady=50)

middle_frame = Frame()
middle_frame.pack(padx=10, pady=0)

bottom_frame = Frame()
bottom_frame.pack(padx=10, pady=0)

label = Label(top_frame, text="Выберите файл для анализа ссылок", font=LABEL_FONT)
label.pack(padx=10, side=LEFT)
file_choise = ttk.Button(top_frame, text="Обзор", command=open_file, padding=5)
file_choise.pack(padx=10, side=LEFT)

analyze = ttk.Button(middle_frame, text="Начать анализ", command=message, padding=5)
analyze.pack(side=RIGHT)

message = Label(bottom_frame, font=MESSAGE_FONT, justify=CENTER)
message.pack(pady=20)

window.mainloop()