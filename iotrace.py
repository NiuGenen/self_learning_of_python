#python 3.6
import os
import time

#io traces from http://iotta.snia.org/
test = True

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
log_count = 1000000
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

'''
test one file
'''
#file name format : tracename.dd-mm-yyyy.hh-mm-(PM|AM).trace
def get_base_time_stramp_in_s_from_file_name(name):
    print("DECODE TIME from " + name)
    parts = name.split('.')
    for part in parts:
        print(part)
    base_data_str = parts.__getitem__(1)
    print("DATA = " + base_data_str)
    base_time_str = parts.__getitem__(2)
    print("TIME = " + base_time_str)
    base_time_parts = base_time_str.split('-')
    base_time_h = int(base_time_parts.__getitem__(0))
    if base_time_parts.__getitem__(2) == "PM":
        base_time_h += 12
    base_time_m = int(base_time_parts.__getitem__(1))
    base_data_time_str = base_data_str + " " + str(base_time_h) + ":" + str(base_time_m)
    print("STR  = " + base_data_time_str )
    base_data_time = time.strptime(base_data_time_str, "%d-%m-%Y %H:%S")
    print( "DATA_TIME = " + base_data_time.__str__() )
    base_time_stramp = time.mktime( base_data_time )
    print("TIMESTRAMP in s  = " + str(base_time_stramp) )
    return int(base_time_stramp)

f = files.__getitem__(0)
print(f)
print( "TEST FILE : " + f )
trace = open( default_traces_dir + r"\\" + f, "r")
count = 1
base_timestramp_in_s  = get_base_time_stramp_in_s_from_file_name( f )
print("TimeStramp in Seconds = " + str(base_timestramp_in_s) )
base_timestramp_in_ns = base_timestramp_in_s * 1000 * 1000
print("TimeStramp in Seconds = " + str(base_timestramp_in_ns) )
for line in trace:
    line = line.strip().lower()
    if line == "beginheader":
        count = -1000
    if line == "endheader":
        count = 0
    if count < 100 and count > 0:
        print(line)
    if count >= 100:
        break
    count += 1

#end of script
log_close()