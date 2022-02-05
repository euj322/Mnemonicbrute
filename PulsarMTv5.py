# #!/usr/bin/python3
# encoding=utf8
# -*- coding: utf-8 -*-
"""
@author: hack
"""

from funcP import *
from consts import *

def createParser ():
    parser = argparse.ArgumentParser(description='Hunt to Mnemonic')
    parser.add_argument ('-b', '--bip', action='store', type=str, help='32/44/ETH/BTC/combo default Mode BTC', default='BTC')
    parser.add_argument ('-dbbtc', '--databasebtc', action='store', type=str, help='File BF BTC', default='')
    parser.add_argument ('-dbeth', '--databaseeth', action='store', type=str, help='File BF ETH', default='')
    parser.add_argument ('-th', '--threading', action='store', type=int, help='threading', default='1')
    parser.add_argument ('-m', '--mode', action='store', type=str, help='mode s/e/g/c', default='e')
    parser.add_argument ('-des', '--desc', action='store', type=str, help='description', default='local')
    parser.add_argument ('-bit', '--bit', action='store', type=int, help='128, 160, 192, 224, 256', default=128)
    parser.add_argument ('-dbg', '--debug', action='store', type=int, help='debug 0/1/2', default=0)
    parser.add_argument ('-em', '--mail', action='store_true', help='send mail')
    parser.add_argument ('-sl', '--sleep', action='store', type=int, help='pause start (sec)', default='5')
    parser.add_argument ('-bal', '--balance', action='store_true', help='check balance')
    parser.add_argument ('-brain', '--brain', action='store_true', help='check brain')
    parser.add_argument ('-telegram', '--telegram', action='store_true', help='send telegram')
    parser.add_argument ('-rnd', '--rnd', action='store_true', help='enable rnd')
    parser.add_argument ('-cd', '--customdir', action='store', type=str, help='custom dir for mode custom', default='')
    parser.add_argument ('-cw', '--customword', action='store', type=int, help='custom words for mode custom', default='6')
    parser.add_argument ('-cl', '--customlang', action='store', type=str, help='custom lang for mode custom', default='english')
    return parser.parse_args().bip, parser.parse_args().databasebtc, parser.parse_args().databaseeth, parser.parse_args().threading, parser.parse_args().mode, \
        parser.parse_args().desc, parser.parse_args().bit, parser.parse_args().debug, parser.parse_args().mail, parser.parse_args().sleep, parser.parse_args().balance, \
        parser.parse_args().brain, parser.parse_args().telegram, parser.parse_args().rnd, parser.parse_args().customdir, parser.parse_args().customword, parser.parse_args().customlang

