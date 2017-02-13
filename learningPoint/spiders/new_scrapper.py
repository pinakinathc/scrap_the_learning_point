import csv
import cPickle
import scrapy
from bs4 import BeautifulSoup
from pathlib import Path

class QuotesSpider(scrapy.Spider):
    name = "scrapper"
  #  start_urls=['http://www.thelearningpoint.net/home/school-listings/cbse-13/Bayonet-School-Bayonet-School-C-O-Infantry-School--Mhow-1030454']

    def start_requests(self):
		base_url = 'http://www.thelearningpoint.net/system/app/pages/search?scope=search-site&q=school&offset='

		print "Scraping Started...please wait to finish transactions......."

		for counter in xrange(0,55110,10):
			url = base_url+str(counter)
			print "url to be scrapped: ",url
			yield scrapy.Request(url=url, callback=self.parse_page)
        
    def parse_page(self, response):
	page = response.xpath('//td[@id="col0"]').css('div.sites-search-result h3 a::attr(href)').extract()
	for i in page:
            link = response.urljoin(i)
            print "next page",link
			#inp = input()
            try:
         	yield scrapy.Request(url=link, callback=self.parse_school)
            except:
		print "could not go to indivitual school"
		inp = input();


    def parse_school(self, response):
        print "Scrapping school data: ",response
        try:
            data = {}
            data['Name of Institution'] = unicode('')
            data['Affiliation Number'] = unicode('')
            data['State'] = unicode('')
            data['District'] = unicode('')
            data['Postal Address'] = unicode('')
            data['Pin Code'] = unicode('')
            data['Phone Office 1'] = unicode('')
            data['Phone Office 2'] = unicode('')
            data['Phone Residence 1'] = unicode('')
            data['Phone Residence 2'] = unicode('')
            data['FAX No'] = unicode('')
            data['Email'] = unicode('')
            data['Website'] = unicode('')
            data['Year of Foundation'] = unicode('')
            data['Date of First Openning of School'] = unicode('')
            data['Name of Principal/ Head of Institution'] = unicode('')
            data['Sex'] = unicode('')
            data['Principal Education/Professional Qualifications'] = unicode('')
            data['Number of Experience Years'] = unicode('')
            data['Administrative'] = unicode('')
            data['Teaching'] = unicode('')
            data['Status of The School'] = unicode('')
            data['Type of affiliation'] = unicode('')
            data['Affiliation Period From'] = unicode('')
            data['Affiliation Period To'] = unicode('')
            data['Name of Trust/ Society/ Managing Committee'] = unicode('')
            data['locality'] = unicode('')
            data['extra'] = unicode('')

            point = 0
            page = BeautifulSoup(response.css('body').extract()[0],'html.parser').find_all('td')
            
        
            for val, i in enumerate(page):
                if i.b is not None and i.b.string is not None and i.b.string.strip() == unicode('Name of Institution'):
                    data['Name of Institution'] = page[val+1].string.strip()
            
            for val, i in enumerate(page):
                if i.b is not None and i.b.string is not None and i.b.string.strip() == 'Affiliation Number':
                    data['Affiliation Number'] = page[val+1].string.strip()

            for val, i in enumerate(page):
                if i.b is not None and i.b.string is not None and i.b.string.strip() == 'State':
                    data['State'] = page[val+1].string.strip()

            for val, i in enumerate(page):
                if i.b is not None and i.b.string is not None and i.b.string.strip() == 'District':
                    data['District'] = page[val+1].string.strip()

            for val, i in enumerate(page):
                if i.b is not None and i.b.string is not None and i.b.string.strip() == 'Phone No. with STD Code':
                    data['Phone No. with STD Code'] = page[val+1].string.strip()

            for val, i in enumerate(page):
                if i.b is not None and i.b.string is not None and i.b.string.strip() == 'Postal Address':
                    data['Postal Address'] = page[val+1].string.strip()
            
            for val, i in enumerate(page):
                if i.b is not None and i.b.string is not None and i.b.string.strip().lower().find('pin') is not -1:
                    data['Pin Code'] = page[val+1].string.strip()
            
            for val, i in enumerate(page):
                if i.b is not None and i.b.string is not None and i.b.string.strip().find('Office') is not -1:
                    #data['Phone Office 1'] = page[val+1].string.strip()
                    point = val
            try:        
                phoneNumber1 = data['Phone No. with STD Code'] + page[point+1].string.strip();
                data['Phone Office 1'] = ''.join(filter(str.isdigit, phoneNumber1));
            except:
                print "Phone Office 1 not found"
            try:
                data['Phone Office 2'] = data['Phone No. with STD Code'] + page[point+2].string.strip();
            except:
                print "Phone Office 2 not found"
            try:
                data['Phone Residence 1'] = data['Phone No. with STD Code'] + page[point+4].string.strip();
            except:
                print "Phone Residence 1 not found"
            try:
                data['Phone Residence 2'] = data['Phone No. with STD Code'] + page[point+5].string.strip();
            except:
                print "Phone Residence 2 not found"

            
            for val, i in enumerate(page):
                if i.b is not None and i.b.string is not None and i.b.string.strip().find('FAX No') is not -1:
                    data['FAX No'] = page[val+1].string.strip()

            for val, i in enumerate(page):
                if i.b is not None and i.b.string is not None and i.b.string.strip().find('Email') is not -1:
                    data['Email'] = page[val+1].string.strip()

            for val, i in enumerate(page):
                if i.b is not None and i.b.string is not None and i.b.string.strip().find('Website') is not -1:
                    data['Website'] = page[val+1].string.strip()

            for val, i in enumerate(page):
                if i.b is not None and i.b.string is not None and i.b.string.strip().find('Year of Foundation') is not -1:
                    data['Year of Foundation'] = page[val+1].string.strip()

            for val, i in enumerate(page):
                if i.b is not None and i.b.string is not None and i.b.string.strip().find('Openning') is not -1:
                    data['Date of First Openning of School'] = page[val+1].string.strip()

            for val, i in enumerate(page):
                if i.b is not None and i.b.string is not None and i.b.string.strip().find('Head') is not -1:
                    data['Name of Principal/ Head of Institution'] = page[val+1].string.strip()

            for val, i in enumerate(page):
                if i.b is not None and i.b.string is not None and i.b.string.strip() == 'Sex':
                    data['Sex'] = page[val+1].string.strip()

            for val, i in enumerate(page):
                if i.b is not None and i.b.string is not None and i.b.string.strip().find('Qualifications') is not -1:
                    data['Principal Education/Professional Qualification'] = page[val+1].string.strip()

            for val, i in enumerate(page):
                if i.b is not None and i.b.string is not None and i.b.string.strip().find('Experience') is not -1:
                    data['Number of Experience Years'] = page[val+1].string.strip()
            
            for val, i in enumerate(page):
                if i.b is not None and i.b.string is not None and i.b.string.strip().find('Administrative') is not -1:
                    data['Administrative'] = page[val+1].string.strip()

            for val, i in enumerate(page):
                if i.b is not None and i.b.string is not None and i.b.string.strip().find('Teaching') is not -1:
                    data['Teaching'] = page[val+1].string.strip()

            for val, i in enumerate(page):
                if i.b is not None and i.b.string is not None and i.b.string.strip().find('Status of The School') is not -1:
                    data['Status of The School'] = page[val+1].string.strip()

            for val, i in enumerate(page):
                if i.b is not None and i.b.string is not None and i.b.string.strip().find('Type of affiliation') is not -1:
                    data['Type of affiliation'] = page[val+1].string.strip()

            for val, i in enumerate(page):
                if i.b is not None and i.b.string is not None and i.b.string.strip().find('Affiliation Period From') is not -1:
                    data['Affiliation Period From'] = page[val+1].string.strip()

            for val, i in enumerate(page):
                if i.b is not None and i.b.string is not None and i.b.string.strip().find('Affiliation Period To') is not -1:
                    data['Affiliation Period To'] = page[val+1].string.strip()

            for val, i in enumerate(page):
                if i.b is not None and i.b.string is not None and i.b.string.strip().find('Trust') is not -1:
                    data['Name of Trust/ Society/ Managing Committee'] = page[val+1].string.strip()

            for val, i in enumerate(page):
                if i.b is not None and i.b.string is not None and i.b.string.strip().find('Police') is not -1:
                    data['locality'] = page[val+1].string.strip()


            print "Showing data: ",data
        except:
            print "Error: ",response




        check = Path("output/"+data['State'].lower()+".csv")
        if not check.is_file():
            with open("output/"+data['State'].lower()+".csv","wb") as myFile:
                fieldnames = ['Name of Institution','Affiliation Number', 'State', 'District', 'locality', 'Postal Address', 'Pin Code', 'Phone Office 1', 'Phone Office 2', 'Phone Residence 1', 'Phone Residence 2', 'FAX No', 'Email', 'Website', 'Year of Foundation', 'Date of First Openning of School', 'Name of Principal/ Head of Institution', 'Sex', 'Principal Education/Professional Qualifications', 'Number of Experience Years', 'Administrative', 'Teaching', 'Status of The School', 'Type of affiliation', 'Affiliation Period From', 'Affiliation Period To', 'Name of Trust/ Society/ Managing Committee', 'extra']

                writer = csv.DictWriter(myFile,fieldnames=fieldnames)
                writer.writeheader()

                                                
        with open("output/"+data['State'].lower()+".csv","a") as myFile:
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

                        

                 
