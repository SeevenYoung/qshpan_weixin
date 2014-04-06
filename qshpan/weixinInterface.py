# -*- coding: utf-8 -*-
import hashlib
import web
import lxml
import time
import os
import urllib2,json
from lxml import etree
import random
import pylibmc
from bs4 import BeautifulSoup
import config
import discuz

    
def xiaohuangji(ask):
    ask = ask.encode('UTF-8')
    enask = urllib2.quote(ask)
    send_headers = {
        'Cookie':'Filtering=0.0; Filtering=0.0; isFirst=1; isFirst=1; simsimi_uid=50840753; simsimi_uid=50840753; teach_btn_url=talk; teach_btn_url=talk; sid=s%3AzwUdofEDCGbrhxyE0sxhKEkF.1wDJhD%2BASBfDiZdvI%2F16VvgTJO7xJb3ZZYT8yLIHVxw; selected_nc=zh; selected_nc=zh; menuType=web; menuType=web; __utma=119922954.2139724797.1396516513.1396516513.1396703679.3; __utmc=119922954; __utmz=119922954.1396516513.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'
     }
    baseurl = r'http://www.simsimi.com/func/reqN?lc=zh&ft=0.0&req='
    url = baseurl+enask
    req = urllib2.Request(url,headers=send_headers)
    resp = urllib2.urlopen(req)
    reson = json.loads(resp.read())
    return reson

def hepanHotNews():
    my_account = discuz.Discuz()
    url = r'http://bbs.stuhome.net/'
    my_account.login(config.username, config.password)
    
    html = my_account._get_response(url);
    test = html.read().decode('utf-8')  
#    html_doc = open("hepan.html","r").read()
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
    return reply_text     

class WeixinInterface:

    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)
    

    def GET(self):
        #获取输入参数
        data = web.input()
        signature=data.signature
        timestamp=data.timestamp
        nonce=data.nonce
        echostr=data.echostr
        #自己的token
        token="weixin" #这里改写你在微信公众平台里输入的token
        #字典序排序
        list=[token,timestamp,nonce]
        list.sort()
        sha1=hashlib.sha1()
        map(sha1.update,list)
        hashcode=sha1.hexdigest()
        #sha1加密算法        

        #如果是来自微信的请求，则回复echostr
        if hashcode == signature:
            return echostr
    def test(self):
        print "hello,wolrd"
    def POST(self):        
        str_xml = web.data() #获得post来的数据
        xml = etree.fromstring(str_xml)#进行XML解析
        content=xml.find("Content").text#获得用户所输入的内容
        msgType=xml.find("MsgType").text
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text
        
        mc = pylibmc.Client() #初始化一个memcache实例用来保存用户的操作
        
        if msgType == 'text':
            content=xml.find("Content").text
            if content == 'help':
                replayText = '''1.输入xhj（小黄鸡），来尽情蹂躏她/他\n2.输入"qshp"（请水河畔)，查看当前河畔的热门帖子\n3.输入m随机来首音乐听（建议在wifi下听）\n'''
                return self.render.reply_text(fromUser,toUser,int(time.time()),replayText)
            elif content.lower() == 'bye':
                mc.delete(fromUser+'_xhj')
                return self.render.reply_text(fromUser,toUser,int(time.time()),u'您已经跳出了和小黄鸡的交谈中，输入help来显示操作指令')
                
            elif content.lower() == 'xhj':
                mc.set(fromUser+'_xhj','xhj')
                return self.render.reply_text(fromUser,toUser,int(time.time()),u'您已经进入与小黄鸡的交谈中，请尽情的蹂躏它吧！输入bye跳出与小黄鸡的交谈')
            elif content == 'm':
                musicList = [
                             [u'http://bcs.duapp.com/yangyanxingblog3/music/destiny.mp3','Destiny',u'献给我的宝贝晶晶'],
                             [u'http://bcs.duapp.com/yangyanxingblog3/music/5days.mp3','5 Days',u'献给我的宝贝晶晶'],
                             [u'http://bcs.duapp.com/yangyanxingblog3/music/Far%20Away%20%28Album%20Version%29.mp3','Far Away (Album Version)',u'献给我的宝贝晶晶'],
                             [u'http://bcs.duapp.com/yangyanxingblog3/music/%E5%B0%91%E5%B9%B4%E6%B8%B8.mp3',u'少年游',u'献给我的宝贝晶晶'],
                             [u'http://bcs.duapp.com/yangyanxingblog3/music/%E8%8F%8A.mp3',u'菊--关喆',u'献给我的宝贝晶晶'],
                             [u'http://bcs.duapp.com/yangyanxingblog3/music/%E7%A6%BB%E4%B8%8D%E5%BC%80%E4%BD%A0.mp3',u'离不开你',u'献给我的宝贝晶晶'],
                             [u'http://bcs.duapp.com/yangyanxingblog3/music/%E9%99%8C%E7%94%9F%E4%BA%BA.mp3',u'陌生人',u'献给我的宝贝晶晶'],
                             [u'http://bcs.duapp.com/yangyanxingblog3/music/%E8%8A%B1%E5%AE%B9%E7%98%A6.mp3',u'花容瘦',u'献给我的宝贝晶晶'],
                             [u'http://bcs.duapp.com/yangyanxingblog3/music/%E4%B9%98%E5%AE%A2.mp3',u'乘客',u'献给我的宝贝晶晶'],
                             [u'http://bcs.duapp.com/yangyanxingblog3/music/If%20My%20Heart%20Was%20A%20House.mp3',u'If My Heart Was A House',u'献给我的宝贝晶晶'],
                             [u'http://bcs.duapp.com/yangyanxingblog3/music/Hello%20Seattle%EF%BC%88Remix%E7%89%88%EF%BC%89.mp3',u'Hello Seattle（Remix版',u'献给我的宝贝晶晶'],
                             [u'http://bcs.duapp.com/yangyanxingblog3/music/Everybody%20Hurts.mp3',u'Everybody Hurts',u'献给我的宝贝晶晶']                            
                                ]
                music = random.choice(musicList)
                musicurl = music[0]
                musictitle = music[1]
                musicdes =music[2]
                return self.render.reply_music(fromUser,toUser,int(time.time()),musictitle,musicdes,musicurl)
            elif content == 'qshp':
            	reply_text = hepanHotNews()
            	return self.render.reply_text(fromUser,toUser,int(time.time()),reply_text)
                
            else:
	        		#读取memcache中的缓存数据	        
                mcxhj = mc.get(fromUser+'_xhj')
                if mcxhj =='xhj':
                    res = xiaohuangji(content)
                    print "hello"
                    reply_text=res['sentence_resp']
                    if u'微信' in reply_text:
                        reply_text = u"小黄鸡脑袋出问题了，请换个问题吧~" #这里小黄鸡会有广告，我索性就全给屏蔽了
                    return self.render.reply_text(fromUser,toUser,int(time.time()),reply_text)
                else:
                    #replyString = u'''这里是单程车票，更多玩法请输入"help"，您刚才说的是：'''+content
                    #replyString = u'''<a href="http://bbs.qshpan.com/forum.php?mod=viewthread&tid=1421326">http://bbs.stuhome.net/forum.php?mod=viewthread&tid=1421326 九寨归来，同去的有小黑猫，za_may12 --author:超哥</a>'''
                    replyString = u'''http://bbs.stuhome.net/forum.php?mod=viewthread&tid=1421365'''
                    return self.render.reply_text(fromUser,toUser,int(time.time()),replyString)

	
            
