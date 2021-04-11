from selenium import webdriver
from bs4 import BeautifulSoup as soups
import numpy as np
import os
from os import path
from time import time
import cv2
 
project_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))


def num_to_name(x):
    if x<10:
        return "000"+str(x)
    if x<100:
        return "00"+str(x)
    if x<1000:
        return "0"+str(x)
    return str(x)

def search_selenium(keyword, save_path, size):
    start_time = time()
    search_url = "https://www.google.com/search?q=" + str(keyword) + "&hl=en&tbm=isch"
    
    browser = webdriver.Chrome(project_path + "/chromedriver")
    browser.get(search_url)
    
    image_count = len(browser.find_elements_by_tag_name("img"))
    
    print("# of loaded images : ", image_count)
 
    browser.implicitly_wait(2)
 
    cnt = 0
    i = 0
    while(i<size) :
        image_path = save_path + "/" + num_to_name(i) + ".png"
        cnt = cnt + 1
        if cnt > 500:
            break
        try:
            image = browser.find_elements_by_tag_name("img")[cnt]
            # print("before screen shot")
            image.screenshot(image_path)
            # print("1")
            img = cv2.imread(image_path)
            # print("2")
            h, w, _ = img.shape
            if h<=50 or w<=50:
                #print("too small image. pass...")
                continue
            i = i + 1
        except:
            print("unable screen")
            pass
    
    end_time = time()
    elapsed = end_time - start_time
    print('Elapsed time is %f seconds.' % elapsed)

    browser.close()

    return i
 
if __name__ == "__main__" :
    size = 100
    result_path = project_path + "/result/"
    if not path.exists(project_path + "/result"):
        os.mkdir(project_path + "/result")
    keywords = np.load(file= project_path + "/vocab.npy")
    n = len(keywords)
    print("# of words : " + str(n))
    success = 0
    for i in range(n):
        keyword = keywords[i]
        save_path = result_path + keyword
        print("[%04d / %04d] progressing..." % (i+1, n))
        print("keyword: " + keyword)
        if path.exists(save_path):
            print("already exists. keyword may be duplicated")
            continue
        else:
            os.mkdir(save_path)
        rt = search_selenium(keyword, save_path, size)
        if rt == size:
            success = success + 1
        print("# of collected image for keyword [" + keyword + "]: " + str(rt) + "     success : " + str(success) + "/" + str(i+1))