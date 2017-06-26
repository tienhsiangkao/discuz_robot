#! /usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request, urllib.error, urllib.parse
import http.cookiejar
import re

class DiscuzRobot:

### Initialize the url, username, password and proxy ###
    def __init__(self, forumUrl, userName, password, proxy = None):

        self.forumUrl = '' # bbs url, http://bbs.example.com
        self.userName = ''.encode("utf-8") # your username
        self.password = '' # your password
        self.formhash = '' # for formhash 
        self.isLogon = False
        self.isSign = False
        self.jar = http.cookiejar.CookieJar()

        if not proxy:
            openner = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.jar))
        else:
            openner = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.jar),
             urllib.request.ProxyHandler({'http' : proxy}))
        urllib.request.install_opener(openner)

### Login module ###
    def login(self):
        url = self.forumUrl + ""; # use your 
        postData = urllib.parse.urlencode({'username': self.userName, 'password': self.password, 'answer': '', 'cookietime': '2592000', 'handlekey': 'ls', 'questionid': '0', 'quickforward': 'yes',  'fastloginfield': 'username'}).encode("utf-8")
        req = urllib.request.Request(url,postData)
        content = urllib.request.urlopen(req).read()
        if self.userName in content:
            self.isLogon = True
            print('logon success!')
            self.initFormhash()
        else:
            print('logon faild!')

### Grab formhash ###
    def initFormhash(self):
        def saveHtml(file_name,file_content):
            with open (file_name.replace('/','_')+".html","wb") as f:
                f.write( file_content )
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.jar))
        content = opener.open(self.forumUrl).read().decode('gbk')
        rows = re.findall("formhash\" value=\"(.*)\"", content)
        if len(rows)!=0:
            self.formhash = rows[0]
            print('formhash is: ' + self.formhash)
        else:
            print('none formhash!')

### Signin ###
    def sign(self,msg = 'WooHoo~!'):
        
	opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.jar))

        if self.isSign:
            return
        if self.isLogon:
            url = self.forumUrl + '/plugin.php?id=dsu_amupper&ppersubmit=true&formhash=' # the formhash 
            postData = urllib.parse.urlencode({'fastreply': '1', 'formhash': self.formhash, 'qdmode': '1' }).encode("utf-8")
            req = urllib.request.Request(url,postData)
            temp = opener.open(url + self.formhash)
            content = urllib.request.urlopen(req).read().decode('gbk')
            #print content
            if '签到完毕' in content:
                self.isSign = True
                print('sign success!')
                return
        print('sign faild!')

if __name__ == '__main__':
    robot = DiscuzRobot('','','')
    robot.login()
    robot.sign()
