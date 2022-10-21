from bs4 import *
import requests
import os
from datetime import datetime
from PIL import Image
import glob
import pandas as pd
import re
import shutil

# Constants :
IMAGE_EXTRACT_PATH = 'downloads'
COMPRESSED_OUTPUT_PATH = 'compressed'
BYTE_CONSTANT = 1024.0
EXCEL_PATH='sample.xlsx'

# creating data frame
# importing excel file
def FetchUrlFromExcel(path):
    df = pd.read_excel(path)  
    a=pd.DataFrame(df)
    col_value=[]
    url_list=[]
    for i in list(a):
        col_value+=a[i].tolist()
    for b in col_value:
        if(type(b) is str):
            url=re.match(r'(https?://[^\s]+)', b)
            if(bool(url) is True):
                url_list.append(b)
    return(list(set(url_list)))

def compressImages(folder_name):
    try:
        if not (os.path.exists(COMPRESSED_OUTPUT_PATH)):
            os.mkdir(COMPRESSED_OUTPUT_PATH)
        files = os.listdir(folder_name)
        # check Files Through Directory
        for file in files:
            # print(file)
            timestamp = str(datetime.now())
            filepath = folder_name+"/"+file
            dist_path = COMPRESSED_OUTPUT_PATH+"/"+timestamp+file
            filesize = "%.2f" % (os.path.getsize(filepath)/BYTE_CONSTANT)
            if float(filesize) > BYTE_CONSTANT:

                im1 = Image.open(filepath)
                im1.save(dist_path, "JPEG", quality=10)
            else:
                shutil.copyfile(filepath, dist_path)

        

    # if folder exists with that name, ask another name
    except:
        raise Exception()

    # image downloading start
    # download_images(images, folder_name)


# CREATE FOLDER
def folder_create():
    try:
        # folder creation
        if not (os.path.exists(IMAGE_EXTRACT_PATH)):
            os.mkdir(IMAGE_EXTRACT_PATH)
    # if folder exists with that name, ask another name
    except:
        pass


# DOWNLOAD ALL IMAGES FROM THAT URL
def download_images(images, folder_name):

    # initial count is zero
    count = 0

    # print total images found in URL
    print(f"Total {len(images)} Image Found!")

    # checking if images is not zero
    if len(images) != 0:
        for i, image in enumerate(images):
            # From image tag ,Fetch image Source URL
            # 1.data-srcset
            # 2.data-src
            # 3.data-fallback-src
            # 4.src
            # Here we will use exception handling
            # first we will search for "data-srcset" in img tag
            try:
                # In image tag ,searching for "data-srcset"
                image_link = image["data-srcset"]

            # then we will search for "data-src" in img
            # tag and so on..
            except:
                try:
                    # In image tag ,searching for "data-src"
                    image_link = image["data-src"]
                except:
                    try:
                        # In image tag ,searching for "data-fallback-src"
                        image_link = image["data-fallback-src"]
                    except:
                        try:
                            # In image tag ,searching for "src"
                            image_link = image["src"]

                        # if no Source URL found
                        except:
                            pass

            # After getting Image Source URL
            # We will try to get the content of image
            try:
                if not image_link == '':
                    r = requests.get(image_link).content
                    #print(r)
                    try:
                        # possibility of decode
                        r = str(r, 'utf-8')
                    except UnicodeDecodeError:
                        dateTimeObj = str(datetime.now())
                    
                        # After checking above condition, Image Download start
                        with open(f"{folder_name}/{dateTimeObj}.jpg", "wb+") as f:
                            f.write(r)

                        # counting number of image downloaded
                        count += 1
            except:
                raise 

        # There might be possible, that all
        # images not download
        # if all images download
        if count == len(images):
            print("All Images Downloaded!")

        # if all images not download
        else:
            print(f"Total {count} Images Downloaded Out of {len(images)}")

# MAIN FUNCTION START


def main(urls):
      # Call folder create function
    folder_create()
    for url in urls:
        
        
        # content of URL
        r = requests.get(url)

        # Parse HTML Code
        soup = BeautifulSoup(r.text, 'html.parser')

        # find all images in URL
        images = soup.findAll('img')
        
        
        # image downloading start
        download_images(images, IMAGE_EXTRACT_PATH)
        compressImages(IMAGE_EXTRACT_PATH)
    shutil.rmtree(IMAGE_EXTRACT_PATH)
  


# take url
#url = input("Enter URL:- ")

# CALL MAIN FUNCTION
main(FetchUrlFromExcel(EXCEL_PATH))
