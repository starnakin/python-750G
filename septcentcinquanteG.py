# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

import urllib.parse
import urllib.request

import re


class Recipes(object):

	@staticmethod
	def search(query_dict):
		"""
		Search recipes parsing the returned html data.
		"""
		url = "http://www.750g.com/recettes_%s.htm" % (query_dict["recherche"].replace(" ", "_"))

		html_content = urllib.request.urlopen(url).read()
		soup = BeautifulSoup(html_content, 'html.parser')

		search_data = []
		articles = soup.findAll("section", {'class': re.compile('recipe-\d+')})

		for article in articles:
			data = {}
			try:
				data["name"] = article.find("h2", {"class": "c-row__title c-recipe-row__title"}).get_text().strip(' \t\n\r')
				data["url"] = article.find("a", {"class": "u-link-wrapper"})['href']
				data["desc"] = article.find("p", {"class": "c-row__desc"}).get_text().strip(' \t\n\r')
				try:
					data["image"] = article.find("div", {"class": "c-row__media c-recipe-row__media"}).find("img")["data-src"][7:]
				except Exception as e1:
					data["image"] = ""
					pass
			except Exception as e2:
				print(e2)
				pass
			search_data.append(data)

		return search_data

	@staticmethod
	def get(uri):
		base_url = "http://www.750g.com"
		url = base_url + uri

		html_content = urllib.request.urlopen(url).read()
		soup = BeautifulSoup(html_content, 'html.parser')

		#image_url = str(soup.find("picture", {"class": "recipe-cover-blur"}).find("img").text)
		image_url=soup.find("picture", {"class": "recipe-cover-blur"}).find('img')["src"]

		list_ingredients=[]
		ingredients_data = soup.findAll("span", { "class": "recipe-ingredients-item-label"})
		for i in ingredients_data:
			list_ingredients.append(i.text)

		rate = (soup.find("span", {"class": "rating-grade"}).text).replace("\n        ", "")

		preparation_data = soup.findAll("div", {"class": "recipe-steps-text"})

		list_instructions = []
		for i in preparation_data:
			list_instructions.append(i.text)

		try:
			name=soup.find("span", {"class":"recipe-title"}).text
		except:
			name="Inconnu"
   
		data = {
			"url": "http://www.750g.com/"+uri,
			"image": image_url,
			"name": name,
			"ingredients": list_ingredients,
			"instructions": list_instructions,
			"rate": rate
		}

		return data








