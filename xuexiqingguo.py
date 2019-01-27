# -*- coding: utf-8 -*-
import urllib.request
import re
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import chardet
import sys
import io
import time
import os
from xlwt import *
import requests
import json
import argparse
import random

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
os.environ["webdriver.chrome.driver"]=chromedriver


profile_dir=r"C:\Users\spiden\AppData\Local\Google\Chrome\User Data"
chrome_options=webdriver.ChromeOptions()
#chrome_options.add_argument(r"user-data-dir=" +os.path.abspath(profile_dir))
#chrome_options.add_argument('--headless')
chrome_options.add_argument("--mute-audio")

def driver_get_doc(cookie,d_text,d_video):

	driver = webdriver.Chrome(executable_path=chromedriver,chrome_options = chrome_options)

	l = len(d_text);
	p = random.uniform(0,1);
	if(p > 0):
		tmp= []
		for i in range(10):
			tmp.append(random.randint(0,l))
		for i in tmp:
			driver.get(d_text[i])
			driver.add_cookie(cookie_dict = cookie)
			driver.get(d_text[i])	
			#print (driver.current_url)
			length = 500;
			for i in range(5):
				js = js="var q=document.documentElement.scrollTop=" + str(length)
				driver.execute_script(js) 
				time.sleep(20)
				length +=length;
	else:
		for i in range(10):
			driver.get(d_text[i])
			driver.add_cookie(cookie_dict = cookie)
			driver.get(d_text[i])
			length = 500;
			for i in range(5):
				js = js="var q=document.documentElement.scrollTop=" + str(length)
				driver.execute_script(js) 
				time.sleep(20)
				length += length

	l = len(d_video);
	p = random.uniform(0,1);
	if(p > 0):
		tmp= []
		for i in range(7):
			tmp.append(random.randint(0,l))
		for i in tmp:
			driver.get(d_video[i])
			driver.add_cookie(cookie_dict = cookie)
			driver.get(d_video[i])	
			#print (driver.current_url)	
			driver.find_element_by_class_name('outter').click()
			time.sleep(200)
			
	else:
		for i in range(7):
			driver.get(d_video[i])
			driver.add_cookie(cookie_dict = cookie)
			driver.get(d_video[i])	
			driver.find_element_by_class_name('outter').click()
			time.sleep(200)
	driver.quit()

def get_the_address(url):
	url_address = []
	web = urllib.request.urlopen(url);
	content = web.read().decode('utf-8');
	content = content.split('Cache =')[1]
	content =content.split(';')[0];
	#print (content)
	tmp = content.split('":')[0].split('{"')[1];
	data = json.loads(content);
	cur = data[tmp]['list']
	for c in cur:
		url_address.append(c['static_page_url']);
	return url_address

def get_current_point(url,cookies):
	headers = {'Referer':'https://www.zhihu.com/search?type=content&q=%E6%96%B0%E4%B8%9C%E6%96%B9%E5%B9%B4%E4%BC%9A','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
	content = requests.get(url,headers = headers, cookies = cookies)
	#content = requests.get(url)
	print (content.text)
	content = BeautifulSoup(content.text,'html5lib')
	print (content)
	hh = content.findAll(name = 'div',attrs = {'class' :'Button FollowButton Button--primary Button--blue'});
	print (hh)
	# hh = content.findAll(name = 'div',attrs = {'class' :'my-points-header'});
	#print (hh)

def handle_cookie(cookie):
	handled_cookie ={};
	cur = cookie.split(';');
	for c in cur:
		k,v = c.strip().split('=',1)
		handled_cookie[k]=v;
	return handled_cookie

def __main__():

	parser = argparse.ArgumentParser(description = 'run the model')
	parser.add_argument("--token", dest="token", type=str, metavar='<str>',default = 'sdfs',
                    help="the value of the cookie")
	args = parser.parse_args()
	value = args.token;

	cookie = {'name' : 'token', 'domain':'.xuexi.cn','path':'/'}
	cookie['value'] = value
	url_video = 'https://www.xuexi.cn/a191dbc3067d516c3e2e17e2e08953d6/datab87d700beee2c44826a9202c75d18c85.js'
	url_text = 'https://www.xuexi.cn/98d5ae483720f701144e4dabf99a4a34/data5957f69bffab66811b99940516ec8784.js'
	u_text = get_the_address(url_text);
	u_video = get_the_address(url_video);
	print (u_text[0]);
	print (u_video[0]);
	driver_get_doc(cookie,u_text,u_video);


if __name__=='__main__':
	__main__()