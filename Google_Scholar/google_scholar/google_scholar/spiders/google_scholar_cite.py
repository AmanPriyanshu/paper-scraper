import scrapy  
from scrapy.crawler import Crawler
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import os
import regex as re
import sys
import pandas as pd
#https://scholar.google.com/scholar?start=0&q=%22covid+19%22&hl=en&scisbd=1&as_sdt=0,5


class google_scholar_cite(scrapy.Spider): 
	name = 'google_scholar_cite'
	
	def parse(self, response):
		global link_titles, abstracts, journals, authors, citations
		#sel = Selector(text=response, type="html")
		#titles = response.css(".gs_rt a::text").extract()
		data_link_titles = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "gs_rt", " " ))]//a').extract()
		link_titles = data_link_titles
		data_abstract = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "gs_rs", " " ))]').extract()
		abstracts = data_abstract
		
		authors = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "gs_a", " " ))]').extract()
		citations = response.css('.gs_or_cit+ a::text').extract()
		citations = [int(i[len('Cited by '):]) for i in citations]
		


		
 
      
def search_termer(search_term):
	name = "google_scholar_cite"
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
	search_term = search_termer(search_term)
	print(search_term)

	urls = 'https://scholar.google.com/scholar?start='+str(n)+'&q='+search_term+'&hl=en&as_sdt=0,5'
	print(urls)
	#exit()
	process = CrawlerProcess({'USER_AGENT': 'Mozilla/5.0'})
	process.crawl(google_scholar_cite, start_urls=[urls])
	process.start()
	#https://scholar.google.com/scholar?start=30&q=covid+19&hl=en&as_sdt=0,5

	os.system('cls')
	final_titles = []
	final_links = []
	final_abstracts = []
	final_journals = []
	final_authors = []
	final_citations = citations

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
		if len(abstracts) == 10:
			i = abstracts[index]
			abstract = i[i.find('<div class="gs_rs">')+len('<div class="gs_rs">'):i.find('</div>')]
			abstract = abstract.replace('<b>', '')
			abstract = abstract.replace('</b>', '')
			abstract = abstract.replace('<br>', '')
			#print(abstract)
			final_abstracts.append(abstract)
		else:
			final_abstracts.append(' ')
		author = authors[index]
		author = author[author.find('<div class="gs_a">')+len('<div class="gs_a">'):-len('</div>')]
		author = re.sub(r'\<.*?\>', '', author)
		author = author[:author.find('-')]
		final_authors.append(author)


	
	dict_days = {'titles':final_titles, 
		'authors':final_authors,  
		'journals':final_journals, 
		'abstracts':final_abstracts,
		'links':final_links,
		'citations':final_citations}
	#print(dict_days)
	data_cite = pd.DataFrame(dict_days)
	search_term = search_term.replace('+', '_')
	data_cite.to_csv('./data/'+search_term+'_cite.csv', header=False, mode='a', index=False)
	print(data_cite.head)


