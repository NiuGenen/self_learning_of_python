from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

default_source_dir = "E:\DevelopmentToolsRelease"
default_traces_dir = default_source_dir + "\Traces"
default_result_dir = default_source_dir + r"\result"

result_s_2_read = default_result_dir + r"\\" + "s_2_read.csv"
result_s_2_write = default_result_dir + r"\\" + "s_2_write.csv"
result_s_2_io = default_result_dir + r"\\" + "s_2_io.csv"
result_byte_2_io = default_result_dir + r"\\" + "byte_2_io.csv"

#spread of io size
'''
b_2_io = open(result_byte_2_io,"r")
b = []
io = []
total_io = 0
kb_x = []
kb_io = []
kb_to_io = dict()
for line in b_2_io:
    words = line.strip().split(",")
    byte = int(words.__getitem__(0))
    c = int(words.__getitem__(1))
    b.append(byte)
    io.append(c)
    total_io += c

    kb = int(byte/1024)
    if kb in kb_to_io:
        kb_to_io[kb] += c
    else:
        kb_to_io.setdefault(kb, c)
print("Total io = " + str(total_io) )
print(kb_to_io)
for key in kb_to_io:
    kb_x.append(key)
    kb_io.append(kb_to_io[key])

io_spread=[0,0,0,0,0,0,
           0,0,0,0,0,0,
           0,0,0,0,0,0]
count = 0
while count < b.__len__():
    byte = b[count]
    num = io[count]
    index = int(byte/1024/4)#4KB each
    if index > 17:
        index = 17
    io_spread[index] += num
    count += 1
print(io_spread)
'''

#number of reads and writes per second
'''
s_2_r = open(result_s_2_read, "r")
s_2_w = open(result_s_2_write, "r")
s_r = []
r = []
s_w = []
w = []
total_r = 0
total_w = 0
for line in s_2_r:
    #print(line)
    words = line.strip().split(",")
    ts = int(words.__getitem__(0)) - 1204736457 + 1
    c = int(words.__getitem__(1))
    s_r.append(ts)
    r.append(c)
    total_r += c
s_2_r.close()
print("Total_r = " + str(total_r) )
for line in s_2_w:
    #print(line)
    words = line.strip().split(",")
    ts = int(words.__getitem__(0)) - 1204736457 + 1
    c = int(words.__getitem__(1))
    s_w.append(ts)
    w.append(c)
    total_w += c
s_2_w.close()
print("Total_w = " + str(total_w) )

fig_s_2_rw = plt.figure()
ax = fig_s_2_rw.add_subplot(1,1,1)
ax.set_ylabel('Number of requests')
ax.set_xlabel('DevelopmentToolsRelease')
ax.set_title('Number of reads and writes per second')
#ax.set_xticks([0,10000,20000,30000,40000,50000,60000,64800])
plt.xlim(0,64800)
#ax.set_yticks([0,500,1000,1500])
plt.ylim(0,1500)
ax.bar(s_r, r, alpha = .5, color = 'g',label="Reads")
ax.bar(s_w, w, alpha = .5, color = 'r',label="Writes")
plt.legend(loc='upper right')
plt.show()
'''

#number of requests
'''
s_2_io = open(result_s_2_io, "r")
s = []
io = []
total_io = 0
for line in s_2_io:
    #print(line)
    words = line.strip().split(",")
    ts = int(words.__getitem__(0)) - 1204736457 + 1
    c = int(words.__getitem__(1))
    s.append(ts)
    io.append(c)
    total_io += c
s_2_io.close()
'''
#per second
"""
fig_s_2_io = plt.figure()
ax = fig_s_2_io.add_subplot(1,1,1)
ax.set_ylabel('Total Requests (I/Os)')
ax.set_xlabel('DevelopmentToolsRelease')
ax.set_title('Number of requests per second')
plt.xlim(0,64800)
plt.ylim(0,3000)
ax.bar(s, io, alpha = .5, color = 'k')
plt.show()
"""
#per hour
'''
h_2_io = dict()
index = 0
while index < s.__len__():
    ss = s[index]
    h = int(ss/3600)
    if h in h_2_io:
        h_2_io[h] += io[index]
    else:
        h_2_io.setdefault(h, io[index])
    index+=1
h = []
io = []
for key in h_2_io:
    h.append(key)
    io.append(h_2_io[key])
fig_h_2_io = plt.figure()
ax = fig_h_2_io.add_subplot(1,1,1)
ax.set_ylabel('Total Requests (I/Os)')
ax.set_xlabel('DevelopmentToolsRelease')
ax.set_title('Number of requests per hour')
ax.bar(h, io, alpha = .5, color = 'k')
plt.show()
'''

# 3D disknum to time in second to io
# 17 disk for all from 0 to 16
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel("time per second")
ax.set_ylabel('number of requests')
ax.set_zlabel('disk number')
for disknum ,cs in zip(
        [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,16],
        ['r', 'g', 'b', 'y','r', 'g', 'b', 'y','r', 'g', 'b', 'y','r', 'g', 'b', 'y']):
    result_s_2_io_under_disknum = default_result_dir + r"\\" + "disk_" + str(disknum) + "_s_2_io.csv"
    print( result_s_2_io_under_disknum )
    f = open(result_s_2_io_under_disknum, "r")
    xs = []
    ys = []
    for line in f:
        words = line.strip().split(",")
        time_s = int( words.__getitem__(0) ) - 1204736457 + 1
        io = int( words.__getitem__(1) )
        xs.append( time_s )
        ys.append( io )
    f.close()
    print("Drawing it ......")
    ax.bar(xs, ys, zs=disknum, zdir='y', color=cs, alpha=0.8)
plt.show()
