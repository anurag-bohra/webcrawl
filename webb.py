import time
import sys 
from subprocess import Popen, PIPE
import subprocess
import re
import socket
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
try:
    import urllib.request
except ImportError:
    import urllib2

def download_page(url,*arg):
    version = (3,0)
    cur_version = sys.version_info
    if cur_version >= version:    
        try:
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
            req = urllib.request.Request(url, headers = headers)
            resp = urllib.request.urlopen(req)
            page = str(resp.read())
            if len(arg)>0:
                file = open(arg[0], "w")
                file.write(page)
                file.close()
                return page
            else:
                return page
        except Exception as e:
            print(str(e))
    else:                        
        try:
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
            req = urllib2.Request(url, headers = headers)
            response = urllib2.urlopen(req)
            page = response.read()
            if len(arg)>0:
                file = open(arg[0], "w")
                file.write(page)
                file.close()
                return page
            else:
                return page    
        except:
            return"Page Not found"

def page_title(url):
    page = download_page(url)
    start_title = page.find("<title")
    end_start_title = page.find(">",start_title+1)
    stop_title = page.find("</title>", end_start_title + 1)
    title = page[end_start_title + 1 : stop_title]
    return (title)

def find_next_link(s):
    start_link = s.find("<a href")
    if start_link == -1:    
        end_quote = 0
        link = "no_links"
        return link, end_quote
    else:
        start_quote = s.find('"', start_link)
        end_quote = s.find('"',start_quote+1)
        link = str(s[start_quote+1:end_quote])
        return link, end_quote

def find_all_links(content):
    if content.startswith('http') or content.startswith('www'):
        url = content
        if "http" not in url:
            url = "http://" + url
        if "www" not in url:
            url = "www."[:7] + url[7:]
        content = download_page(url)
    page = content
    links = []
    while True:
        link, end_link = find_next_link(page)
        if link == "no_links":
            break
        else:
            links.append(link)      
            page = page[end_link:]
    return links 

def url_parse(url,seed_page):
    url = url.lower().replace(' ','%20') 
    s = urlparse(url)      
    t = urlparse(seed_page)    
    i = 0
    while i<=7:
        if url == "/":
            url = seed_page
            flag = 0  
        elif not s.scheme:
            url = "http://" + url
            flag = 0
        elif "#" in url:
            url = url[:url.find("#")]
        elif "?" in url:
            url = url[:url.find("?")]
        elif s.netloc == "":
            url = seed_page + s.path
            flag = 0
        elif "www" not in url:
            url = "www."[:7] + url[7:]
            flag = 0
            
        elif url[len(url)-1] == "/":
            url = url[:-1]
            flag = 0
        elif s.netloc != t.netloc:
            url = url
            flag = 1
            break        
        else:
            url = url
            flag = 0
            break
        
        i = i+1
        s = urlparse(url)
    return(url, flag)

def web_crawl(*arg):
    
    to_crawl = [arg[0]]      
    crawled=[]
    
    a = urlparse(arg[0])
    seed_page = a.scheme+"://"+a.netloc

    i=0;       
    while to_crawl: 
        urll = to_crawl.pop(0) 
        
        urll,flag = url_parse(urll,seed_page)
        flag2 = extension_scan(urll)

        if flag2 == 1:
            pass
            
        else:       
            if urll in crawled:    
                pass 
            else:   
                print("\n"+urll)
                if len(arg)>1:
                    delay = arg[1]
                    time.sleep(delay)

                to_crawl = to_crawl + find_all_links(download_page(urll))
                crawled.append(urll)

                n = 1
                j = 0
                #k = 0
                while j < (len(to_crawl)-n):
                    if to_crawl[j] in to_crawl[j+1:(len(to_crawl)-1)]:
                        to_crawl.pop(j)
                        n = n+1
                    else:
                        pass
                    j = j+1
            i=i+1

            print("Iteration No. = " + str(i))
            print("Pages to Crawl = " + str(len(to_crawl)))
            print("Pages Crawled = " + str(len(crawled)))
            
            if len(arg)>1:
                if arg[2]=="write_log":
                    file = open('log.txt', 'a')    
                    file.write("URL: " + urll + "\n")        
                    file.write("Iteration No. = " + str(i) + "\n")
                    file.write("Pages to Crawl = " + str(len(to_crawl)) + "\n")
                    file.write("Pages Crawled = " + str(len(crawled)) + "\n\n")
                    file.close()                         
    return ''



def remove_html_tags(page):
    pure_text = (re.sub(r'<.+?>', '', page))  
    return pure_text

def clean_page(page):
    while True:
        script_start = page.find("<script")
        script_end = page.find("</script>")
        if '<script' in page:
            script_section = page[script_start:script_end+9]
            page = page.replace(script_section,'')
        else:
            break
    pure_text = (re.sub(r'<.+?>', '', page))
    return pure_text

def get_next_heading(s,heading_type):
    start_link = s.find("<"+heading_type)
    if start_link == -1:    
        end_quote = 0
        link = "no_headings"
        return link, end_quote
    else:
        start_quote = s.find('>', start_link+1)
        end_quote = s.find('</'+heading_type+'>',start_quote+1)
        link = str(s[start_quote+1:end_quote])
        return link, end_quote

def get_all_headings_as_list(url,heading_type):
    links = []
    page = download_page(url)
    while True:
        link, end_link = get_next_heading(page,heading_type)
        link = link.replace('\n',' ')
        link = re.sub(r'<.+?>', '', link)
        if link == "no_headings":
            break
        else:
            links.append(link)     
            #time.sleep(0.1)
            page = page[end_link:]
    return links 

def get_all_headings(*arg):
    url = arg[0]
    lists = get_all_headings_as_list(url,arg[1])
    if len(arg)>2:
        if arg[2] == 'list':
            return lists 
    else:
        return lists

