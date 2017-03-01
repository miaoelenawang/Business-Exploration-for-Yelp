
# coding: utf-8

# In[53]:

import requests
from lxml import html
import lxml.html as lx
import re
import json

#url = "https://www.yelp.com/biz/craftsman-and-wolves-the-den-san-francisco-2"


# In[54]:

#page = requests.get(url)
#tree = lx.fromstring(page.content)


# In[55]:
def extract_single_page(url):
	#url = "https://www.yelp.com/biz/craftsman-and-wolves-the-den-san-francisco-2"
	page = requests.get(url)
	tree = lx.fromstring(page.content)
	try:
		claim = tree.xpath('//div[@class="u-nowrap claim-status_teaser js-claim-status-hover"]')[0].text_content()
		claims = re.sub(" ","",claim).strip('\n')
	except:
		claims = None
	try:
		health_inspect = tree.xpath('//dd[@class="nowrap health-score-description"]')[0].text_content()
		hl_inspect = re.sub(" ","",health_inspect).strip('\n')
	except:
		hl_inspect = None
	week = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
	hours = {i : None for i in week}
	hour = tree.xpath('//table[@class="table table-simple hours-table"]//tr')
	hou = {i.xpath('th')[0].text_content().strip():i.xpath('td')[0].text_content().strip() for i in hour}
	for wkday in week:
		try:
			hours.update({wkday:hou[wkday]})
		except:
			hours.update({wkday:None}) 	
	try:
		more_info= tree.xpath('//div[@class="short-def-list"]')[0].text_content()
		more_info= [ii for ii in re.sub(" ","",more_info).split('\n') if ii not in ['']]
		more_info = {more_info[i]:more_info[i+1] for i in range(0,len(more_info)-1,2)}

	except:
		more_info = None
	try: 
		loc = tree.find_class('lightbox-map hidden')[0].get('data-map-state')
		d = json.loads(loc)
		latitude = d.get('center').get('latitude')
		longitude = d.get('center').get('longitude')
	except:
		latitude = None
		longitude = None

	li = tree.xpath("//div/h3[text()='People also viewed']/../ul/li")
	related3 = {'related'+str(i):None for i in range(3)}
	try:
		related = [i.find_class('js-analytics-click')[0].get('href').split('/')[2].split('?')[0] for i in li]
		k = 0
		for j in related[:2]:
			related3.update({'related'+str(k):j}) 
			k +=1
	except:    
		related3 = {'related'+str(i):None for i in range(3)}

	Business = {"claimed status":claims,"health inspect":hl_inspect,"more information":more_info, 'latitude':latitude,'longitude':longitude}
	Business.update(hours)  
	Business.update(related3)  
	return Business
	



def claimed_status(tree):
	try:
		claim = tree.xpath('//div[@class="u-nowrap claim-status_teaser js-claim-status-hover"]')[0].text_content()
		claims = re.sub(" ","",claim).strip('\n')
	except:
		claims = "none"
	return({"claimed status":claims})



# In[56]:

def health_inspection(tree):
	try:
		health_inspect = tree.xpath('//dd[@class="nowrap health-score-description"]')[0].text_content()
		hl_inspect = re.sub(" ","",health_inspect).strip('\n')
	except:
		hl_inspect = "none"
	return({"health inspect":hl_inspect})



# In[57]:

def open_hours(tree):
	try:
		hours = tree.xpath('//table[@class="table table-simple hours-table"]')[0].text_content()
		hours = [ii for ii in re.sub(" ","",hours).split('\n') if ii not in ['']]
		hour = {hours[i]:hours[i+1] for i in range(0,len(hours)-2,2)}
	except:
		hour = {}
	week = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
	for wkday in week:
		try: 
			hour[wkday]
		except:
			hour.update({wkday:"none"})   
	return(hour)

#hour




def more_information(tree):
	try:
		more_info= tree.xpath('//div[@class="short-def-list"]')[0].text_content()
		more_info= [ii for ii in re.sub(" ","",more_info).split('\n') if ii not in ['']]
		more_info = {more_info[i]:more_info[i+1] for i in range(0,len(more_info)-1,2)}
		more_info = {"more information":more_info}
	except:
		more_info = {"more information":"none"}
	return(more_info)

								




def conbine_dict(tree):
	Dict = {};
	Dict.update(claimed_status(tree))
	Dict.update(health_inspection(tree))
	for key,value in open_hours(tree).items():
		Dict.update({key:value})
	try:
		for ii in more_information(tree).items():
			Dict.update(ii)
	except:
		Dict.update(more_information(tree))
	return(Dict)
	


#



