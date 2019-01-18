# -*- coding: utf-8 -*-
#import urllib.request
import re
from bs4 import BeautifulSoup
import chardet
import sys
import io
import json
import os
import tensorflow as tf
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

name1=[]
count =0
def get_doc(url):
	web = urllib.request.urlopen(url)
	html = BeautifulSoup(web.read(),'html5lib')
	return html


def get_first_urls(html):
	t= html.findAll(name='li',attrs={"class":re.compile('catalog_li_normal')})
	i=0;
	urls=[];
	for h in t:
		cur = h.a['href']
		u="http://tieba.baidu.com"+cur
		urls.append(u)
		i=i+1
	print (i)
	return urls	
	
# def get_2_urls(html):
# 	t= html.findAll(name='a',attrs={"hidefocus":"true","href":re.compile("/p/"),"title":re.compile(".*")})
# 	haha=[];
# 	for h in t:
# 		cur = "http://tieba.baidu.com"+h['href']
# 		haha.append(cur)
# 	return haha
def get_2_urls(html,b_name):
	t= html.findAll(name='div',attrs={"class":"grbm_ele_wrapper"})

	for h in t:
		t1=h.find(name='span',attrs={'class':re.compile("grbm_ele_pic_amount")})
		cur1 = t1.get_text().split("张")
		num = cur1[0]   #一共多少张

		t2=h.find(name='div',attrs={'class':"grbm_ele_title"})
		cur2 = t2.a['href'].split('/')
		id=cur2[2]     #相册id
		p_name = t2.a.get_text()  #相册名字

		# print (id,num,p_name)
		handle_json(id, num, p_name,b_name)

def handle_json(id, num, p_name,b_name):
    j_url="http://tieba.baidu.com/photo/g/bw/picture/list?kw=%E5%88%98%E4%BA%A6%E8%8F%B2&alt=jview&rn=200&tid="+str(id)+"&pn=1&ps=1&pe="+str(num)+"&wall_type=v&_=1464"
    # j_url="http://tieba.baidu.com/photo/g/bw/picture/list?kw=%E5%88%98%E4%BA%A6%E8%8F%B2&alt=jview&rn=200&tid=2016159949&pn=1&ps=41&pe=80&wall_type=v&_=146416"
    data=[]
    try:
    	web = urllib.request.urlopen(j_url)
    	j_data = web.read().decode('gbk')
    	data = json.loads(j_data)
    except:
    	print ("无法解码")
    
    if(len(data)==0):
    	return 0
    cur = data['data']
    # print (cur)
    global count 
    path1=r'C:\Users\spiden\Desktop\spider\yifei'
    path2=os.path.join(path1,b_name)
    if not os.path.isdir(path2):
    	os.makedirs(path2)

    new_path = os.path.join(path2,p_name)
    if not os.path.isdir(new_path):
    	os.makedirs(new_path)

    cur2 =cur['pic_list']
    j =1
    for h in cur2:
    	pic = h['purl'].strip()
    	try:
    		res = urllib.request.urlopen(pic).read()
    		with open(new_path +'\\'+str(j)+'.jpg','wb') as code:
    			code .write(res)
    		j=j+1
    		count=count+1
    	except:
    		print ("链接有误，读取超时")
    return 1
    

def test():
	j_url="http://tieba.baidu.com/photo/g/bw/picture/list?kw=%E5%88%98%E4%BA%A6%E8%8F%B2&alt=jview&rn=200&tid=2016159949&pn=1&ps=41&pe=80&wall_type=v&_=146416"



def get_f_name(html):
	n = html.find(name='li',attrs={"class":re.compile("catalog_li_normal current")})
	x=n.a.span.get_text()
	tmp=x.split('(')
	aaa=tmp[0].strip()
	return aaa
	
def get_s_name(html):
	t= html.findAll(name='a',attrs={"hidefocus":"true","href":re.compile("/p/"),"title":re.compile(".*")})
	haha=[];
	for h in t:
		cur = h.get_text()
		haha.append(cur)
	return haha
	return t

def handle_img(html):
	# 如何自动获取？？
	# isMore = html.find(name='div',attrs={"class":"js_pager"})
	t = html.findAll(name='img',attrs={"id":"dlg_pi_img"})
	print (t)


def __main__():
	url = "http://tieba.baidu.com/f?kw=liuyifei&ie=utf-8&tab=album"
	
	urls = get_first_urls(get_doc(url))   #得到所有分类图片
	for h in urls:
		print (h)
		html=get_doc(h)
		b_name=get_f_name(html)
		get_2_urls(html,b_name)
	global count
	print (count)


	





	# for i in urls:
	# 	lll=get_2_urls(get_doc(i))
	# 	for cur in lll:
	# 		print(cur)
	# for i in urls:
	# 	print (i)
	# 	html = get_doc(i)
	# 	print (get_f_name(html))


	# 	print (get_2_urls(html))
	# html=get_doc(urls[0])
	# u=get_2_urls(html)
	# print (u[5])
	# name2=get_s_name(html)
 
	# doc = get_doc(u[5])
	# print (doc)
	# t = html.findAll(name='img')
	# print (len(t))
	# web = urllib.request.urlopen("https://movie.douban.com/typerank?type_name=dongzuo&type=5&interval_id=100:90&action=")
	# cao = web.read()
	# soup = BeautifulSoup(cao,'html5lib')
	# k = soup.findAll('img')
	# print (len(k))



	

	


if __name__ == '__main__':
	__main__()


