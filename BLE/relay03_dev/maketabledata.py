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
    
    jf_open = open('info/DN03.json', 'r')
    jf_load = json.load(jf_open)
    gapname = jf_load["device_number"]
    #print(gapname)
    
    with open("data/routetabledata.txt", 'w', encoding='utf-8')as f1:
        with open('data/makeroute_data.txt','r+',encoding='utf-8')as f2:
            #d = f2.readlines()
            f2.seek(0)
            tabledata = ""
            for i in f2:
                #check = f2.readline(5)
                if gapname in i[:4]:
                    tabledata += i
                    #print(check)
                    print(i)
            print("****")
            print(tabledata)
            f2.close()
            #f.truncate(0)
        #os.remove('data/makeroute_data.txt')
        f1.write(tabledata)
        f1.close()

if __name__ == "__main__":
    MakeTableData()