def run(*args):
    inf.bip = args[0]
    inf.db_btc = args[1]
    inf.db_eth = args[2]
    inf.mode = args[3]
    email.desc = args[4]
    inf.bit = args[5]
    inf.debug = args[6]
    inf.mail = args[7]
    inf.th = args[8]
    inf.delay = args[9]
    inf.balance = args[10]
    inf.brain = args[11]
    inf.telegram = args[12]
    inf.rnd = args[13]
    inf.custom_dir = args[14]
    inf.custom_words = args[15]
    inf.custom_lang = args[16]
    total_counter = args[17]
    process_counter = args[18]
    brain_counter = args[19]
    found_counter = args[20]
    mnem_counter = args[21]
    tc = 0
    ind:int = 1
    if inf.bip == 'BTC' or inf.bip == '32' or inf.bip == '44': 
        mnemonic_lang = inf.mnemonic_BTC
        inf.bf_btc = load_BF(inf.db_btc)
        process_counter.increment(1)
    elif inf.bip == 'combo':
        mnemonic_lang = inf.mnemonic_BTC
        inf.bf_btc = load_BF(inf.db_btc)
        inf.bf_eth = load_BF(inf.db_eth)
        process_counter.increment(1)
    else: 
        mnemonic_lang = inf.mnemonic_ETH
        inf.bf_eth = load_BF(inf.db_eth)
        process_counter.increment(1)
    if inf.mode == 'g': inf.game_list = inf.load_game()
    if inf.mode == 'c': inf.custom_list = inf.load_custom(inf.custom_dir)
    try:
        while True:
            pp = multiprocessing.current_process()
            if pp.is_alive():
                pass
            else:
                process_counter.decrement(1)
            start_time = time()
            for mem in mnemonic_lang:
                mnem_counter.increment(1)
                if inf.mode == 'e' : mnemonic, seed_bytes, rnd = nnmnem(mem)
                else: mnemonic, seed_bytes = nnmnem(mem)
                #rnd
                if inf.rnd and inf.bip == 'combo':
                    total_counter.increment(brnd('btc',found_counter))
                    total_counter.increment(brnd('eth',found_counter))
                elif inf.rnd and (inf.bip == 'BTC' or inf.bip == '32' or inf.bip == '44'):
                    total_counter.increment(brnd('btc',found_counter))
                elif inf.rnd and inf.bip == 'ETH':
                    total_counter.increment(brnd('eth',found_counter))
                #brain
                if inf.brain and inf.bip !='ETH':
                    brain_counter.increment(bw(mnemonic, False, found_counter))
                    brain_counter.increment(bw(seed_bytes.hex(), True, found_counter))
                    if inf.mode == 'e' : brain_counter.increment(bw(rnd, True, found_counter))
                #function bip
                if inf.bip == "32" : total_counter.increment(b32(mnemonic,seed_bytes, found_counter))
                if inf.bip == "44" : total_counter.increment(b44(mnemonic,seed_bytes, found_counter))
                if inf.bip == "ETH": total_counter.increment(bETH(mnemonic,seed_bytes, found_counter))
                if inf.bip == "BTC": 
                    total_counter.increment(b32(mnemonic,seed_bytes, found_counter))
                    total_counter.increment(bBTC(mnemonic,seed_bytes, found_counter))
                if inf.bip == 'combo':
                    total_counter.increment(b32(mnemonic,seed_bytes, found_counter))
                    total_counter.increment(bBTC(mnemonic,seed_bytes, found_counter))
                    total_counter.increment(bETH(mnemonic,seed_bytes, found_counter))
                    
            st = time() - start_time
            ftc = tc
            tc = total_counter.value()
            tc_float, tc_hash = convert_int(tc)
            btc = tc - ftc
            speed = int((btc/st))
            speed_float, speed_hash = convert_int(speed)
            mc = mnem_counter.value()
            fc = found_counter.value()
            bc:int = brain_counter.value()
            bc_float, bc_hash = convert_int(bc)
            pc = process_counter.value()
            if multiprocessing.current_process().name == '0':
                print(f'{yellow}> Cores:{pc} | Mnemonic: {mc} | Hash MNEM: {tc_float:.2f} {tc_hash} | Hash BRAIN: {bc_float:.2f} {bc_hash} | {speed_float:.2f} {speed_hash} | Found: {fc}',end='\r')
            inf.count = 0
            ind += 1
    except(KeyboardInterrupt, SystemExit):
        print('\n[EXIT] Interrupted by the user.')
        logger_info.info('[EXIT] Interrupted by the user.')
        sys.exit()

