#python 3.6
import urllib.request
import re

#search word and encoded to adapte url
word = urllib.request.quote("ed sheeran")
print(word)
#page number. one page inclueds 60 pictures
pn = 0
#request
request = urllib.request.Request("https://image.baidu.com/search/flip?"
                                 "tn=baiduimage&ie=utf-8"
                                 "&word=ed%20sheeran"
                                 "&pn=" + str(pn))
#reponse
response = urllib.request.urlopen(request)
#objURL is original picture's url
url_pattern = re.compile(r'"objURL":"http.*?\.jpg"')
#to get url from objURL
pattern = re.compile(r'http:.*?\.jpg')
#get content from response
content = response.read()
#print( content )
content = content.decode('utf-8')
#print( content )
print("-------------------------------------------------------------------------------------")
#make sure you hava this directory in your computer
default_download_path = "E://python_download/"
#download number start
pic_count = 400
#avoid to download same picture
pic_urls = []
#for each objRUL in content
for p in re.findall(url_pattern, content):
    if(pic_urls.count(p) == 0):
        pic_urls.append(p)
        print(p)
        pp = re.findall(pattern, p)
        print(pp)
        #for each picture url in objURL
        for ppp in pp:
            try:
                pppp = urllib.request.urlopen(ppp,timeout=10).read()
                f = open(default_download_path + str(pic_count) + ".jpg","wb")
                f.write(pppp)
                f.close()
                pic_count+=1
            #goto the next one when exception occur
            except urllib.request.URLError as e:
                print("URLError")
            except UnicodeEncodeError as e:
                print("UnicodeEncodeError")
            except Exception as e:
                print("Exception")
#print( response.read() )