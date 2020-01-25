import shutil
import requests
import os
from selenium import webdriver
from tkinter import *

window = Tk()
window.title("Загрузчик фотоальбома ВК")

window_width = 400
window_height = 200
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
coord_x = round((screen_width - window_width) / 2)
coord_y = round((screen_height - window_height) / 2)

window.geometry(f'{window_width}x{window_height}+{coord_x}+{coord_y}')


def on_click():
    max_size = 1000
    album_url = inp.get() or 'https://vk.com/album-186089522_269355851'
    f_url_0 = album_url.split('_')[0].replace("album", "photo")

    driver = webdriver.Chrome('chromedriver.exe')

    total_count = 0
    try:
        driver.get(album_url)
        html_source = driver.page_source
        ff_url = int(
            driver.find_element_by_class_name('photos_row').get_attribute('data-id').split('_')[1])
        [total_count] = re.findall(r'"totalCount":\d+', html_source)
        total_count = int(re.findall(r'\d+', total_count)[0])
    except Exception as error:
        print(error)

    def load_photo(url, n):
        response = requests.get(url, stream=True)
        with open(f'photo/img-{n}.jpg', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)

    def load(num_url, num_name):
        driver.get(f'{f_url_0}_{ff_url + num_url}')
        html_source2 = driver.page_source
        reg = r'"w_src":["[\w\\\/\-\.\:]+"'
        u = re.findall(reg, html_source2)[4][9:]
        u = u.replace('"', ''"").replace('\\', "")
        load_photo(u, num_name)

    if os.path.exists('./photo') is not True:
        os.mkdir('./photo')
    cnt = 0
    size = total_count

    while total_count and (cnt < max_size):
        try:
            load(cnt, size - total_count + 1)
            total_count -= 1
        except Exception as error:
            print(error)
        cnt += 1

    driver.quit()

    window.destroy()


lbl = Label(window, text="Адрес страницы фотоальбома")
lbl.place(relx=0.5, rely=0.1, anchor="center")

inp = Entry(window, width=50)
inp.place(relx=0.5, rely=0.25, anchor="center")
inp.focus()

btn = Button(window, text="Скачать фотоальбом", command=on_click)
btn.place(relx=0.5, rely=0.45, anchor="center")

window.mainloop()
