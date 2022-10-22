from bs4 import *
import requests
import os
from PIL import Image
import glob
import pandas as pd
import re
import shutil
import time
# Constants :
IMAGE_EXTRACT_PATH = 'downloads'
COMPRESSED_OUTPUT_PATH = 'compressed'
BYTE_CONSTANT = 1024.0
EXCEL_PATH = 'sample.xlsx'


def FetchUrlFromExcel(path):
    df = pd.read_excel(path)
    a = pd.DataFrame(df)
    col_value = []
    url_list = []
    for i in list(a):
        col_value += a[i].tolist()
    for b in col_value:
        if (type(b) is str):
            url = re.match(r'(https?://[^\s]+)', b)
            if (bool(url) is True):
                url_list.append(b)
    return (list(set(url_list)))


def compressImages(folder_name):
    try:
        if not (os.path.exists(COMPRESSED_OUTPUT_PATH)):
            os.mkdir(COMPRESSED_OUTPUT_PATH)
        files = os.listdir(folder_name)
        for file in files:
            filepath = pathFinder(folder_name,file)
            dist_path = pathFinder(COMPRESSED_OUTPUT_PATH,file)
            filesize = "%.2f" % (os.path.getsize(filepath)/BYTE_CONSTANT)
            if float(filesize) > BYTE_CONSTANT:
                im1 = Image.open(filepath)
                im1.save(dist_path, "JPEG", quality=12)
            else:
                shutil.copyfile(filepath, dist_path)
    except:
        raise Exception()



def pathFinder(path,file):
    try:
        return os.path.normpath(os.path.abspath(os.path.join(path,file)))
    except:
       pass


def folder_create(name):
    try:

        if not (os.path.exists(name)):
            os.mkdir(name)
    except:
        pass
def remove_folder(name):
    try:
        if (os.path.exists(name)):
            shutil.rmtree(name)
    except:
        pass



def download_images(images, folder_name):
    count = 0
    print(f"Total {len(images)} Image Found!")
    if len(images) != 0:
        for i, image in enumerate(images):
            try:
                image_link = image["data-srcset"]
            except:
                try:
                    image_link = image["data-src"]
                except:
                    try:
                        image_link = image["data-fallback-src"]
                    except:
                        try:
                            image_link = image["src"]
                        except:
                            pass
            try:
                if not image_link == '' and re.match(r'(https?://[^\s]+)', image_link):
                    r = requests.get(image_link).content
                    file_ext = image_link.split(".")[-1].split(" ")[0]
                    file_ext = {True: file_ext, False: "jpg"}[
                        file_ext in ["png", "svg", "jpeg", "jpg", "gif"]]
                    try:
                        r = str(r, 'utf-8')
                    except UnicodeDecodeError:
                        file_name = str(time.time()) + "." + file_ext
                        filepath = pathFinder(folder_name,file_name)
                        with open(fr'{filepath}', "wb+") as f:
                            f.write(r)
                        count += 1
            except:
                raise 
        if count == len(images):
            print("All Images Downloaded!")
        else:
            print(f"Total {count} Images Downloaded Out of {len(images)}")


def main(urls):
    folder_create(IMAGE_EXTRACT_PATH)
    for url in urls:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        images = soup.findAll('img')
        download_images(images, IMAGE_EXTRACT_PATH)
        compressImages(IMAGE_EXTRACT_PATH)
    remove_folder(IMAGE_EXTRACT_PATH)


main(FetchUrlFromExcel(EXCEL_PATH))
