#python 3.6
import os
import time

#io traces from http://iotta.snia.org/

trace_name = "DevelopmentToolsRelease"
trace_absolute_dir = "E:\\"

default_source_dir = trace_absolute_dir + trace_name # E:\DevelopmentToolsRelease
default_traces_dir = default_source_dir + "\Traces"  # E:\DevelopmentToolsRelease\Traces

#get trace file name
files = os.listdir( default_traces_dir ) # E:\DevelopmentToolsRelease\Traces
print("LIST FILE : " + default_traces_dir)
for f in files:
    print( f )

#create result directory
default_result_dir = default_source_dir + r"\result" # E:\DevelopmentToolsRelease\result
if not os.path.exists( default_result_dir ):
    os.mkdir( default_result_dir )
    print( "CREATE    : " + default_result_dir )
else:
    print( "DIR EXIST : " + default_result_dir )

# Trace File Name Format : tracename.mm-dd-yyyy.hh-mm-(PM|AM).trace.csv
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
    base_data_time = time.strptime(base_data_time_str, "%m-%d-%Y %H:%M")
    base_time_stramp = time.mktime( base_data_time )

    return int(base_time_stramp)

#write dictionary to file, each line is : key,value
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

min_timestramp_s = 0 # minimun timestramp in second of all the requests in all file
max_timestramp_s = 0 # maxinum timestramp in second of all the requests in all file
total_read = 0       # number of all the read request
total_write = 0      # number of all the write request
size_read = 0        # size in byte of all the read request
size_write = 0       # size in byte of all the write request
count_s_2_read = dict()		# KEY: timestramp in second.    Value: number of reads
count_s_2_write = dict()	# KEY: timestramp in second.    Value: number of writes
count_byte_2_io = dict()  # KEY: request's size in byte.  Value: number of requests(Read & Write)
count_file_2_io = dict()  # KEY: file name.               Value: number of requests(Read & Write)
map_disknum_2_s_2_io = dict()	                 # KEY: disknum as int.              Value: dictinoary, which KET is timestramp in second, Value is number of requests
map_ns_to_offset_in_sector = dict()            # KEY: timestramp in nanosecond.    Value: data offset in sector(512 byte one sector) as int.   Note: for all the requests
map_ns_to_offset_in_sector_of_read = dict()    # KEY: timestramp in nanosecond.    Value: data offset in sector(512 byte one sector) as int.   Note: only for read request
map_ns_to_offset_in_sector_of_write = dict()   # KEY: timestramp in nanosecond.    Value: data offset in sector(512 byte one sector) as int.   Note: only for write request
def update_map_disknum_2_s_2_io(target, disknum,timestramp_s):  # function to update map_disknum_2_s_2_io
    if disknum in target:
        s_2_io = target[disknum]
        if timestramp_s in s_2_io:
            s_2_io[timestramp_s] += 1
        else:
            s_2_io.setdefault(timestramp_s, 1)
    else:
        target.setdefault(disknum, {timestramp_s:1})

