import urllib.request
import re
import string

def download(url, file):
    print( "Download: " + url)
    print( "OutputFile: " + file)
    content = urllib.request.urlopen( url , timeout=10 ).read()
    f = open(file , "wb")
    f.write(content)
    f.close()

pattern_next_vlolume = re.compile(r'nextVolume="/manhua/[0-9]{4,5}/[0-9]{4,12}\.html"')
pattern_pic_nr = re.compile(r'picCount\ =\ [0-9]?[0-9]{2}')
pattern_pic_name_png = re.compile(r'picAy\[[0-9]?[0-9]?[0-9]?\]="(?:(?!picAy).)*?\.png"')
pattern_pic_name_jpg = re.compile(r'picAy\[[0-9]?[0-9]?[0-9]?\]="(?:(?!picAy).)*?\.jpg"')

def get_next_vlolume( base_str ):
    pattern_next_vlolume_head = re.compile(r'nextVolume="')
    head_s = re.findall(pattern_next_vlolume_head, base_str )
    head_len = head_s.__getitem__(0).__len__()
    str_len = base_str.__len__()
    next_vlolume = base_str[ head_len:(str_len-1)]
    return next_vlolume

def get_total_nr( base_str ):
    pattern_pic_nr_head = re.compile(r'picCount\ =\ ')
    head_s = re.findall(pattern_pic_nr_head, base_str )
    head_len = head_s.__getitem__(0).__len__()
    str_len = base_str.__len__()
    pic_count = base_str[ head_len:str_len]
    return pic_count

def get_pic_name(base_ary):
    pattern_base_head = re.compile(r'picAy\[[0-9]?[0-9]?\]="')
    head_length = 0
    head_s = re.findall(pattern_base_head, base_ary )
    head_length = head_s.__getitem__(0).__len__()
    str_length  = base_ary.__len__()
    pic_name = base_ary[head_length:(str_length - 1)]
    return pic_name

tail_str = "#p=1"
url = r"http://www.dmzx.com"
#file_path = "E:\\PERSONAL\\python_download\\ZCHZT\\"
#start_volume = r"/manhua/6413/641312774.html" # 1
#start_volume = r"/manhua/6413/641313904.html" # 9
#start_volume = r"/manhua/6413/25387.html" # 45
#start_volume = r"/manhua/6413/2000003929.html" # 46
#start_volume = r"/manhua/6413/2000014374.html" #51
#start_volume = r"/manhua/6413/2000074365.html" # 72
#start_volume = r"/manhua/6413/2000076848.html" # 73
#start_volume = r"/manhua/6413/2000078969.html" # 74
#start_volume = r"/manhua/6413/2000081188.html" # 75
#start_volume = r"/manhua/6413/2000083872.html" # 76

file_path = "E:\\PERSONAL\\python_download\\ZCHZTL\\"
#start_volume = r"/manhua/13096/1309624648.html" # 1
#start_volume = r"/manhua/13096/1309624649.html" # 2
#start_volume = r"/manhua/13096/25236.html" # 3
start_volume = r"/manhua/13096/2000003881.html" # 4

volume_num = 4
file_name_base = str(volume_num) + "\\" + str(volume_num) + "_"

picHosts = "http://jpgcdn.dmzx.com/img/"

def download_manhua(base_url, volume):
    global volume_num
    global file_name_base

    manhua_url = base_url + volume + tail_str
    print( manhua_url )
    print( "downloading......" )
    manhua_content = urllib.request.urlopen( manhua_url , timeout=10).read()
    manhua_content = str(manhua_content)
    #print( manhua_content )

    pic_nr_base_s = re.findall( pattern_pic_nr, manhua_content )
    if( pic_nr_base_s.__len__() > 0):
        pic_nr_base = pic_nr_base_s.__getitem__(0)
        pic_nr = get_total_nr(pic_nr_base)
        print( "PicCount = " + pic_nr )

    print(" ----------- JPG ----------- ")
    pic_name_jpg_base_s = re.findall( pattern_pic_name_jpg, manhua_content )
    jpg_nr = pic_name_jpg_base_s.__len__()
    count_jpg = 0
    while( count_jpg < jpg_nr ):
        pic_name_jpg_base = pic_name_jpg_base_s.__getitem__( count_jpg )
        pic_name = get_pic_name( pic_name_jpg_base )
        try:
            file_name = file_path + file_name_base + str( count_jpg ) + ".jpg"
            download( picHosts + pic_name, file_name )
            print( "PicName = " + pic_name )
        except urllib.request.URLError as e:
            print("URLError")
        except urllib.error.HTTPError as e:
            print("HTTPError")
        except UnicodeEncodeError as e:
            print("UnicodeEncodeError")
        except Exception as e:
            print("Exception")
        count_jpg += 1

    print(" ----------- PNG ----------- ")
    pic_name_png_base_s = re.findall( pattern_pic_name_png, manhua_content )
    png_nr = pic_name_png_base_s.__len__()
    count_png = 0
    while( count_png < png_nr ):
        pic_name_png_base = pic_name_png_base_s.__getitem__( count_png )
        pic_name = get_pic_name( pic_name_png_base )
        print( "PicName = " + pic_name )
        file_name = file_path + file_name_base + str( count_png + count_jpg ) + ".png"
        download( picHosts + pic_name, file_name )
        count_png += 1

    next_vlolume_base_s = re.findall( pattern_next_vlolume , manhua_content )
    if( next_vlolume_base_s.__len__() > 0):
        next_vlolume_base = next_vlolume_base_s.__getitem__(0)
        next_vlolume = get_next_vlolume( next_vlolume_base )
        print( "nextVolume = " + next_vlolume )
        volume_num += 1
        file_name_base = str(volume_num) + "\\" + str(volume_num) + "_"
        return next_vlolume
    else:
        return ""

next_volume = download_manhua( url, start_volume )
while( next_volume.__len__() > 0 ):
    next_volume = download_manhua( url, next_volume )