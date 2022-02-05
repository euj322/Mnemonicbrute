# #!/usr/bin/python3
# encoding=utf8
# -*- coding: utf-8 -*-
"""
@author: Noname400
"""
from bitcoinlib.encoding import addr_base58_to_pubkeyhash,addr_bech32_to_pubkeyhash
import sys

def convert(file_in,file_out):
    print("[I] File input -> " + file_in)
    print("[I] File output -> " + file_out)
    bech_ = 1
    base_ = 1
    i = 0
    line_10 = 100000
    ii = 1
    count = 0
    f = open(file_in,'r')
    fw = open(file_out,'w')
    while True:
        addr = f.readline().strip()
        if addr[:2] == '0x' : 
            print('адреса ETH не требуют обработки, их надо сразу подавать в БлюмФильтр \n \
                                    но они должны быть без 0x')
            f.close()
            fw.close()
            sys.exit()
        if not addr:
            print('[F] Finish!')
            f.close()
            fw.close()
            sys.exit()

        count += 1
        if count == line_10:
            print(f"> skip: {ii} | pass line:{i} (bech32:{bech_} base58:{base_}) | total: {count}",end='\r')
            line_10 +=100000


        if len(addr) <= 34:
            try:
                res = addr_base58_to_pubkeyhash(addr, as_hex=True)
            except:
                ii +=1
                #print('ошибка в строке:',count)
            else:
                fw.write(res+'\n')
                base_ +=1
                i += 1
        else:
            try:
                res = addr_bech32_to_pubkeyhash(addr, as_hex=True)
            except:
                ii +=1
                #print('ошибка в строке:',count)
            else:
                fw.write(res+'\n')
                bech_ +=1
                i += 1


if __name__ == "__main__":

    if len (sys.argv) < 3:
        print ("Ошибка. Слишком мало параметров.")
        sys.exit (1)

    if len (sys.argv) > 3:
        print ("Ошибка. Слишком много параметров.")
        sys.exit (1)

    file_in = sys.argv[1]
    file_out = sys.argv[2]

    convert(file_in,file_out)