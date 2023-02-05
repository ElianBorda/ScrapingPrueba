import requests
from bs4 import BeautifulSoup

def printList(list):
	for elem in list:
		print(elem)

def extractTitleVulHub(urlPage):
	url = urlPage
	ua = {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}
	res = requests.get(url, headers=ua)
	soup = BeautifulSoup(res.text, "html.parser")
	allTitles = titleCardsList(soup)
	return extendOtherTitles(allTitles, ua, soup)

def extendOtherTitles(list, ua, sp):
	n = 1
	allTitles = list
	soup = sp

	while soup.find("a", class_="next-page-link") != None:
		n =  n + 1
		url = refreshNextPage(n)
		res = requests.get(url, headers=ua)
		soup = BeautifulSoup(res.text, "html.parser")
		allTitles.extend(titleCardsList(soup))

	return allTitles

def refreshNextPage(numberPage):
	return "https://www.vulnhub.com/?page=" + str(numberPage)


def printAllTitlePage(soup):
# Dado una pagina, imprime en pantalla los titulos de cada carta de la misma.
	for title in titleCardsList(soup):
		print(title)

def titleCardsList(soup):
# Dado una pagina, devuelve una lista con los titulos de cada carta
	cardsClears = []

	for card in contentCardsList(soup):
		cardsClears.append(cardClear(card))
	return cardsClears

def cardClear(card):
# Dado una carta, devuelve el titulo en limpio de la misma
	return card.find("div", class_="card-title").text.strip()

def contentCardsList(soup):
# Devuelve una lista cuyos elementos son los html de cada carta de una pagina
	return contentCards(soup).find_all("div", class_="card")

def contentCards(soup):
# Devuelve el HTML de todas las Cartas de una pagina
	return soup.find("div", class_="card-container")




# MAIN ---------------------------------------------------------------

if __name__ == '__main__':
	printList(extractTitleVulHub("https://www.vulnhub.com/"))

