# -*- coding: utf-8 -*-

import config
import discuz
import time
from bs4 import BeautifulSoup
import re
#import BeautifulSoup

if __name__ == '__main__':
    my_account = discuz.Discuz()
    url = r'http://bbs.stuhome.net/'
    my_account.login(config.username, config.password)
    
    html = my_account._get_response(url);
    test = html.read().decode('utf-8')
    
#        html_doc = open("hepan.html","r").read()
    soup = BeautifulSoup(test)    
    text = soup.findAll("div", {"class":"module cl xl xl1"})
    con =  text[2].findAll("li")
    
    llen = len(con)
    reply_text =''''''
    i = 0
    while i < llen:
        result = con[i].find_all("a")
        result1 = result[0]
        result2 = result[1]
        # result = url[1]
    #     print result2["href"]
    #     print result2["title"]
    #     print result1.string
        i= i+1
        reply_text = reply_text + '''%d:<a href = "%s"> title:%s --author:%s</a>\n''' %(i,result2['href'],result2['title'],result1.string)
        #return reply_text 
    print reply_text   

         
    
    



