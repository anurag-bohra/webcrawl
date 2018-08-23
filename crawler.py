
import webb
import xlsxwriter as x
import socket
from urlparse import urlparse
import sys
import re
import os
from collections import Counter

reload(sys)
sys.setdefaultencoding('utf8')
os.system("mkdir webpages")

web_name=raw_input("Enter the domain name to scrawl.\n (write without http and www, example - bizcarta.io)-> ")
web_name="http://www."+web_name
file_name=raw_input("Enter the name of the excel file without extension -> ")
file_name=file_name+".xlsx"
print("\n")
workbook=x.Workbook(file_name)
worksheet = workbook.add_worksheet('sheet1')
bold=workbook.add_format({'bold':True})
chart=workbook.add_chart({'type':'pie'})
cell_format=workbook.add_format()
cell_format.set_text_wrap()

lists=webb.find_all_links(web_name)
all_links=[]
for link in lists:
	all_links+=webb.find_all_links(link)

print("starting...")
row=1
worksheet.set_column(1,1,60)
worksheet.set_column(0,0,20)
worksheet.set_column(2,2,10)
worksheet.set_column(3,3,80)
worksheet.set_column(4,4,40)
worksheet.set_column(5,5,40)
worksheet.set_column(6,6,40)

worksheet.write('A1' , 'DOMAIN' , bold)
worksheet.write('B1' , 'URL' , bold)
worksheet.write('C1' , 'IP' , bold)
worksheet.write('D1' , 'TITLE' , bold)
worksheet.write('E1' , 'HEADINGS' , bold)
worksheet.write('F1' , 'SUB HEADINGS' , bold)
worksheet.write('G1' , 'EMAILS PRESENT' , bold)
c=1
dlist=[]
for link in all_links:
	if((link != "#") and (link.startswith('http'))):
		print("crawling link-"+str(c))
		headings=webb.get_all_headings("\n"+link,"h1","list")
		subheadings=webb.get_all_headings("\n"+link,"h2","list")
		title=str(webb.page_title(link))
		o=urlparse((link))
		stri=o.netloc
		worksheet.write(row,0,stri)
		#print(link)
		worksheet.write_string(row,1, link, cell_format)
		ip=socket.gethostbyname(stri)
		worksheet.write(row,2, ip)
		if headings:
			worksheet.write(row,4, '\n'.join(headings), cell_format)
		if subheadings:		
			worksheet.write(row,5, '\n'.join(subheadings), cell_format)
		worksheet.write(row,3, title, cell_format)
		row+=1
		page=webb.download_page(link)
		c_page=webb.clean_page(page)
		if "@" in c_page:
			match=re.findall('[a-z]+@\S+', c_page)
			if match:
				worksheet.write(row,6,'\n'.join(match), cell_format)
		c+=1
		fname="webpages/"+stri+"-"+str(c)+".html"
		file1=open(fname,"w")
		file1.write(page)
		dlist.append(stri)

z=Counter(dlist)
worksheet.write(row+1,0, 'DOMAIN' , bold)
worksheet.write(row+1,1, 'COUNT' , bold)
start=row+1
for k,v in z.items():
	row+=1
	worksheet.write(row,0,k)
	worksheet.write(row,1, v)
end=row
chart.add_series({'name':'Number of links in each domain','categories':['sheet1',start,0,end,0],'values':['sheet1',start,1,end,1]})
chart.set_title({'name':'Links in each domain'})
chart.set_style(10)
worksheet.insert_chart(end+3,0,chart)	
workbook.close()
print("\n Please check the current directory for the excel sheet and webpages folder having crawled information and webpages")
