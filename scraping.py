import requests
from bs4 import BeautifulSoup
import pprint
import os.path
from os import path
import json
import random
import time

def load(filename):
	with open(filename,"r+")as c:
		# file_data=content.read()
		file_data=json.load(c)
		return file_data
def dump(data,filename):
	with open(filename,'w')as content:
		json.dump(data,content)

url="https://www.imdb.com/india/top-rated-indian-movies/?ref_=nv_mv_250_in"
page=requests.get(url)
# print(page.text)
soup=BeautifulSoup(page.text,'html.parser')
def scrape_top_list():
	main_div=soup.find('div',class_='lister')
	tbody=main_div.find('tbody',class_='lister-list')
	trs=tbody.find_all('tr')

	movie_ranks=[]
	movie_name=[]
	year_of_release=[]
	movie_urls=[]
	movie_ratings=[]
	for tr in trs:
		rank=''
		position=tr.find('td',class_='titleColumn').get_text().strip()
		for i in position:
			if '.' not in i:
				rank=rank+i
			else:
				break
		movie_ranks.append(rank)
		title=tr.find('td',class_='titleColumn').a.get_text()
		movie_name.append(title)
		year=tr.find('span',class_='secondaryInfo').get_text()
		year_of_release.append(year)
		rating=tr.find('td',class_='ratingColumn imdbRating').strong.get_text()
		movie_ratings.append(rating)
		link=tr.find('td',class_='titleColumn').a['href']
		movie_link="https://www.imdb.com"+link
		movie_urls.append(movie_link)

	top_movies=[]
	detail={'Position':'','Name':'','Year':'','Rating':'','Url':''}
	for i in range(0,len(movie_ranks)):
		detail['Position']=int(movie_ranks[i])
		detail['Name']=str(movie_name[i])
		year_of_release[i]=year_of_release[i][1:5]
		detail['Year']=int(year_of_release[i])
		detail['Url']=movie_urls[i]
		detail['Rating']=float(movie_ratings[i])
		top_movies.append(detail)
		# top_movies.append('                                                                   ')
		detail={'Position':'','Name':'','Year':'','Rating':'','Url':''}
	return top_movies
exists=path.exists("/home/deepanshu/Documents/web_scraping/task1.json")
if not exists:
	dump(scrape_top_list(),"task1.json")
	top_movies= load("task1.json")
else:
	top_movies= load("task1.json")

# pprint.pprint(top_movies)

# ####------------------------------------------Task-2----------------------------------------------
def group_by_year():
	year_list=[]
	for i in top_movies:
		year_list.append(i['Year'])
	years=set(year_list)

	top_movies_list=[]
	movies={}
	for i in years:
		List=[]
		for j in top_movies:
			if i == j['Year']:
				List.append(j)
		movies[i]=List
	# top_movies_list.append(movies)
	return movies

exists=path.exists("/home/deepanshu/Documents/web_scraping/task2.json")
if not exists:
	dump(group_by_year(),"task2.json")
	part2= load("task2.json")
else:
	part2= load("task2.json")

# pprint.pprint(part2)

######-------------------------------------------------------Task-3----------------------------------

def group_by_decade():
	def init():
		for i in part2:
			return i
	j=init()
	j=int(j)
	j=j-(j%10)
	# print(part2['1955'])

	movies={}
	List=[]
	for i in part2:
		if int(i) in range(j,j+10):
			List.append(part2[i])
		else:
			movies[j]=List
			j+=10
			List=[]
	else:
		movies[j]=List
	return movies

exists=path.exists("/home/deepanshu/Documents/web_scraping/task3.json")
if not exists:
	dump(group_by_decade(),"task3.json")
	part3= load("task3.json")
else:
	part3= load("task3.json")

# pprint.pprint(part3)

# ###-----------------------------------------------Task-4-----------------------------

def scrap_movie_detail(movie_url):
	#Task-9
	random_sleep=random.randint(1,3)
	time.sleep(random_sleep)

	#Task-4
	page=requests.get(movie_url)
	soup=BeautifulSoup(page.text,'html.parser')

##------------finding_name--------------------------
	name_div=soup.find('div',class_='title_wrapper')
	h1=name_div.find("h1").text
	movie_name=''
	for i in h1:
		if i!='(':
			movie_name=movie_name+i
		else:
			break

##---------------finding_director------------------------
	dir_div=soup.find('div',class_="credit_summary_item")
	directors_name=dir_div.find_all('a')
	movie_dir=[i.get_text() for i in directors_name]
	# print(movie_dir)
	
##----------------findinng_time---------------------------
	sub_div=soup.find('div',class_='subtext')
	name=sub_div.find('time').get_text().strip().split()
	
	def Time(a):
		time=''
		for i in a:
			if i.isdigit():
				time=time+i
		return int(time)
	hr=0
	minuts=0
	for t in range(len(name)):
		if t==0:
			hr=Time(name[t])*60
		else:
			minuts=Time(name[t])
	movie_time=hr+minuts
	# print(movie_time)

