from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

trace_name = "DevelopmentToolsRelease"
trace_absolute_dir = "E:\\"

default_source_dir = trace_absolute_dir + trace_name
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
# 16 disk for all from 0 to 16 ( no 15 )
'''
fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
ax = Axes3D(fig)
ax.set_xlabel("time per second")
ax.set_ylabel('disk number')
ax.set_zlabel('number of requests')
for disknum ,cs in zip(
        [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,16],
        ['r', 'g', 'b', 'y','r', 'g', 'b', 'y','r', 'g', 'b', 'y','r', 'g', 'b', 'y']):
    result_s_2_io_under_disknum = default_result_dir + r"\\" + "disk_" + str(disknum) + "_s_2_io.csv"
    print( result_s_2_io_under_disknum )
    f = open(result_s_2_io_under_disknum, "r")
    xs = []
    ys = []
    zs = []
    dz = []
    for line in f:
        words = line.strip().split(",")
        time_s = int( words.__getitem__(0) ) - 1204736457 + 1
        io = int( words.__getitem__(1) )
        xs.append( time_s )
        ys.append(disknum)
        zs.append( 0 )
        dz.append( io )
    f.close()
    print("Drawing it ......")
    ax.bar3d(x=xs, y=ys, z=zs, dx=.5, dy=.5, dz=dz, alpha=.5, color=cs)
    #ax.bar3d(xs, ys, z=disknum, dx=0.5, dy=0.5,dz=disknum, color=cs, alpha=0.8)
plt.show()
'''

# interarrival timestramp in ns to io
'''
result_inter_ns_2_io = default_result_dir + "\\" + "inter_ns_2_io.csv"
print( result_inter_ns_2_io )
f = open(result_inter_ns_2_io, "r")
ns = []
io_ns = []
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
s_2_io = dict()
total_io = 0
for line in f:
    words = line.strip().split(",")
    _ns = int( words.__getitem__(0) )
    _io = int( words.__getitem__(1) )
    total_io += _io
    s = _ns/60/60
    if s in s_2_io:
        s_2_io[s] += _io
    else:
        s_2_io.setdefault(s, _io)
    #ns.append( _ns )
    #io_ns.append( _io )
#print("Drawing ns_2_io ......")
#ax.scatter(ns, io, color="b", alpha=.5)
s = []
io_s = []
for _s in s_2_io:
    if _s < 4:
        s.append( _s )
        io_s.append( s_2_io[_s] )
ax.scatter(s, io_s, color="b", alpha=.5)
ax.set_xlabel("Interarrival Time (seconds)")
ax.set_ylabel("Number of Request")
ax.set_title("Interarrival Time")

percent = []
sum_io = 0.0
for _s in sorted(s):
    sum_io += s_2_io[_s]
    percent.append( sum_io/total_io * 100 )
ax2 = ax.twinx()
ax2.plot(sorted(s), percent, color="r", alpha=.5)
fmt='%.1f%%'    # y formate as percent
yticks = mtick.FormatStrFormatter(fmt)
ax2.yaxis.set_major_formatter(yticks)
ax2.set_ylabel("Percent")

f.close()
plt.show()
'''

