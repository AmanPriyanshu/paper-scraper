import os
import sys

# python ______.py 0 0 coronavirus

if __name__ == "__main__":
	system_type = int(sys.argv[1])
	choice = int(sys.argv[2])
	search_term = ' '.join(sys.argv[3:])
	print(search_term)
	
	if system_type == 0:
		os.system("cls")
	else:
		os.system("clear")
	print('Searching and Scraping...')
	if choice == 0:
		n = 0
		os.system('python ./Google_Scholar/google_scholar/google_scholar/spiders/google_scholar_cite.py '+str(n)+' '+search_term)