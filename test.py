#python 3.6
import urllib.parse
import urllib.request
import time

#some test for my own project

def http_post(url,para):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    #headers = {'User-Agent': user_agent}
    request = urllib.request.Request(url,para)
    #request.headers = headers
    print( request.get_full_url() )
    print( request.data )
    print( request.get_header('User-Agent') )
    response = urllib.request.urlopen(request)
    print( response.read() )

print("test_request_UserPath")
url_path = "http://localhost:60000/servlet_server_for_android/UserPathServlet"
post_para = dict(username='asd',userid=1,start=1494432000000,end=1494518400000)
#print(post_para['username'])
post_data = urllib.parse.urlencode(post_para).encode(encoding='UTF8')
#print(post_data)
http_post(url_path,post_data)

print("test_request_PointTrack")
url_point = "http://localhost:60000/servlet_server_for_android/PointTrackServlet"
print(int(time.time()*1000))
post_para = dict(test=True,userid=404,point="{'latitude':26,'longitude':118,'location':'asd'}",timestramp=int(time.time()*1000))
post_data = urllib.parse.urlencode(post_para).encode(encoding='UTF8')
print(post_data)
http_post(url_point,post_data)
