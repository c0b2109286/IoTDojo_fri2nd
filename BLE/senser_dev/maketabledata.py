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

def MakeTableData():
    
    jf_open = open('info/SN01.json', 'r')
    jf_load = json.load(jf_open)
    gapname = jf_load["device_number"]
    
    with open("data/routetabledata.txt", 'w', encoding='utf-8')as f1:
        with open('data/makeroute_data.txt','r+',encoding='utf-8')as f2:
            d = f2.readlines()
            f2.seek(0)
            tabledata = ""
            for i in d:
                if gapname in i:
                    tabledata += i
                print(d)
                print("****")
            print(tabledata)
            f2.close()
            #f.truncate(0)
        #os.remove('data/makeroute_data.txt')
        f1.write(tabledata)
        f1.close()

if __name__ == "__main__":
    MakeTableData()
