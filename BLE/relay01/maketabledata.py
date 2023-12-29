import bluetooth
import random
import struct
import utime
import ubinascii
import micropython
import machine
# import manegement_s1
import info
import json
import os

def MakeData(fn, all_data,orthopedy_data):
    
    jf_open = open(fn, 'r')
    jf_load = json.load(jf_open)
    gapname = jf_load["device_number"]
    #gapname = "2"
    count = 0
    counter = 0
    
    with open(all_data, 'a', encoding='utf-8')as f1:
        with open(orthopedy_data,'r+',encoding='utf-8')as f2:
            d = f2.readlines()
            f2.seek(0)
            tabledata = ""
            
            for line in f2:
                counter += 1
            print(counter)
            
            for i in d:
                #print(i)
                if count is not counter-1:
                    #print(i[:-6])
                    print(i[:-3])
                    #print("@@@@@@@")
                    #if gapname in i[:-6]:
                    if gapname in i[:-3]:
                        tabledata += i
                    #print(d)
                    print("********")
                if count is counter-1:
                    #print(i[:-4])
                    print(i[:-2])
                    #print("@@@@@@@")
                    #if gapname in i[:-4]:
                    if gapname in i[:-2]:
                        tabledata += i
                    #print(d)
                    print("****")
                count += 1
                
            print(tabledata)
            f2.close()
            #f.truncate(0)
        #os.remove('data/makeroute_data.txt')
        f1.write(tabledata)
        f1.close()

if __name__ == "__main__":
    all_data = "data/routetabledata.txt"
    orthopedy_data = 'data/makeroute_data.txt'
    fn = 'info/DN01.json'
    MakeData(fn, all_data,orthopedy_data)
