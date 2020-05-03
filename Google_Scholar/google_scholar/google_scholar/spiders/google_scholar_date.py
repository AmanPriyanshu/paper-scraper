import scrapy  
from scrapy.crawler import Crawler
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import os
from datetime import datetime, timedelta
import regex as re
import pandas as pd
import sys

#https://scholar.google.com/scholar?start=0&q=%22covid+19%22&hl=en&scisbd=1&as_sdt=0,5


class google_scholar_date(scrapy.Spider): 
	name = 'google_scholar_date'
	
	def parse(self, response):
		global link_titles, abstracts, journals, days, authors
		#sel = Selector(text=response, type="html")
		#titles = response.css(".gs_rt a::text").extract()
		data = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "gs_rt", " " ))]/a')
		data_titles = data.extract()
		link_titles = data_titles
		days = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "gs_age", " " ))]/text()').extract()
		authors = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "gs_a", " " ))]').extract()
		abstracts = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "gs_rs", " " ))]').extract()


def search_termer(search_term):
	name = "google_scholar_date"
	search = [i for i in search_term.split(' ') if not (i=='')]
	search_term = '+'.join(search)
	print('Searching for: '+search_term+'...')
	return search_term

if __name__ == "__main__":
	try:
		n = int(sys.argv[1])
		search_term = ' '.join(sys.argv[2:])
	except:
		n = 0
		search_term = ' '.join(sys.argv[1:])
	print(n)
	print(search_term)

	search_term = search_termer(search_term)
	print(search_term)

	urls = 'https://scholar.google.com/scholar?start='+str(n)+'&q=%22'+search_term+'%22&hl=en&scisbd=1&as_sdt=0,5'
	print(urls)

	process = CrawlerProcess({'USER_AGENT': 'Mozilla/5.0'})
	process.crawl(google_scholar_date, start_urls=[urls])
	process.start()
	#https://scholar.google.com/scholar?start=30&q=covid+19&hl=en&as_sdt=0,5
	#exit()
	os.system('cls')
	final_titles = []
	final_links = []
	final_abstracts = []
	final_journals = []
	final_days =[]
	final_authors = []
	#final_journals = journals
	print(len(link_titles))
	for index in range(len(link_titles)):
		i = link_titles[index]
		title = i[i.find('">')+2:i.find('</a>')]
		title = title.replace('<b>', '')
		title = title.replace('</b>', '')
		final_titles.append(title)
		link = i[i.find('href="')+len('href="'): i.find('" data-clk="')]
		final_links.append(link)
		
		journal = link[link.find('//')+2:]
		journal = journal[:journal.find('/')]
		final_journals.append(journal)
		day = days[index]
		day = day[:day.find(' days')]
		d = datetime.today() - timedelta(days=int(day))
		final_days.append(str(d.date()))

		author = authors[index]
		author = author[author.find('<div class="gs_a">')+len('<div class="gs_a">'):-len('</div>')]
		author = re.sub(r'\<.*?\>', '', author)
		author = author[:author.find('-')]
		final_authors.append(author)

		abstract = abstracts[index]
		abstract = re.sub(r'\<.*?\>', '', abstract)
		abstract = abstract[abstract.find('-')+1:]
		print(abstract)
		final_abstracts.append(abstract[:-1])
	dict_days = {'titles':final_titles, 
		'authors':final_authors, 
		'journals':final_journals, 
		'links':final_links,
		'abstracts':final_abstracts,
		'date':final_days}

	data_date = pd.DataFrame(dict_days)
	search_term = search_term.replace('+', '_')
	data_date.to_csv('./data/'+search_term+'_date.csv', header=False, mode='a', index=False)
	print(data_date.head)