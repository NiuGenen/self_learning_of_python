import urllib.request

content = urllib.request.urlopen("https://manhua.163.com/reader/4460198728620123378/4639712296520113489")
content = str(content)

print(content)