##-------------------------finding_genere---------------
	genere=sub_div.find_all('a')
	movie_generes=[i.get_text() for i in genere]
	movie_generes.pop()
	# print(movie_generes)

##-------------------------finding_poster_url-----------
	poster_div=soup.find('div',class_='poster')
	movie_poster=poster_div.a['href']
	# print(movie_poster)

##-------------------------finding_country_name_&_language----------
	country_div=soup.find('div',attrs={"class": "article", "id": "titleDetails"})
	txt = country_div.find_all('div', class_ = "txt-block")
	for i in txt:
		if i.find('h4') in i:
			j = (i.find('h4', class_= "inline").text)
			if j == "Country:":
				movie_country=i.find('a').text

			elif j == "Language:":
				language=i.find_all('a')
				movie_language=[]
				for lang in language:
					movie_language.append(lang.text)
	# print(movie_country)
	# print(movie_language)

	movie_bio=soup.find('div',class_='summary_text').get_text().strip()
	# print(movie_bio)

	#       ========================Task13---------finding_cast------------===============================
	movie_id=(movie_url[27:36])
	exists=path.exists("/home/deepanshu/Documents/web_scraping/%s.json"%movie_id)
	if exists:
		movie_cast=load('%s.json'%movie_id)
	else:
		movie_cast=scrape_movie_cast(cast_url,movie_id)




##---------------------------creating dictionary of above datas-------------------------
	personal_detail={"name":"","director":"","country":"","language":"","poster_image_url":"","bio":"","runtime":"","genere":"","cast":""}
	personal_detail["name"]=movie_name
	personal_detail["director"]=movie_dir
	personal_detail["country"]=movie_country
	personal_detail["language"]=movie_language
	personal_detail["poster_image_url"]=movie_poster
	personal_detail["bio"]=movie_bio
	personal_detail["runtime"]=movie_time
	personal_detail["genere"]=movie_generes
	personal_detail["cast"]=movie_cast
	return(personal_detail)

# pprint.pprint(scrap_movie_detail("https://www.imdb.com/title/tt8291224/?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=690bec67-3bd7-45a1-9ab4-4f274a72e602&pf_rd_r=4Y4CWCTB6VVSVTCYYBVJ&pf_rd_s=center-4&pf_rd_t=60601&pf_rd_i=india.top-rated-indian-movies&ref_=fea_india_ss_toprated_tt_3"))

# ###=================================================Task-5===================================================================

def get_movie_list_detail():
	get_movie_list_detail=[]
	for Url in top_movies:
		details=scrap_movie_detail(Url['Url'])
		get_movie_list_detail.append(details)
	return get_movie_list_detail

exists=path.exists("/home/deepanshu/Documents/web_scraping/task5.json")
if not exists:
	dump(get_movie_list_detail(),"task5.json")
	part5= load("task5.json")
else:
	part5= load("task5.json")

# pprint.pprint(part5[:10])

###=============================================Task-6 ========================================================================
language_dict={}
for i in part5:
	for lang in i['language']:
		if lang not in language_dict:
			language_dict[lang]=""
# print(language_dict)

for i in language_dict:
	count=0
	for lang in part5:
		if i in lang['language']:
			count+=1
	language_dict[i]=count
# print(language_dict)

###===============================================Task-7========================================================================
directors_dict={}
for i in part5[:10]:
	for dirct in i['director']:
		if dirct not in directors_dict:
			directors_dict[dirct]=""
for i in directors_dict:
	count=0
	for dirct in part5[:10]:
		if i in dirct['director']:
			count+=1
	directors_dict[i]=count
# pprint.pprint(directors_dict)


###======================================Task-10================================================================================

def analysis_language_and_directors(movies_list):
	#finding directors list
	directors_list=[]
	for i in movies_list:
		for dirct in i['director']:
			if dirct not in directors_list:
				directors_list.append(dirct)
	dirct_dict={}
	for i in directors_list:
		lang_dict={}
		for j in language_dict:
			count=0
			for k in movies_list:
				if i in k['director'] and j in k['language']:
					count+=1
			if count>0:
				lang_dict[j]=count
		dirct_dict[i]=lang_dict
	return dirct_dict

# pprint.pprint(analysis_language_and_directors(part5))

###============================================Task-11==============================================================

def analysis_movie_genere(movies_list):
	# finding_movies_genre_list
	genere_list=[]
	for i in movies_list:
		for j in (i['genere']):
			if j not in genere_list:
				genere_list.append(j)
	# return genere_list
	genere_dict={}
	for i in genere_list:
		count=0
		for k in movies_list:
			if i in k['genere']:
				count+=1
		genere_dict[i]=count
	return genere_dict

# pprint.pprint(analysis_movie_genere(part5))