if __name__ == "__main__":
    inf.bip, inf.db_btc, inf.db_eth, inf.th, inf.mode, email.desc, inf.bit, inf.debug, inf.mail, inf.delay, inf.balance, \
        inf.brain, inf.telegram, inf.rnd, inf.custom_dir, inf.custom_words, inf.custom_lang  = createParser()
    print('-'*70,end='\n')
    print(f'{green}Thank you very much: @iceland2k14 for his libraries!')

    if test():
        print(f'{green}[I] TEST: OK!')
        logger_info.info(f'[I] TEST: OK!')
    else:
        print(f'{red}[E] TEST: ERROR')
        logger_err.error(('[E] TEST: ERROR'))
        sys.exit()

    if inf.bip in ('32', '44', 'ETH', 'BTC', 'combo'):
        pass
    else:
        print(f'{red}[E] Wrong BIP selected')
        logger_err.error(('[E] Wrong BIP selected'))
        sys.exit()

    if inf.bit in (128, 160, 192, 224, 256):
        pass          
    else:
        print(f'{red}[E] Wrong words selected')
        logger_err.error(('[E] Wrong words selected'))
        sys.exit()

    if inf.mode in ('s', 'e', 'g', 'c'):
        if (inf.mode == 's'):
            inf.mode_text = 'Standart'
        elif (inf.mode == 'e'):
            inf.mode_text = 'Mnemonic from Entropy'
        elif (inf.mode == 'g'):
            inf.mode_text = 'Game words'
        elif (inf.mode == 'c'):
            if inf.custom_dir == '':
                print(f'{red}[E] NOT custom file')
                logger_err.error(('[E] NOT custom file'))
                sys.exit()
            inf.mode_text = 'Custom words'
    else:
        print(f'{red}[E] Wrong mode selected')
        logger_err.error(('[E] Wrong mode selected'))
        sys.exit()

    if inf.th < 1:
        print(f'{red}[E] The number of processes must be greater than 0')
        logger_err.error(('[E] The number of processes must be greater than 0'))
        sys.exit()

    if inf.th > multiprocessing.cpu_count():
        print(f'{red}[I] The specified number of processes exceeds the allowed')
        print(f'{green}[I] FIXED for the allowed number of processes')
        inf.th = multiprocessing.cpu_count()

    print('-'*70,end='\n')
    print(f'[I] Version: {inf.version}')
    logger_info.info(f'Start HUNT version {inf.version}')
    print(f'[I] Total kernel of CPU: {multiprocessing.cpu_count()}')
    print(f'[I] Used kernel: {inf.th}')
    print(f'[I] Mode Search: BIP-{inf.bip} {inf.mode_text}')
    logger_info.info(f'[I] Mode Search: BIP-{inf.bip} {inf.mode_text}')
    if inf.bip == 'ETH': print(f'[I] Bloom Filter ETH: {inf.db_eth}')
    elif inf.bip == 'combo': 
        print(f'[I] Bloom Filter ETH: {inf.db_eth}')
        print(f'[I] Bloom Filter BTC: {inf.db_btc}')
    else: print(f'[I] Bloom Filter BTC: {inf.db_btc}')
    if inf.custom_dir != '': print(f'[I] Сustom dictionary: {inf.custom_dir}')
    if inf.custom_dir != '': print(f'[I] Сustom words: {inf.custom_words}')
    if inf.custom_dir != '': print(f'[I] Languages at work: {inf.custom_lang}')
    if inf.mode == 's' and inf.bip == 'ETH': print(f'[I] Languages at work ETH: {inf.mnemonic_ETH}')
    elif inf.mode == 'e' and inf.bip == 'ETH': print(f'[I] Languages at work ETH: {inf.mnemonic_ETH}')
    elif inf.bip == 'combo':
        print(f'[I] Languages at work ETH: {inf.mnemonic_ETH}')
        print(f'[I] Languages at work BTC: {inf.mnemonic_BTC}')
    else: print(f'[I] Languages at work BTC: {inf.mnemonic_BTC}')
    
    print(f'[I] Work BIT: {inf.bit}')
    print(f'[I] Description client: {email.desc}')
    print(f'[I] Smooth start {inf.delay} sec')

    if inf.mail: print('[I] Send mail: On')
    else: print('[I] Send mail: Off')
    if inf.balance: print('[I] Check balance BTC: On')
    else: print('[I] Check balance: Off')
    if inf.brain and inf.bip != 'ETH': print('[I] BrainWallet: On')
    else: print('[I] BrainWallet: Off')
    if inf.telegram: print('[I] Telegram: On')
    else: print('[I] Telegram: Off')
    if inf.rnd: print('[I] Random check hash: On')
    else: print('[I] Random check hash: off')
    print('-'*70,end='\n')
    
    total_counter = Counter(0)
    process_counter = Counter(0)
    brain_counter = Counter(0)
    found_counter = Counter(0)
    mnem_counter = Counter(0)

    procs = []
    try:
        for r in range(inf.th): 
            p = Process(target=run, name= str(r), args=(inf.bip, inf.db_btc, inf.db_eth, inf.mode, email.desc, inf.bit, inf.debug, inf.mail, inf.th, 
                inf.delay, inf.balance, inf.brain, inf.telegram, inf.rnd, inf.custom_dir, inf.custom_words, inf.custom_lang, total_counter, process_counter, brain_counter, found_counter, mnem_counter,))
            procs.append(p)
            p.start()
        for proc in procs: proc.join()
    except(KeyboardInterrupt, SystemExit):
        print('\n[EXIT] Interrupted by the user.')
        logger_info.info('[EXIT] Interrupted by the user.')
        sys.exit()
