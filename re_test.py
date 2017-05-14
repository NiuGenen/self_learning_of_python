#python 3.6
import re

content = "qdywhbadsn\r\ndasdas\r\nqqwasdwgw.asdad         asd.asdssa\r\nafewfasdbeberbe.asd\r\nvsdvhjsdasd"
print(content)
print("----------not greedy---------")
#not greedy if using '*?' to match 0 or more
pattern = re.compile(r'asd.*?\.asd')
for c in re.findall(pattern, content):
    print(c)
print("------------greedy-----------")
#greedy if using '*' to match 0 or more
pattern = re.compile(r'asd.*\.asd')
for c in re.findall(pattern, content):
    print(c)