###=====================================Task-12========================================================
def cast_url():
	for i in top_movies:
		page=requests.get(i['Url'])
		soup=BeautifulSoup(page.text,'html.parser')
		main_div=soup.find('div',attrs={"class":"article","id":"titleCast"})
		cast_div=main_div.find('div',class_="see-more")
		cast_url=cast_div.a['href']
		return cast_url
exists=path.exists("/home/deepanshu/Documents/web_scraping/cast_url.json")
if exists:
	cast_url=load('cast_url.json')
else:
	dump(cast_url(),'cast_url.json')
	cast_url=load('cast_url.json')
# print(cast_url)

def scrape_movie_cast(cast_url,movie_id):
	movie_cast_list=[]
	page=requests.get("https://www.imdb.com/title/%s/"%movie_id+cast_url)
	soup=BeautifulSoup(page.text,'html.parser')
	table=soup.find('table',class_='cast_list')
	trs=table.findAll('tr')

	for tr in trs:	
		movie_cast={'imdb_id':'',"name":""}
		if tr.find('td',class_=""):
			ID=tr.find('td',class_="").a['href'][6:15]
			movie_cast['imdb_id']=ID
			name=tr.find('td',class_="").text.strip()
			movie_cast['name']=name
			movie_cast_list.append(movie_cast)
	return movie_cast_list

# pprint.pprint(scrape_movie_cast(cast_url))

movie_cast_detail_list=[]
for i in top_movies:
	movie_id=(i['Url'][27:36])

	exists=path.exists("/home/deepanshu/Documents/web_scraping/%s.json"%movie_id)
	if exists:
		task12=load('%s.json'%movie_id)
	else:
		dump(scrape_movie_cast(cast_url,movie_id),'%s.json'%movie_id)
		task12=load('%s.json'%movie_id)
	movie_cast_detail_list.append(task12)
	# pprint.pprint(task12)
# print(movie_cast_detail_list)

#####==================================Task13====================================================================

# pprint.pprint(scrap_movie_detail("https://www.imdb.com/title/tt8291224/?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=690bec67-3bd7-45a1-9ab4-4f274a72e602&pf_rd_r=4Y4CWCTB6VVSVTCYYBVJ&pf_rd_s=center-4&pf_rd_t=60601&pf_rd_i=india.top-rated-indian-movies&ref_=fea_india_ss_toprated_tt_3"))

###====================================Task15	===================================================================
actors_list=[]
total_actors_list=[]
for movie in movie_cast_detail_list:
	for dict in movie:
		# print(dict['name'])
		actors_detail={}
		actors_detail['id']=dict['imdb_id']
		actors_detail['name']=dict['name']
		total_actors_list.append(actors_detail)
#catching of total_actor_list
exists=path.exists("/home/deepanshu/Documents/web_scraping/total_actors_list.json")
if exists:
	total_actors_list=load('total_actors_list.json')
else:
	dump(total_actors_list,'total_actors_list.json')
	total_actors_list=load('total_actors_list.json')
# print(len(total_actors_list))

for i in total_actors_list:
	if i not in actors_list:
		actors_list.append(i)
#catcing of actors_list
exists=path.exists("/home/deepanshu/Documents/web_scraping/actors_list.json")
if exists:
	actors_list=load('actors_list.json')
else:
	dump(actors_list,'actors_list.json')
	actors_list=load('actors_list.json')
# print(len(actors_list))

#creating actor_dict or the solution of task 15
actors_dict={}
for i in actors_list:
	count=0
	name_num={}
	for j in total_actors_list:
		if i==j:
			count+=1
	name_num['name']=i['name']
	name_num['num_movies']=count
	actors_dict[i['id']]=name_num
# pprint.pprint(actors_dict)

###=======================================Task14========================================================

### movie_cast_detail_list
Actors_list=[]
for i in movie_cast_detail_list[:5]:
		Actors_list.append(i[:5])
# print(Actors_list) 
for i in Actors_list:
	for j in i:
		count=0
		if j in a[:i] or j in a[(i+1):]


















# Actors_list=[]
# for i in movie_cast_detail_list[:5]:
# 	for j in i[:5]:
# 		Actors_list.append(j)
# set_list=[]
# for i in Actors_list:
# 	if i not in set_list:
# 		set_list.append(i)
# # print(Actors_list)
# # print()
# # print(set_list)

# # id_dict={}
# # for i in set_list:
# # 	co_act={}
# # 	for j in Actors_list:
# # 		count=0
# # 		if j==i:
# # 			count+=1
# # 	if count>1:
# # 		co_act['imdb_id']=j['imdb_id']
# # 		co_act['name']=j['name']
# # 		co_act['num_movies']=count
# # 		co_act_list.append(freq_act)
# # 	co_act['name']=i['name']
# # 	co_act["frequent_co_actors"]=co_act_list

# # 	id_dict[i['imdb_id']]=co_act
# # print(id_dict)