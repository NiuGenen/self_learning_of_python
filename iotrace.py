#python 3.6
import os
import time

#io traces from http://iotta.snia.org/
test = False

cwd = os.getcwd()
print("CWD     = " + cwd)
default_source_dir = "E:\DevelopmentToolsRelease"
default_traces_dir = default_source_dir + "\Traces"
os.chdir( default_source_dir )
cwd = os.getcwd()
print("CWD     = " + cwd)

#define log_file
default_log_file = default_source_dir + "\log.txt"
log_file = open(default_log_file,"wb")
log_count = 100000
def log_line(info):
    global log_count
    log_count -= 1
    time_now = int(time.time())
    time_local = time.localtime(time_now)
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    log_file.write( ("[" + dt + "]    " + info + "\r\n").encode(encoding="utf-8") )
    if log_count < 0:
        log_file.flush()
        log_count = 1000000
def log_close():
    log_file.close()
#test log
if test:
    i = 1
    while(i < 10):
        log_line("test log " + str(i) )
        i += 1

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
    #print("DECODE TIME from " + name)
    parts = name.split('.')
    #for part in parts:
    #    print(part)
    base_data_str = parts.__getitem__(1)
    #print("DATA = " + base_data_str)
    base_time_str = parts.__getitem__(2)
    #print("TIME = " + base_time_str)
    base_time_parts = base_time_str.split('-')
    base_time_h = int(base_time_parts.__getitem__(0))
    if base_time_parts.__getitem__(2) == "PM":
        base_time_h += 12
    base_time_m = int(base_time_parts.__getitem__(1))
    base_data_time_str = base_data_str + " " + str(base_time_h) + ":" + str(base_time_m)
    #print("STR  = " + base_data_time_str )
    base_data_time = time.strptime(base_data_time_str, "%m-%d-%Y %H:%S")
    #print( "DATA_TIME = " + base_data_time.__str__() )
    base_time_stramp = time.mktime( base_data_time )
    #print("TIMESTRAMP in s  = " + str(base_time_stramp) )
    return int(base_time_stramp)

#write dict to file
def write_dict_to_csv(filename, dict):
    file = open(filename, "wb")
    for d in dict:
        file.write((str(d) + "," + str(dict[d]) + "\r\n").encode(encoding="utf-8"))
    file.close()

if test:
    '''
    test one file
    '''
    f = files.__getitem__(0)
    print(f)
    print( "TEST FILE : " + f )
    trace = open( default_traces_dir + r"\\" + f, "r")
    #count = 1
    processing = False
    base_timestramp_in_s  = get_base_time_stramp_in_s_from_file_name( f )
    print("TimeStramp in Seconds = " + str(base_timestramp_in_s) )
    base_timestramp_in_ns = base_timestramp_in_s * 1000 * 1000
    print("TimeStramp in Seconds = " + str(base_timestramp_in_ns) )
    total_read = 0
    total_write = 0
    count_s_2_read = dict()
    count_s_2_write = dict()
    for line in trace:
        line = line.strip().lower()
        #if line == "beginheader":
        #    count = -1000
        #if count < 10 and count > 0:
        if processing:
            #print(line)
            #print("-----------------------------------------------------------")
            words = line.split(",")
            #for word in words:
            #    print(word.strip())
            op_type = words.__getitem__(0)#diskread/diskwrite
            try:
                op_timestramp_rel_ns = words.__getitem__(1)#ns
            except IndexError as e:
                print("IndexError on line : " + line)
                continue
            op_size = words.__getitem__(6)#byte
            #print(op_type + " " + op_timestramp_rel_ns + " " + op_size)
            op_timestramp_ab_ns = int(op_timestramp_rel_ns) + base_timestramp_in_ns
            op_timestramp_ab_s = int(op_timestramp_ab_ns/1000/1000)
            if op_type == "diskread":
                total_read += 1
                if op_timestramp_ab_s in count_s_2_read:
                    count_s_2_read[op_timestramp_ab_s] += 1
                else:
                    count_s_2_read.setdefault(op_timestramp_ab_s,1)
            else:
                if op_type == "diskwrite":
                    total_write += 1
                if op_timestramp_ab_s in count_s_2_write:
                    count_s_2_write[op_timestramp_ab_s] += 1
                else:
                    count_s_2_write.setdefault(op_timestramp_ab_s,1)
            #print(op_type + " " + str(op_timestramp) + " " + op_size)
            #op_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(op_timestramp/1000000))
            #print(op_type + " " + str(op_time) + " " + op_size)
        #if count >= 10:
        #    break
        #count += 1
        if line == "endheader":
            #count = 0
            processing = True

    print("TotalRead  = " + str(total_read) )
    print("TotalWrite = " + str(total_write) )
    #print(count_s_2_read)
    print(count_s_2_read.__len__())#2577
    print(count_s_2_write.__len__())#3208
