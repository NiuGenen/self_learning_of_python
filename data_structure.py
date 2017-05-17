# list in list
print("------------------list in list-----------------")
objs = []

obj1 = [1,2,3,4,5]
obj2 = [11,22,33,44,55]
obj3 = [111,222,333,444,555]

objs.append( obj1 )
objs.append( obj2 )
objs.append( obj3 )

for obj in objs:
    print(obj)

#list in dict
print("------------------list in dict-----------------")
objs = dict()

key1 = 1
key2 = 2
key3 = 3

value1 = dict()
value2 = dict()
value3 = dict()


for i in [1,2,3,4,5]:
    value1.update({i:i*10})
    value2.update({i:i*100})
    value3.update({i:i*100})
objs.update({1:value1})
objs.update({2:value2})
objs.update({3:value3})

print(objs)

value = objs[1]
value[2] += 100000000000

print(objs)