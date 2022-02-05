# #!/usr/bin/python3
# encoding=utf8
# -*- coding: utf-8 -*-
"""
@author: Noname400
"""

import argparse
import ctypes
import datetime
from time import sleep, time
import logging
import multiprocessing
import os
import platform
import secrets
import smtplib
import socket
import string
import sys
from binascii import hexlify
import ecdsa,hashlib, binascii, base58
from ecdsa.ecdsa import digest_integer
from logging import Formatter
from multiprocessing import Lock, Process, Value
from random import randint
from secrets import choice
import bitcoin
import requests
from bip32 import BIP32
from bloomfilter import BloomFilter
from colorama import Back, Fore, Style, init
from mnemonic import Mnemonic

import secp256k1_lib

init(autoreset = True)

yellow = Fore.YELLOW+Style.BRIGHT
red = Fore.RED+Style.BRIGHT
#clear = Style.RESET_ALL
green = Fore.GREEN+Style.BRIGHT

current_path = os.path.dirname(os.path.realpath(__file__))
logger_found = logging.getLogger('FOUND')
logger_found.setLevel(logging.INFO)
handler_found = logging.FileHandler(os.path.join(current_path, 'found.log'), 'a' , encoding ='utf-8')
handler_found.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger_found.addHandler(handler_found)

logger_info = logging.getLogger('INFO')
logger_info.setLevel(logging.INFO)
handler_info = logging.FileHandler(os.path.join(current_path, 'info.log'), 'a' , encoding ='utf-8')
handler_info.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger_info.addHandler(handler_info)

logger_dbg = logging.getLogger('DEBUG')
logger_dbg.setLevel(logging.DEBUG)
handler_dbg = logging.FileHandler(os.path.join(current_path, 'debug.log'), 'w' , encoding ='utf-8')
logger_dbg.addHandler(handler_dbg)

logger_err = logging.getLogger('ERROR')
logger_err.setLevel(logging.DEBUG)
handler_err = logging.FileHandler(os.path.join(current_path, 'error.log'), 'w' , encoding ='utf-8')
handler_err.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger_err.addHandler(handler_err)

class Counter:
    def __init__(self, initval=0):
        self.val = Value(ctypes.c_longlong, initval)
        self.lock = Lock()
    def increment(self, nom):
        with self.lock:
            self.val.value += nom
    def decrement(self, nom):
        with self.lock:
            self.val.value -= nom
    def zero(self):
        with self.lock:
            self.val.value = 0
    def value(self):
        with self.lock:
            return self.val.value

class telegram:
    token = '5097432912:AAE6iDOa-q1Q2BWkHQF5o-qjMiM_Ra0ioIQ'
    channel_id = '@mnemonicHUNT'

class email:
    host:str = "smtp.timeweb.ru" # SMTP server
    port:int = 25
    password:str = '12qwerty34'
    subject:str = '* Find Mnemonic *'
    to_addr:str = 'hunt@quadrotech.ru'
    from_addr:str = 'hunt@quadrotech.ru'
    desc:str = ''

class inf:
    def load_game():
        try:
            f = open('wl/game.txt','r')
            l = [line.strip() for line in f]
            f.close()
        except:
            logger_err.error('Error load wl/game.txt')
            print(f'[E] Error load wl/game.txt')
            pp = multiprocessing.current_process()
            pp.close()
            sys.exit()
        else:
            return l
    def load_custom(custom_file):
        try:
            f = open(custom_file,'r')
            l = [line.strip() for line in f]
            f.close()
        except:
            logger_err.error(f'Error load {custom_file}')
            print(f'[E] Error load {custom_file}')
            pp = multiprocessing.current_process()
            pp.close()
            sys.exit()
        else:
            return l
    version:str = '* Pulsar v5.2.6 multiT Hash160 *'
    mnemonic_BTC:list = ['english', 'japanese', 'chinese_simplified', 'chinese_traditional'] # ['english', 'chinese_simplified', 'chinese_traditional', 'french', 'italian', 'spanish', 'korean','japanese','portuguese','czech']
    mnemonic_ETH:list = ['english'] # ['english', 'chinese_simplified', 'chinese_traditional', 'french', 'italian', 'spanish', 'korean','japanese','portuguese','czech']
    #general
    th:int = 1 #number of processes
    bit:int = 128
    bf_btc:BloomFilter
    bf_eth:BloomFilter
    db_btc:str = ''
    db_eth:str = ''
    lbtc:list = ['44','49','84']
    l32:list = ["m/0'/","m/44'/0'/"]
    l32_:list = ["","'"]#"","'"
    l44:list = ['0','145','236'] # ["0","145","236","156","177","222","192","2","3","5","7","8","20","22","28","90","133","147","2301","175","216"]
    leth:list = ['60','61'] #['60','61']
    bip:str = 'BTC'
    game_list:list = []
    rnd = False
    custom_list:list = []
    custom_dir:str = ''
    custom_words:int = 12
    custom_lang:str = ''
    #balance
    balance:bool = False
    bal_err:int = 0
    bal_server:list = ['https://api.blockcypher.com/v1/btc/main/addrs/', 'https://rest.bitcoin.com/v2/address/details/', 'https://sochain.com/api/v2/address/BTC/', \
        'https://blockchain.info/rawaddr/']
    ETH_bal_server:list = ['https://api.blockchair.com/ethereum/dashboards/address/','https://api.etherscan.io/api?module=account&action=balance&address=']
    bal_srv_count:int = 0
    bal_all_err = 0
    #brain
    brain = False
    #telegram
    telegram = False
    telegram_err = 0
    #mail
    mail:bool = False
    mail_err:str = 0
    #debug
    debug:bool = False
    #
    count:int = 1
    count_nem = 0
    dt_now:str = ''
    delay:int = 5
    work_time:float = 0.0
    mode:str = ''
    mode_text:str = ''