import csv
import cPickle
import scrapy
from bs4 import BeautifulSoup
from pathlib import Path

class QuotesSpider(scrapy.Spider):
	name = "indivitual"
	#start_urls= ['http://www.thelearningpoint.net/home/school-listings/cbse-26/BASELIUS-THOMAS-I-CATHOLICOSE-PUBLIC-SCHOOL--BTC-PUBLIC-SCHOOL--BTC-PUBLIC-SCHOOL-PUTHENCRUZ--P-O-ERNAKULAM---Dist--930840']

#	index = {}
#	total_selected = 0
#	total_counted = 0

	def start_requests(self):
		base_url = 'http://www.thelearningpoint.net/system/app/pages/search?scope=search-site&q=school&offset='

		print "Scraping Started...please wait to finish transactions......."

		for counter in xrange(0,55110,10):
			url = base_url+str(counter)
			yield scrapy.Request(url=url, callback=self.parse_page)

	def parse_page(self, response):
		page = response.xpath('//td[@id="col0"]').css('div.sites-search-result h3 a::attr(href)').extract()
		for i in page:
			link = response.urljoin(i)
			#print "next page",link
			#inp = input()
			try:
				yield scrapy.Request(url=link, callback=self.parse_school)
#				total_counted = total_counted + 1
#				print "Total Counted till Now: ",total_counted
			except:
				print "could not go to indivitual school"
				inp = input()

	def parse_school(self,response):
		print "scraping school data:"
		#inp = input()
		data = {}

		try:
			page = response.xpath('//div[@id="sites-canvas-main-content"]/table/tbody/tr/td/div').extract()
		except:
			print "Error : ",response
			inp = input()

		try:
			soup = BeautifulSoup(page[len(page)-3],'html.parser')
			tables = soup.find_all('table')
			table = tables[0].find_all('td')

			data['extra'] = unicode('')

			for i in xrange(1,len(page)-3):
				soup1 = BeautifulSoup(page[i],"html.parser")
				if soup1.string is not None:
					data['extra'] = data['extra'] + unicode(' ') + soup1.string.strip()
		except:
			soup = BeautifulSoup(page[len(page)-2],'html.parser')
			tables = soup.find_all('table')
			table = tables[0].find_all('td')

			data['extra'] = unicode('')

			for i in xrange(1,len(page)-2):
				soup1 = BeautifulSoup(page[i],"html.parser")
				if soup1.string is not None:
					data['extra'] = data['extra'] + unicode(' ') + soup1.string.strip()

		#data ={}
		try:
			data['Name of Institution'] = table[2].string.strip() #name of institute
		except:
			data['Name of Institution']=""
		try:
			data['Affiliation Number'] = table[4].string.strip() #affiliation number
		except:
			data['Affiliation Number'] = ""
		try:
			data['State'] = table[6].string.strip() #State
		except:
			data['State'] = ""
		try:
			data['District'] = table[8].string.strip() #District
		except:
			data['District'] = ""
		try:
			data['Postal Address'] = table[10].string.strip() #Postal Address
		except:
			data['Postal Address'] = ""
		try:
			data['Pin Code'] = table[12].string.strip() #Pin Code
		except:
			data['Pin Code'] = ""
		try:
			data['Phone Office 1'] = table[16].td.string.strip() #Phone Office_1
		except:
			data['Phone Office 1'] = ""
		try:
			data['Phone Office 2'] = table[17].string.strip() #Phone Office_2
		except:
			data['Phone Office 2'] = ""
		try:
			data['Phone Residence 1'] = table[19].td.string.strip() #Phone Residence_1
		except:
			data['Phone Residence 1'] = ""
		try:
			data['Phone Residence 2'] = table[20].string.strip() #Phone Residence_2
		except:
			data['Phone Residence 2'] = ""
		try:
			data['FAX No'] = table[22].string.strip() #Fax Number
		except:
			data['FAX No'] = ""
		try:
			data['Email'] = table[24].string.strip() #email id
		except:
			data['Email'] = ""
		try:
			data['Website'] = table[26].string.strip() #Website
		except:
			data['Website'] = ""
		try:
			data['Year of Foundation'] = table[28].string.strip() #Year of Foundation
		except:
			data['Year of Foundation'] = ""
		try:
			data['Date of First Openning of School'] =  table[30].string.strip() #openning
		except:
			data['Date of First Openning of School'] = ""
		try:
			data['Name of Principal/ Head of Institution'] = table[32].string.strip() #Head
		except:
			data['Name of Principal/ Head of Institution'] = ""
		try:
			data['Sex'] = table[34].string.strip()
		except:
			data['Sex'] = ""
		try:
			data['Principal Education/Professional Qualifications'] = table[36].string.strip()
		except:
			data['Principal Education/Professional Qualifications'] = ""
		try:
			data['Number of Experience Years'] = table[38].string.strip()
		except:
			data['Number of Experience Years'] = ""
		try:
			data['Administrative'] = table[40].string.strip()
		except:
			data['Administrative'] = ""
		try:
			data['Teaching'] =  table[42].string.strip()
		except:
			data['Teaching'] = ""
		try:
			data['Status of The School'] = table[44].string.strip()
		except:
			data['Status of The School'] = ""
		try:
			data['Type of affiliation'] = table[46].string.strip()
		except:
			data['Type of affiliation'] = ""
		try:
			data['Affiliation Period From'] = table[49].string.strip()
		except:
			data['Affiliation Period From'] = ""
		try:
			data['Affiliation Period To'] = table[51].string.strip()
		except:
			data['Affiliation Period To'] = ""
		try:
			data['Name of Trust/ Society/ Managing Committee'] = table[53].string.strip()
		except:
			data['Name of Trust/ Society/ Managing Committee'] = ""
		try:
			table = tables[2].find_all('td')
			data['locality'] = table[5].string.strip()
		except:
			data['locality'] = ""


