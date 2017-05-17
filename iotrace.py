#python 3.6
import os
import time

#io traces from http://iotta.snia.org/

default_source_dir = "E:\DevelopmentToolsRelease"
default_traces_dir = default_source_dir + "\Traces"

#get trace file name
files = os.listdir( default_traces_dir )
print("LIST FILE : " + default_traces_dir)
for f in files:
    print(f)

#create result directory
default_result_dir = default_source_dir + r"\result"
if not os.path.exists( default_result_dir ):
    os.mkdir( default_result_dir )
    print( "CREATE    : " + default_result_dir )
else:
    print( "DIR EXIST : " + default_result_dir )

#file name format : tracename.dd-mm-yyyy.hh-mm-(PM|AM).trace
def get_base_time_stramp_in_s_from_file_name(name):
    parts = name.split('.')
    base_data_str = parts.__getitem__(1)
    base_time_str = parts.__getitem__(2)
    base_time_parts = base_time_str.split('-')
    base_time_h = int(base_time_parts.__getitem__(0))
    if base_time_parts.__getitem__(2) == "PM":
        base_time_h += 12
    base_time_m = int(base_time_parts.__getitem__(1))
    base_data_time_str = base_data_str + " " + str(base_time_h) + ":" + str(base_time_m)
    base_data_time = time.strptime(base_data_time_str, "%m-%d-%Y %H:%S")
    base_time_stramp = time.mktime( base_data_time )
    return int(base_time_stramp)

#write dict to file
def write_dict_to_csv(filename, dict):
    file = open(filename, "wb")
    for d in dict:
        file.write((str(d) + "," + str(dict[d]) + "\r\n").encode(encoding="utf-8"))
    file.close()

min_base_time = get_base_time_stramp_in_s_from_file_name(files.__getitem__(0))
for f in files:
    print(f)
    base_time = get_base_time_stramp_in_s_from_file_name(f)
    print("Time = " + str(base_time) )
    if(base_time < min_base_time):
        min_base_time = base_time
print("Min Time = " + str(min_base_time) )

min_timestramp_s = 0
max_timestramp_s = 0
total_read = 0
total_write = 0
size_read = 0
size_write = 0
#count_s_2_read = dict()
#count_s_2_write = dict()
#count_byte_2_io = dict()
map_disknum_2_s_2_io = dict()# each disknum to one dict, which is timestramp in second to io
#list_ns_of_io = []
map_ns_to_offset_in_sector = dict()
def update_map_disknum_2_s_2_io(target, disknum,timestramp_s):
    if disknum in target:
        s_2_io = target[disknum]
        if timestramp_s in s_2_io:
            s_2_io[timestramp_s] += 1
        else:
            s_2_io.setdefault(timestramp_s, 1)
    else:
        target.setdefault(disknum, {timestramp_s:1})

for f in files:
    print("Processing : " + f)
    file = open(default_traces_dir + r"\\" + f, "r")
    base_timestramp_in_s = get_base_time_stramp_in_s_from_file_name(f)
    base_timestramp_in_ns = base_timestramp_in_s * 1000 * 1000
    print("Base time :" + str(base_timestramp_in_ns) )
    processing = False
    for line in file:
        line = line.strip().lower()
        if processing:
            words = line.split(",")
            op_type = words.__getitem__(0)  # diskread/diskwrite
            if op_type != "diskread" and op_type != "diskwrite":
                continue

            op_timestramp_rel_ns = words.__getitem__(1)  # relatived timestramp in ns
            op_timestramp_ab_ns = int(op_timestramp_rel_ns) + base_timestramp_in_ns # absolute timestramp in ns
            #list_ns_of_io.append(op_timestramp_ab_ns)   # update timestramp ns list # assume no requests has same timestramp in ns
            op_timestramp_ab_s = int(op_timestramp_ab_ns / 1000 / 1000) # absolute timestramp in s
            if min_timestramp_s == 0:
                min_timestramp_s = op_timestramp_ab_s
            else:
                if op_timestramp_ab_s < min_timestramp_s:
                    min_timestramp_s = op_timestramp_ab_s
            if max_timestramp_s == 0:
                max_timestramp_s = op_timestramp_ab_s
            else:
                if op_timestramp_ab_s > max_timestramp_s:
                    max_timestramp_s = op_timestramp_ab_s

            op_size = words.__getitem__(6)  # io size in byte 16
            op_size = int(op_size, 16)
            #if op_size in count_byte_2_io:
            #    count_byte_2_io[op_size] += 1
            #else:
            #    count_byte_2_io.setdefault(op_size, 1)

            op_disk_num = words.__getitem__(8) # disk number
            op_disk_num = int(op_disk_num)
            update_map_disknum_2_s_2_io(map_disknum_2_s_2_io, op_disk_num, op_timestramp_ab_s) # update disknum

            op_offset_byte = words.__getitem__(5) # data offset in byte 16
            op_offset_byte = int(op_offset_byte, 16)
            op_offset_sector = int(op_offset_byte / 512) # data offset in sector
            #map_ns_to_offset_in_sector.update( { op_timestramp_ab_ns: op_offset_sector } ) # timestramp of request to its data offset in sector

            if op_type == "diskread":
                total_read += 1
                size_read += op_size
                #if op_timestramp_ab_s in count_s_2_read:
                #    count_s_2_read[op_timestramp_ab_s] += 1
                #else:
                #    count_s_2_read.setdefault(op_timestramp_ab_s, 1)
            else:
                if op_type == "diskwrite":
                    total_write += 1
                    size_write += op_size
                    #if op_timestramp_ab_s in count_s_2_write:
                    #    count_s_2_write[op_timestramp_ab_s] += 1
                    #else:
                    #    count_s_2_write.setdefault(op_timestramp_ab_s, 1)
        if line == "endheader":
            processing = True
    file.close()
    print("TotalRead  = " + str(total_read))
    print("TotalWrite = " + str(total_write))