# scanning trace files and accumulate data
for f in files: # Line 14 : files = os.listdir( default_traces_dir )
    print("Processing : " + f)
    file = open(default_traces_dir + r"\\" + f, "r")
    base_timestramp_in_s = get_base_time_stramp_in_s_from_file_name(f)	# get this file's base timestramp in second
    base_timestramp_in_ns = base_timestramp_in_s * 1000 * 1000
    print("Base time :" + str(base_timestramp_in_ns) )
    processing = False	# ignore header. processing=True when meet "endheader"
    for line in file:
        line = line.strip().lower()  # lower case of each line
        if processing:
            words = line.split(",")		# get words
            op_type = words.__getitem__(0)  # diskread/diskwrite
            if op_type != "diskread" and op_type != "diskwrite":
                continue

            op_timestramp_rel_ns = words.__getitem__(1)  # relatived timestramp in ns
            op_timestramp_ab_ns = int(op_timestramp_rel_ns) + base_timestramp_in_ns # absolute timestramp in nanosecond

            op_timestramp_ab_s = int(op_timestramp_ab_ns / 1000 / 1000) # absolute timestramp in second
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

            op_size = words.__getitem__(6)# io size in byte 16
            op_size = int(op_size, 16)
            if op_size in count_byte_2_io:  # accumulate number of requests according to its IO size
                count_byte_2_io[op_size] += 1
            else:
                count_byte_2_io.setdefault(op_size, 1)

            op_disk_num = words.__getitem__(8)# disk number
            op_disk_num = int(op_disk_num)
            update_map_disknum_2_s_2_io(map_disknum_2_s_2_io, op_disk_num, op_timestramp_ab_s) # update disknum

            op_offset_byte = words.__getitem__(5) # data offset in byte 16
            op_offset_byte = int(op_offset_byte, 16)
            op_offset_sector = int(op_offset_byte / 512) # data offset in sector
            map_ns_to_offset_in_sector.update( { op_timestramp_ab_ns: op_offset_sector } ) # timestramp in ns -> data offset in sector

            op_filename = words.__getitem__(14)

            if op_type == "diskread":
                total_read += 1
                size_read += op_size
                if op_timestramp_ab_s in count_s_2_read: # accumulate number of reads per second
                    count_s_2_read[op_timestramp_ab_s] += 1
                else:
                    count_s_2_read.setdefault(op_timestramp_ab_s, 1)
                map_ns_to_offset_in_sector_of_read.update( { op_timestramp_ab_ns: op_offset_sector } )
                if op_filename in count_file_2_io:
                    count_file_2_io[op_filename]["read"] += 1
                else:
                    count_file_2_io.setdefault(op_filename, {"read":1,"write":0})
            else:
                if op_type == "diskwrite":
                    total_write += 1
                    size_write += op_size
                    if op_timestramp_ab_s in count_s_2_write: # accumulate number of writes per second
                        count_s_2_write[op_timestramp_ab_s] += 1
                    else:
                        count_s_2_write.setdefault(op_timestramp_ab_s, 1)
                        map_ns_to_offset_in_sector_of_write.update({op_timestramp_ab_ns: op_offset_sector})
                    if op_filename in count_file_2_io:
                        count_file_2_io[op_filename]["write"] += 1
                    else:
                        count_file_2_io.setdefault(op_filename, {"read": 0, "write": 1})
        if line == "endheader":
            processing = True
    file.close()
    print("TotalRead  = " + str(total_read))
    print("TotalWrite = " + str(total_write))

print("--------------------------------------------------------")
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

# timestramp in second -> number of requests
# which means to merged s_2_read & s_2_write
print("Merge time(second) to read and write to IO......")
count_s_2_io = count_s_2_read.copy()
for w in count_s_2_write:
    if w in count_s_2_io:
        count_s_2_io[w] += count_s_2_write[w]
    else:
        count_s_2_io.setdefault(w, count_s_2_write[w])

# calculate interarrival time of whole requests
# and its data offset in sector
# NOTE: the timestramps of request need to be sorted
def count_inter_value_of_dict_sorted_by_key(source, target):
    # source & target are both dictionary
	# sorted source by its key, foreach two adjoining key-value, get their difference
	# target's KEY is the difference, Value is count
    first = True
    last_key = 0
    this_key = 0
    for key in sorted( source.keys() ):
        if first:
            last_key = key
            first = False
        else:
            this_key = key
            #inter_key = this_key - last_key
            inter_value = source[this_key] - source[last_key]
            if inter_value in target:
                target[inter_value] += 1
            else:
                target.setdefault(inter_value, 1)
            this_key = last_key