#		with open("output/"+data['State'].lower()+".csv","a") as myFile:
		check = Path("output/data.csv")
		if not check.is_file():
			with open("output/data.csv","wb") as myFile:
				fieldnames = ['Name of Institution','Affiliation Number', 'State', 'District', 'locality', 'Postal Address', 'Pin Code', 'Phone Office 1', 'Phone Office 2', 'Phone Residence 1', 'Phone Residence 2', 'FAX No', 'Email', 'Website', 'Year of Foundation', 'Date of First Openning of School', 'Name of Principal/ Head of Institution', 'Sex', 'Principal Education/Professional Qualifications', 'Number of Experience Years', 'Administrative', 'Teaching', 'Status of The School', 'Type of affiliation', 'Affiliation Period From', 'Affiliation Period To', 'Name of Trust/ Society/ Managing Committee', 'extra']

				writer = csv.DictWriter(myFile,fieldnames=fieldnames)
				writer.writeheader()

		with open("output/data.csv","a") as myFile:
			fieldnames = ['Name of Institution','Affiliation Number', 'State', 'District', 'locality', 'Postal Address', 'Pin Code', 'Phone Office 1', 'Phone Office 2', 'Phone Residence 1', 'Phone Residence 2', 'FAX No', 'Email', 'Website', 'Year of Foundation', 'Date of First Openning of School', 'Name of Principal/ Head of Institution', 'Sex', 'Principal Education/Professional Qualifications', 'Number of Experience Years', 'Administrative', 'Teaching', 'Status of The School', 'Type of affiliation', 'Affiliation Period From', 'Affiliation Period To', 'Name of Trust/ Society/ Managing Committee', 'extra']

			writer = csv.DictWriter(myFile,fieldnames=fieldnames)

			writer.writerow({
				'Name of Institution':data['Name of Institution'],
				'Affiliation Number':data['Affiliation Number'],
				'State':data['State'],
				'District':data['District'],
				'locality':data['locality'],
				'Postal Address':data['Postal Address'],
				'Pin Code':data['Pin Code'],
				'Phone Office 1':data['Phone Office 1'],
				'Phone Office 2':data['Phone Office 2'],
				'Phone Residence 1':data['Phone Residence 1'],
				'Phone Residence 2':data['Phone Residence 2'],
				'FAX No':data['FAX No'],
				'Email':data['Email'],
				'Website':data['Website'],
				'Year of Foundation':data['Year of Foundation'],
				'Date of First Openning of School':data['Date of First Openning of School'],
				'Name of Principal/ Head of Institution':data['Name of Principal/ Head of Institution'],
				'Sex':data['Sex'],
				'Principal Education/Professional Qualifications':data['Principal Education/Professional Qualifications'],
				'Number of Experience Years':data['Number of Experience Years'],
				'Administrative':data['Administrative'],
				'Teaching':data['Teaching'],
				'Status of The School':data['Status of The School'],
				'Type of affiliation':data['Type of affiliation'],
				'Affiliation Period From':data['Affiliation Period From'],
				'Affiliation Period To':data['Affiliation Period To'],
				'Name of Trust/ Society/ Managing Committee':data['Name of Trust/ Society/ Managing Committee'], 
				'extra':data['extra'] })


		with open("index.txt","wb") as myFile:
			cPickle.dump(data,myFile)
			print "Done"
			#inp = input()

		print "Scrapped: ",response
#		total_selected = total_selected + 1
#		print "Total Selected: ",total_selected