else:
    #not test
    min_base_time = get_base_time_stramp_in_s_from_file_name(files.__getitem__(0))
    for f in files:
        #print(f)
        base_time = get_base_time_stramp_in_s_from_file_name(f)
        print("Time = " + str(base_time) )
        #log_line("Time = " + str(base_time))
        if(base_time < min_base_time):
            min_base_time = base_time
    print("Min Time = " + str(min_base_time) )
    #min_timestramp_s = 0
    #max_timestramp_s = 0
    #total_read = 0
    #total_write = 0
    #size_read = 0
    #size_write = 0
    #count_s_2_read = dict()
    #count_s_2_write = dict()
    count_byte_2_io = dict()
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
                try:
                    op_timestramp_rel_ns = words.__getitem__(1)  # ns
                except IndexError as e:
                    print("IndexError on line : " + line)
                    continue
                op_size = words.__getitem__(6)  # byte
                op_size = int(op_size, 16)
                # print(op_type + " " + op_timestramp_rel_ns + " " + op_size)
                #op_timestramp_ab_ns = int(op_timestramp_rel_ns) + base_timestramp_in_ns
                #op_timestramp_ab_s = int(op_timestramp_ab_ns / 1000 / 1000)
                #if min_timestramp_s == 0:
                #    min_timestramp_s = op_timestramp_ab_s
                #else:
                #    if op_timestramp_ab_s < min_timestramp_s:
                #        min_timestramp_s = op_timestramp_ab_s
                #if max_timestramp_s == 0:
                #    max_timestramp_s = op_timestramp_ab_s
                #else:
                #    if op_timestramp_ab_s > max_timestramp_s:
                #        max_timestramp_s = op_timestramp_ab_s
                if op_type == "diskread":
                    #total_read += 1
                    #size_read += op_size
                    #if op_timestramp_ab_s in count_s_2_read:
                    #    count_s_2_read[op_timestramp_ab_s] += 1
                    #else:
                    #    count_s_2_read.setdefault(op_timestramp_ab_s, 1)
                    if op_size in count_byte_2_io:
                        count_byte_2_io[op_size] += 1
                    else:
                        count_byte_2_io.setdefault(op_size, 1)
                else:
                    if op_type == "diskwrite":
                        #total_write += 1
                        #size_write += op_size
                        #if op_timestramp_ab_s in count_s_2_write:
                        #    count_s_2_write[op_timestramp_ab_s] += 1
                        #else:
                        #    count_s_2_write.setdefault(op_timestramp_ab_s, 1)
                        if op_size in count_byte_2_io:
                            count_byte_2_io[op_size] += 1
                        else:
                            count_byte_2_io.setdefault(op_size, 1)
            if line == "endheader":
                processing = True
        #print("TotalRead  = " + str(total_read))
        #print("TotalWrite = " + str(total_write))
    #print("TotalRead  = " + str(total_read))
    #print("TotalWrite = " + str(total_write))
    #print("SizeRead = " + str(size_read) )
    #print("SizeWrite = " + str(size_write) )
    #print("MinTime = " + str(min_timestramp_s) )
    #print("MaxTime = " + str(max_timestramp_s) )
    #durning_time = max_timestramp_s - min_timestramp_s
    #print("AvgIOPS = " + str( int((total_write + total_read)/(durning_time)) ) )
    #print("AvgReadSize = " + str( int((size_read)/(durning_time)) ) )
    #print("AvgWriteSize = " + str( int((size_write)/(durning_time)) ) )
    #print("AvgReqSize = " + str( int((size_write + size_read)/(durning_time)) ) )

    #count_s_2_io = count_s_2_read.copy()
    #for w in count_s_2_write:
    #    if w in count_s_2_io:
    #        count_s_2_io[w] += count_s_2_write[w]
    #    else:
    #        count_s_2_io.setdefault(w, count_s_2_write[w])

    result_s_2_read = default_result_dir + r"\\" + "s_2_read.csv"
    result_s_2_write = default_result_dir + r"\\" + "s_2_write.csv"
    result_s_2_io = default_result_dir + r"\\" + "s_2_io.csv"
    result_byte_2_io = default_result_dir + r"\\" + "byte_2_io.csv"

    #write_dict_to_csv(result_s_2_read, count_s_2_read)
    #write_dict_to_csv(result_s_2_write, count_s_2_write)
    #write_dict_to_csv(result_s_2_io, count_s_2_io)
    write_dict_to_csv(result_byte_2_io, count_byte_2_io)

#end of script
log_close()