print("TotalRead  = " + str(total_read))
print("TotalWrite = " + str(total_write))
print("SizeRead = " + str(size_read) )
print("SizeWrite = " + str(size_write) )
print("MinTime = " + str(min_timestramp_s) )
print("MaxTime = " + str(max_timestramp_s) )
durning_time = max_timestramp_s - min_timestramp_s
print("AvgIOPS = " + str( int((total_write + total_read)/(durning_time)) ) )
print("AvgReadSize = " + str( int((size_read)/(durning_time)) ) )
print("AvgWriteSize = " + str( int((size_write)/(durning_time)) ) )
print("AvgReqSize = " + str( int((size_write + size_read)/(durning_time)) ) )

# count timestramp in second to io
# which means to merged s_2_read & s_2_write
#count_s_2_io = count_s_2_read.copy()
#for w in count_s_2_write:
#    if w in count_s_2_io:
#        count_s_2_io[w] += count_s_2_write[w]
#    else:
#        count_s_2_io.setdefault(w, count_s_2_write[w])

# calculate interarrival time of whole requests
# and its data offset of sector
'''
keys = map_ns_to_offset_in_sector.keys()
first = True
ns_L = 0
ns_H = 0
count_inter_ns_2_io = dict()
count_inter_offset_sector_2_io = dict()
for ns in sorted(keys): # sorted timestramp in ns of request
    if first:
        ns_L = ns
        first = False
    else:
        ns_H = ns
        interarrival_time_ns = ns_H - ns_L
        interarrival_offset_sector = map_ns_to_offset_in_sector[ns_H] - map_ns_to_offset_in_sector[ns_L]
        if interarrival_time_ns in count_inter_ns_2_io:
            count_inter_ns_2_io[ interarrival_time_ns ] += 1
        else:
            count_inter_ns_2_io.setdefault( interarrival_time_ns, 1 )
        if interarrival_offset_sector in count_inter_offset_sector_2_io:
            count_inter_offset_sector_2_io[ interarrival_offset_sector ] += 1
        else:
            count_inter_offset_sector_2_io.setdefault( interarrival_offset_sector, 1 )
        ns_L = ns_H
'''
# construct output path of result
result_s_2_read = default_result_dir + r"\\" + "s_2_read.csv"
result_s_2_write = default_result_dir + r"\\" + "s_2_write.csv"
result_s_2_io = default_result_dir + r"\\" + "s_2_io.csv"
result_byte_2_io = default_result_dir + r"\\" + "byte_2_io.csv"
result_inter_offset_sector_2_io = default_result_dir + r"\\" + "inter_offset_sector_2_io.csv"
result_inter_ns_2_io = default_result_dir + r"\\" + "inter_ns_2_io.csv"

# write data to file
#write_dict_to_csv(result_s_2_read, count_s_2_read)
#write_dict_to_csv(result_s_2_write, count_s_2_write)
#write_dict_to_csv(result_s_2_io, count_s_2_io)
#write_dict_to_csv(result_byte_2_io, count_byte_2_io)
#write_dict_to_csv(result_inter_offset_sector_2_io, count_inter_offset_sector_2_io)
#write_dict_to_csv(result_inter_ns_2_io, count_inter_ns_2_io)

for disknum in map_disknum_2_s_2_io:
    result_s_2_io_unber_disknum = default_result_dir + r"\\" + "disk_" + str(disknum) + "_s_2_io.csv"
    s_2_io = map_disknum_2_s_2_io[disknum]
    write_dict_to_csv(result_s_2_io_unber_disknum, s_2_io)