# inter offset of sector to io(read/write)
'''
result_inter_offset_2_io = default_result_dir + "\\" + "inter_offset_sector_2_io.csv"
#result_inter_offset_2_read = default_result_dir + "\\" + "inter_offset_sector_2_read.csv"
#result_inter_offset_2_write = default_result_dir + "\\" + "inter_offset_sector_2_write.csv"
print( result_inter_offset_2_io )
#print( result_inter_offset_2_read )
#print( result_inter_offset_2_write )
sector = []
io = []
f_io = open(result_inter_offset_2_io, "r")
_sector_2_io = dict()
_sector_2_read = dict()
_sector_2_write = dict()
#_512_sector_2_io = dict()
total_read = 0
total_write = 0
for line in f_io:
    words = line.strip().split(",")
    _sector = int( words.__getitem__(0) )
    _io = int( words.__getitem__(1) )
    total_io += _io
    #if _io > 100:
    #    print(str(_sector) + " = " + str(_io) )
#    _512_sector = int( _sector / 512 )
    if _sector in _sector_2_io:
        _sector_2_io[ _sector ] += _io
    else:
        _sector_2_io.setdefault(_sector, _io)
#    if _512_sector in _512_sector_2_io:
#        _512_sector_2_io[ _512_sector ] += _io
#    else:
#        _512_sector_2_io.setdefault( _512_sector, _io )
    sector.append( _sector )
    io.append( _io )
f_io.close()
#for line in open(result_inter_offset_2_read):
#    words = line.strip().split(",")
#    _sector = int( words.__getitem__(0) )
#    _read = int( words.__getitem__(1) )
#    if _read > 1000:
#        print( str(_sector) + " = " + str(_read) )
#    total_read += _read
#    if _sector in _sector_2_read:
#        _sector_2_read[ _sector ] += _read
#    else:
#        _sector_2_read.setdefault( _sector, _read )
#print("Total read = " + str(total_read) )
#for line in open(result_inter_offset_2_write):
#    words = line.strip().split(",")
#    _sector = int(words.__getitem__(0))
#    _write = int(words.__getitem__(1))
#    if _write > 1000:
#        print( str(_sector) + " - " + str(_write) )
#    total_write += _write
#    if _sector in _sector_2_write:
#        _sector_2_write[_sector] += _write
#    else:
#        _sector_2_write.setdefault(_sector, _write)
#print("Total write = " + str(total_write) )

x_io = []
y_io = []
for _s in _sector_2_io:
    if abs(_s) <= 80:
        x_io.append( _s )
        y_io.append( _sector_2_io[_s] / total_io * 100 ) # calculate percent of
#x_read = []
#y_read = []
#for _s in _sector_2_read:
#    if abs(_s) <= 80:
#        x_read.append( _s )
#        y_read.append( _sector_2_read[_s] / (total_read + total_write) * 100 ) # calculate percent of

#x_write = []
#y_write = []
#for _s in _sector_2_write:
#    if abs(_s) <= 80:
#        x_write.append( _s )
#        y_write.append( _sector_2_write[_s] / (total_read + total_write) * 100 ) # calculate percent of

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.scatter( x_io, y_io, color="b", alpha=.5 )
#ax.scatter( x_read, y_read, color="b", alpha=.5 ,label="Reads")
#ax.scatter( x_write, y_write, color="r", alpha=.5, label="Writes" )
plt.legend(loc='upper right')
ax.set_xlabel("Offset Between Requests ")
ax.set_ylabel("% of Total Requests")
ax.set_title("Tight Spatial Locality")
plt.xlim(-80,80)
plt.ylim(0,6)
ax.plot([-80,80],[1,1],color="k",alpha=.5)
ax.plot([-80,80],[2,2],color="k",alpha=.5)
ax.plot([-80,80],[3,3],color="k",alpha=.5)
ax.plot([-80,80],[4,4],color="k",alpha=.5)
ax.plot([-80,80],[5,5],color="k",alpha=.5)
ax.plot([0,0],[0,6],color="k",alpha=.5)
fmt='%.2f%%'    # y formate as percent
yticks = mtick.FormatStrFormatter(fmt)
ax.yaxis.set_major_formatter(yticks)
plt.show()
'''

# file rank by number of reads or requests
# top 10 files
result_file_2_io = default_result_dir + "\\" + "file_2_io.csv"
map_file_2_id = dict()
id = 1
top_35_file_2_io = dict() # { filename:{"read":number_of_reads,"write":number_of_writes,"io": =reads + writes} }
total_read = 0
total_write = 0
def add_to_top_num(top, num, filename, reads, writes ):
    inserted = False
    io = reads + writes
    for _key in top:
        if io > ( top[_key]["read"] + top[_key]["write"] ):
            top.__delitem__(_key)
            top.setdefault(filename, {"read":reads,"write":writes,"io":io})
            inserted = True
            break
    if not inserted and top.__len__() < num:
            top.setdefault(filename, {"read":reads,"write":writes,"io":io})

for line in open( result_file_2_io ):
    words = line.strip().split(",")
    filename = words.__getitem__(0)
    reads = int( words.__getitem__(1) )
    total_read += reads
    writes = int( words.__getitem__(2) )
    total_write += writes
    add_to_top_num(top_35_file_2_io,35,filename, reads, writes)
print("Total read = " + str(total_read) )
print("Total write = " + str(total_write) )
#print(top_10_reads_file)
#print(top_10_writes_file)
# sorted keys by value
def get_io(key):
    return top_35_file_2_io.__getitem__(key)["io"]
sorted_file_of_io = sorted(top_35_file_2_io, key=get_io, reverse=True)
#for file in sorted_file_of_io:
#    print(file + " = " + str(top_35_file_2_io[file]) )
x = []
index = 1
while index <= top_35_file_2_io.__len__():
    x.append(index)
    index += 1

y_read = []
y_write = []
percent = []
sum_io = 0
for file in sorted_file_of_io:
    y_read.append( top_35_file_2_io[file]["read"]/1000 )
    y_write.append( top_35_file_2_io[file]["write"]/1000 )
    sum_io += top_35_file_2_io[file]["io"]
    percent.append( sum_io/(total_read + total_write) * 100 )

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.bar(x, y_read, color="b", alpha=.5, label="Reads")
ax.bar(x, y_write, color="r", alpha=.5, bottom=y_read, label="Writes")
plt.legend(loc="center right") # (upper|center|lower)
ax.set_xlabel("File rank by number of request")
ax.set_ylabel("Number Of Requests (thousands)")
ax.set_title("File Heat")
#ax.yaxis.set_major_locator( mtick.MultipleLocator(1000) )
ax.yaxis.set_major_formatter( mtick.FormatStrFormatter('%d'))

ax2 = ax.twinx()
ax2.plot(x, percent, color="g", alpha=.5)
y2ticks = mtick.FormatStrFormatter('%.1f%%')
ax2.yaxis.set_major_formatter(y2ticks)
ax2.set_ylabel("Percent of requests")

plt.show()