print("Calculating requests' inter time(ns) & offset(IO/Read/Write)......")
keys = map_ns_to_offset_in_sector.keys()
first = True # to get the first one in loop
ns_L = 0	# previous timestramp in nanosecond
ns_H = 0  # current timestramp in nanosecond
count_inter_ns_2_io = dict()             # KEY: difference between two adjoining requests' timestramp in nanosecond
count_inter_offset_sector_2_io = dict()  # KEY: difference between two adjoning requests' offset in sector
# both Value is number of requests(Read & Write)
for ns in sorted(keys): # sorted timestramp in ns
    if first:
        ns_L = ns
        first = False
    else:
        ns_H = ns
        inter_time_ns = ns_H - ns_L
        inter_offset_sector = map_ns_to_offset_in_sector[ns_H] - map_ns_to_offset_in_sector[ns_L]
        if inter_time_ns in count_inter_ns_2_io:
            count_inter_ns_2_io[ inter_time_ns ] += 1
        else:
            count_inter_ns_2_io.setdefault( inter_time_ns, 1 )
        if inter_offset_sector in count_inter_offset_sector_2_io:
            count_inter_offset_sector_2_io[ inter_offset_sector ] += 1
        else:
            count_inter_offset_sector_2_io.setdefault( inter_offset_sector, 1 )
        ns_L = ns_H
# KEY: difference between two adjoining requests' timestramp in nanosecond.   Value: number of reads(writes)
count_inter_offset_sector_2_read = dict()
count_inter_offset_sector_2_write = dict()
count_inter_value_of_dict_sorted_by_key(map_ns_to_offset_in_sector_of_read, count_inter_offset_sector_2_read)
count_inter_value_of_dict_sorted_by_key(map_ns_to_offset_in_sector_of_write, count_inter_offset_sector_2_write)

# construct output path of result
print("Constructing Output File Path......")
result_s_2_read = default_result_dir + r"\\" + "s_2_read.csv"
result_s_2_write = default_result_dir + r"\\" + "s_2_write.csv"
result_s_2_io = default_result_dir + r"\\" + "s_2_io.csv"
result_byte_2_io = default_result_dir + r"\\" + "byte_2_io.csv"
result_file_2_io = default_result_dir + r"\\" + "file_2_io.csv"
result_inter_offset_sector_2_io = default_result_dir + r"\\" + "inter_offset_sector_2_io.csv"
result_inter_offset_sector_2_read = default_result_dir + r"\\" + "inter_offset_sector_2_read.csv"
result_inter_offset_sector_2_write = default_result_dir + r"\\" + "inter_offset_sector_2_write.csv"
result_inter_ns_2_io = default_result_dir + r"\\" + "inter_ns_2_io.csv"

# write data to file
print("Writting data to file......")
print("Writting " + result_s_2_read)
write_dict_to_csv(result_s_2_read, count_s_2_read)
print("Writting " + result_s_2_write)
write_dict_to_csv(result_s_2_write, count_s_2_write)
print("Writting " + result_s_2_io)
write_dict_to_csv(result_s_2_io, count_s_2_io)
print("Writting " + result_byte_2_io)
write_dict_to_csv(result_byte_2_io, count_byte_2_io)
print("Writting " + result_file_2_io)
write_dict_to_csv(result_file_2_io, count_file_2_io)
file = open(result_file_2_io, "wb")
for d in count_file_2_io:
    file.write((str(d) + "," + str(count_file_2_io[d]["read"]) + "," + str(count_file_2_io[d]["write"]) + "\r\n").encode(encoding="utf-8"))
file.close()
print("Writting " + result_inter_offset_sector_2_io)
write_dict_to_csv(result_inter_offset_sector_2_io, count_inter_offset_sector_2_io)
print("Writting " + result_inter_offset_sector_2_read)
write_dict_to_csv(result_inter_offset_sector_2_read, count_inter_offset_sector_2_read)
print("Writting " + result_inter_offset_sector_2_write)
write_dict_to_csv(result_inter_offset_sector_2_write, count_inter_offset_sector_2_write)
print("Writting " + result_inter_ns_2_io)
write_dict_to_csv(result_inter_ns_2_io, count_inter_ns_2_io)
for disknum in map_disknum_2_s_2_io:
    result_s_2_io_unber_disknum = default_result_dir + r"\\" + "disk_" + str(disknum) + "_s_2_io.csv"
    s_2_io = map_disknum_2_s_2_io[disknum]
    print("Writting " + result_s_2_io_unber_disknum)
    write_dict_to_csv(result_s_2_io_unber_disknum, s_2_io)