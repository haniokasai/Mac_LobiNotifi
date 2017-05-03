# coding: UTF-8
import commands
import os
import pycurl
#import urllib
import json
from StringIO import StringIO
import ConfigParser

import time

print """
    __          __    _ _   __      __  _
   / /   ____  / /_  (_) | / /___  / /_(_)_______  _____
  / /   / __ \/ __ \/ /  |/ / __ \/ __/ / ___/ _ \/ ___/
 / /___/ /_/ / /_/ / / /|  / /_/ / /_/ / /__/  __/ /
/_____/\____/_.___/_/_/ |_/\____/\__/_/\___/\___/_/

   ____                           __                     __
  / __/__  ____  __ _  __ __  ___/ /__ ___ ________ ___ / /_
 / _// _ \/ __/ /  ' \/ // / / _  / -_) _ `/ __/ -_|_-</ __/
/_/  \___/_/   /_/_/_/\_, /  \_,_/\__/\_,_/_/  \__/___/\__/
                     /___/
                     Ubuntu
""";

#initialize cookie
path = (r'cookie.txt')
if (os.path.isfile(path)):
 os.remove(path)
f = open(path, 'w')
f.close()

class Pattern:
 csrf_token = '<input type="hidden" name="csrf_token" value="';
 authenticity_token = '<input name="authenticity_token" type="hidden" value="';
 redirect_after_login = '<input name="redirect_after_login" type="hidden" value="';
 oauth_token = '<input id="oauth_token" name="oauth_token" type="hidden" value="';
 twitter_redirect_to_lobi = '<a class="maintain-context" href="';

 def get_string(self,source, pattern, end_pattern):
  start = source.find(pattern) + len(pattern)
  end = source.index(end_pattern, start + 1)
  return source[start:end]
 get_string = classmethod(get_string)

class Http:
    def get(self,url):
        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, url)
        storage = StringIO()
        curl.setopt(pycurl.SSL_VERIFYPEER, False)
        #curl.setopt(pycurl.RETURNTRANSFER, 1)
        #curl.setopt(pycurl.CURLOPT_FOLLOWLOCATION, True)
        curl.setopt(pycurl.HTTPHEADER, [
                                        'Connection: keep-alive',
                                        'Accept: ', 'application/json, text/plain, */*',
                                        'User-Agent: ', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36',
                                        'Accept-Language: ', 'ja,en-US;q=0.8,en;q=0.6'
                                        ])
        curl.setopt(pycurl.COOKIEFILE, (r'cookie.txt'))
        curl.setopt(pycurl.COOKIEJAR, (r'cookie.txt'))
        curl.setopt(curl.WRITEFUNCTION, storage.write)
        success = False;
        while not(success):
         try:
          curl.perform()
          success = True
         except pycurl.error:
          commands.getoutput("notify-send 'Lobi : インターネット未接続'")
          time.sleep(30)
        curl.close()
        content = storage.getvalue()
        return content
    get = classmethod(get)

    def post(self,url, data):
        curl = pycurl.Curl()
        storage = StringIO()
        curl.setopt(pycurl.URL, url)
        curl.setopt(pycurl.SSL_VERIFYPEER, False)
        #curl.setopt(pycurl.RETURNTRANSFER, 1)
        #curl.setopt(pycurl.CURLOPT_FOLLOWLOCATION, True)
        curl.setopt(pycurl.HTTPHEADER, [
            'Connection: keep-alive',
            'Accept: ', 'application/json, text/plain, */*',
            'User-Agent: ',
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36',
            'Accept-Language: ', 'ja,en-US;q=0.8,en;q=0.6'
                                        ])
        curl.setopt(pycurl.COOKIEFILE, (r'cookie.txt'))
        curl.setopt(pycurl.COOKIEJAR, (r'cookie.txt'))
        curl.setopt(pycurl.POSTFIELDS,data)

        curl.setopt(curl.WRITEFUNCTION, storage.write)
        success = False;
        while not(success):
         try:
          curl.perform()
          success = True
         except pycurl.error:
          commands.getoutput("notify-send 'Lobi : インターネット未接続'")
          time.sleep(30)
        curl.close()
        content = storage.getvalue()
        return content
    post = classmethod(post)



class LobiAPI:
 NetworkAPI=""

 def Login(self,mail,password):
  source = Http.get('https://lobi.co/signin')
  #print source;
  csrf_token = Pattern.get_string(source,Pattern.csrf_token, '"')
  #print csrf_token;
  post_data = 'csrf_token=%s&email=%s&password=%s' % (csrf_token,mail,password)
  #print post_data
  posted = Http.post('https://lobi.co/signin', post_data)
  print posted;
  if posted.find('ログインに失敗しました') == -1:
   return True
  else:
   return False
 Login = classmethod(Login)

 def GetNotifications(self):
  return json.loads(Http.get('https://web.lobi.co/api/info/notifications?platform=any'))
 GetNotifications = classmethod(GetNotifications)

 def GetMe(self):
  return json.loads(Http.get('https://web.lobi.co/api/me?fields=premium'))
 GetMe = classmethod(GetMe)

 def Logintask(self):
  if os.path.exists("conf.ini"):
    print '設定ファイルが見つかりました'
    inifile = ConfigParser.SafeConfigParser()
    inifile.read('conf.ini')
    #print inifile.get('settings','email')
    #print inifile.get('settings','password')
    if LobiAPI.Login(inifile.get('settings','email'),inifile.get('settings','password')):
     if(LobiAPI.GetMe() is None):
         print "ログイン失敗.ユーザー名か、パスワードが違います。"
         exit();
     me = LobiAPI.GetMe()
     #print me
     print "ログイン成功"
     print "ユーザー名 : "+me["name"].encode('utf8')
    else:
     print "ログイン失敗.サーバーにアクセスできませんでした。"
     exit();
  else:
    print '設定ファイルがありませんでした、記述しておいてください、conf.iniです'
    inifile = ConfigParser.SafeConfigParser()
    inifile.add_section("settings")
    inifile.set('settings','email',"writehere")
    inifile.set('settings','password',"writehere")
    inifile.set('settings','interval',"10")
    inifile.set('settings','cachesize',"5")
    inifile.write(open("conf.ini", 'w'))
    exit()
 Logintask = classmethod(Logintask)
#////////////////////////////main line
LobiAPI.Logintask()
inifile = ConfigParser.SafeConfigParser()
inifile.read('conf.ini')
gn = inifile.getint("settings","interval")
cachesize = inifile.getint("settings","cachesize")
notifi = LobiAPI.GetNotifications()
ns = list()
ia = 0
print ns;
while ia < cachesize:
 ns.insert(ia,notifi["notifications"][ia]["id"])
 print "a"
 ia = ia +1
i = 0
while 1 == 1:
 newnotifi = LobiAPI.GetNotifications()
 ia = 0
 print ns;
 while ia <cachesize:
  if newnotifi["notifications"][ia]["id"] not in ns:
   uname = newnotifi["notifications"][ia]["user"]["name"]
   mes = newnotifi["notifications"][ia]["message"]
   commands.getoutput("notify-send 'Lobi : "+uname.encode("utf-8")+"' '"+mes.encode("utf-8")+"'")
  ia = ia + 1
 #///
 ns = None
 ns = list()
 ia = 0
 while ia < cachesize:
  ns.insert(ia, newnotifi["notifications"][ia]["id"])
  ia = ia + 1
 ##/////
 print "interval is working"
 print ns
 time.sleep(gn)