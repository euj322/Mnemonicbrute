#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Noname400
"""

from consts import *

def generate_private_key():
    curve = ecdsa.curves.SECP256k1
    se = random_secret_exponent(curve.order)
    from_secret_exponent = ecdsa.keys.SigningKey.from_secret_exponent
    return int(from_secret_exponent(se, curve, hashlib.sha256).to_string().hex(),16)

def random_secret_exponent(curve_order):
    while True:
        bytes = secrets.token_bytes(32)
        random_hex = hexlify(bytes)
        random_int = int(random_hex, 16)
        if random_int >= 1 and random_int < curve_order:
            return random_int
        
        else:
            curve = ecdsa.curves.SECP256k1 
            random_secret_exponent(curve.order)

def send_telegram(text: str):
    try:
        requests.get('https://api.telegram.org/bot{}/sendMessage'.format(telegram.token), params=dict(
        chat_id=telegram.channel_id,
        text=text))
        sleep(20)
    except:
        print(f'{red}[E] Error send telegram.')
        logger_err.error(f'[E] Error send telegram.')
        if inf.telegram_err > 3 : 
            inf.telegram == False
            return
        else: 
            inf.telegram_err += 1
            sleep(10)
            return send_telegram(text)

def convert_int(cou:int):
    if cou < 1000:
        res = cou
        return res,'hash'
    if cou >= 1000 and cou < 1000000:
        res = cou/1000
        return res, 'Khash'
    if cou >= 1000000 and cou < 1000000000:
        res = cou/1000000
        return res, 'Mhash'
    if cou >= 1000000000 and cou < 1000000000000:
        res = cou/1000000000
        return res, 'Ghash'
    if cou >= 1000000000000 and cou < 1000000000000000:
        res = cou/1000000000000
        return res, 'Thash'
    if cou >= 1000000000000000 and cou < 1000000000000000000:
        res = cou/1000000000000000
        return res, 'Phash'
    
def reverse_string(s):
    return s[::-1]

def bw(text, backspace, fc):
    f1 = []
    f2 = []
    co = 0
    co_count = 0
    if backspace: no_bs = text.replace(' ', '')
    text_rev = reverse_string(text)
    f1.append(bitcoin.sha256(text))
    if backspace: f1.append(bitcoin.sha256(no_bs))
    f1.append(bitcoin.sha256(text_rev))
    f1.append(bitcoin.dbl_sha256(text))
    if backspace: f1.append(bitcoin.dbl_sha256(no_bs))
    f1.append(bitcoin.dbl_sha256(text_rev))
    for res in f1:
        f2.append(secp256k1_lib.privatekey_to_h160(0, True, int(res,16)))
        f2.append(secp256k1_lib.privatekey_to_h160(0, False, int(res,16)))
    for res in f2:
        if inf.debug > 0:
            addr_c = secp256k1_lib.hash_to_address(0, False, res)
            addr_cbc = secp256k1_lib.hash_to_address(2, False, res)
            print(f'[D][BRAIN] PVK:{f1[co//2]} | HASH160:{res.hex()} | {addr_c} | {addr_cbc} | {text}')
            logger_dbg.debug(f'[D][BRAIN] PVK:{f1[co//2]} | HASH160:{res.hex()} | {addr_c} | {addr_cbc} | {text}')
        if res in inf.bf_btc:
            addr_c = secp256k1_lib.hash_to_address(0, False, res)
            addr_cbc = secp256k1_lib.hash_to_address(2, False, res)
            if inf.debug > 0:
                print(f'[D][F][BRAIN] PVK:{f1[co//2]} | HASH160:{res.hex()} | {addr_c} | {addr_cbc} | {text}')
                logger_dbg.debug(f'[D][F][BRAIN] PVK:{f1[co//2]} | HASH160:{res.hex()} | {addr_c} | {addr_cbc} | {text}')
            if inf.debug < 1:
                if inf.balance:
                    tx1, b1 = get_balance(addr_c,'BTC')
                    tx4, b4 = get_balance(addr_cbc,'BTC')
                    if (tx1 > 0) or (tx4 > 0):
                        print(f'\n[F][BRAIN] Found transaction! PVK:{f1[co//2]} | HASH160:{res.hex()} | {addr_c}:{b1} | {addr_cbc}:{b4} | {text}')
                        logger_found.info(f'[F][BRAIN] Found transaction! PVK:{f1[co//2]} | HASH160:{res.hex()} | {addr_c}:{b1} | {addr_cbc}:{b4} | {text}')
                    if (b1 > 0) or (b4 > 0):
                        print(f'\n[F][BRAIN] Found address in balance! PVK:{f1[co//2]} | HASH160:{res.hex()} | {addr_c} | {addr_cbc} | {text}')
                        logger_found.info(f'[F][BRAIN] Found address in balance! PVK:{f1[co//2]} | HASH160:{res.hex()} | {addr_c} | {addr_cbc} | {text}')
                        if inf.mail:
                            send_email(f'[F][BRAIN PVK:{f1[co//2]} | HASH160:{res.hex()} | {addr_c} | {addr_cbc} | {text}')
                        if inf.telegram:
                            send_telegram(f'[F][BRAIN PVK:{f1[co//2]} | HASH160:{res.hex()} | {addr_c} | {addr_cbc} | {text}')  
                        fc.increment(1)
                    else:
                        print(f'\n[F][BRAIN] Found address balance 0.0 PVK:{f1[co//2]} | HASH160:{res.hex()} | {addr_c} | {addr_cbc} | {text}')
                        logger_found.info(f'[F][BRAIN] Found address balance 0.0 PVK:{f1[co//2]} | HASH160:{res.hex()} | {addr_c} | {addr_cbc} | {text}')
                        if inf.mail:
                            send_email(f'[F][BRAIN] Found address balance 0.0 PVK:{f1[co//2]} | HASH160:{res.hex()} | {addr_c} | {addr_cbc} | {text}')
                        if inf.telegram:
                            send_telegram(f'[F][BRAIN] Found address balance 0.0 PVK:{f1[co//2]} | HASH160:{res.hex()} | {addr_c} | {addr_cbc} | {text}')
                else:
                    print(f'\n[F][BRAIN] Found address PVK:{f1[co//2]} | HASH160:{res.hex()} | {addr_c} | {addr_cbc} | {text}')
                    logger_found.info(f'[F][BRAIN] Found address PVK:{f1[co//2]} | HASH160:{res.hex()} | {addr_c} | {addr_cbc} | {text}')
                    if inf.mail:
                        send_email(f'[F][BRAIN] Found address PVK:{f1[co//2]} | HASH160:{res.hex()} | {addr_c} | {addr_cbc} | {text}')
                    if inf.telegram:
                        send_telegram(f'[F][BRAIN] Found address PVK:{f1[co//2]} | HASH160:{res.hex()} | {addr_c} | {addr_cbc} | {text}')
                    fc.increment(1)
        co += 1
        co_count += 2
    return co_count

def get_balance(address,cyr):
    sleep(11) 
    if cyr == 'ETH':
        try:
            response = requests.get(inf.ETH_bal_server[1] + '0x' + address)
            return int(response.json()['result'])
        except:
            print('[E][ETH] NOT connect balance server')
            logger_err.error('[E][ETH] NOT connect balance server')
            return -1
    else:
        try:
            if inf.bal_srv_count == 0:
                response = requests.get(inf.bal_server[inf.bal_srv_count] + str(address))
                return int(response.json()['n_tx']), float(response.json()['balance'])
            elif inf.bal_srv_count == 1:
                response = requests.get(inf.bal_server[inf.bal_srv_count] + str(address))
                return int(response.json()['txApperances']), float(response.json()['balance'])
            elif inf.bal_srv_count == 2:
                response = requests.get(inf.bal_server[inf.bal_srv_count] + str(address))
                return int(response.json()['data']['total_txs']), float(response.json()['data']['balance'])
            elif inf.bal_srv_count == 3:
                response = requests.get(inf.bal_server[inf.bal_srv_count] + str(address))
                return int(response.json()['n_tx']), float(response.json()['final_balance'])
        except:
            logger_err.error('[E][BTC, 44, 32] NOT connect balance server')
            print('[E][BTC, 44, 32] NOT connect balance server')
            if inf.bal_err < 10:
                inf.bal_err += 1
            else:
                if inf.bal_srv_count < 3:
                    inf.bal_srv_count += 1
                else:
                    inf.bal_srv_count = 0
            inf.bal_all_err += 1
            if inf.bal_all_err == 40:
                inf.balance = False
            return -1

def load_BF(load):
    try:
        fp = open(load, 'rb')
    except FileNotFoundError:
        print(f'{red}[E] File: {load} not found.')
        logger_err.error(f'[E] File: {load} not found.')
        sys.exit()
    else:
        n_int = int(multiprocessing.current_process().name)
        sleep(inf.delay*n_int)
        return BloomFilter.load(fp)    

def send_email(text):
    subject = ''
    current_date = datetime.datetime.now()
    inf.dt_now = current_date.strftime('%m/%d/%y %H:%M:%S')
    text = str(inf.dt_now) + ' | ' + text
    subject = email.subject + ' description -> ' + email.desc
    BODY:str = '\r\n'.join(('From: %s' % email.from_addr, 'To: %s' % email.to_addr, 'Subject: %s' % subject, '', text)).encode('utf-8')
    try:
        server = smtplib.SMTP(email.host,email.port)
    except (smtplib.SMTPAuthenticationError) or (OSError,ConnectionRefusedError):
        print(f'{red} \n[E] could not connect to the mail server')
        logger_err.error('[E] could not connect to the mail server')
        inf.mail_err += 1
        if inf.mail_err >= 3:
            inf.mail = False
    except ConnectionRefusedError:
        print(f'{red} \n[E] could not connect to the mail server')
        logger_err.error('[E] could not connect to the mail server')
        inf.mail_err += 1
        if inf.mail_err >= 3:
            inf.mail = False
    else:
        try:
            server.login(email.from_addr, email.password)
        except (smtplib.SMTPAuthenticationError) or (OSError,ConnectionRefusedError):
            print(f'{red}\n[E] could not connect to the mail server')
            logger_err.error('[E] could not connect to the mail server')
            inf.mail_err += 1
            if inf.mail_err >= 3:
                inf.mail = False
        else:
            try:
                server.sendmail(email.from_addr, email.to_addr, BODY)
            except UnicodeError:
                print(f'{red}\n[E] Error Encode UTF-8')
                logger_err.error('[E] Error Encode UTF-8')
            else:
                server.quit()

def brnd(bip, fc):
    def rbtc(group_size,Pv):
        co = 0
        for tmp in range(group_size):
            #----------------------------------------------------------------    
            bip32_h160_cs = secp256k1_lib.pubkey_to_h160(1, True, Pv[tmp*65:tmp*65+65])
            bip32_h160_c = secp256k1_lib.pubkey_to_h160(0, True, Pv[tmp*65:tmp*65+65])
            bip32_h160_uc = secp256k1_lib.pubkey_to_h160(0, False, Pv[tmp*65:tmp*65+65])
            if inf.debug > 0:
                addr_c = secp256k1_lib.hash_to_address(0, False, bip32_h160_c)
                addr_uc = secp256k1_lib.hash_to_address(0, False, bip32_h160_uc)
                addr_cs = secp256k1_lib.hash_to_address(1, False, bip32_h160_cs)
                addr_cbc = secp256k1_lib.hash_to_address(2, False, bip32_h160_c)
                print(f'[D][Mode RND BTC] (PG:{tmp}) | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                print(f'[D][Mode RND BTC] {bip32_h160_uc.hex()} | {bip32_h160_c.hex()} | {bip32_h160_cs.hex()}')
                logger_dbg.debug(f'[D][Mode RND BTC] (PG:{tmp}) | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                logger_dbg.debug(f'[D][Mode RND BTC] {bip32_h160_uc.hex()} | {bip32_h160_c.hex()} | {bip32_h160_cs.hex()}')
            if (bip32_h160_c.hex() in inf.bf_btc) or (bip32_h160_uc.hex() in inf.bf_btc) or (bip32_h160_cs.hex() in inf.bf_btc):
                if inf.debug > 0:
                    if inf.telegram:
                        send_telegram(f'[D][F][Mode RND BTC] (PG:{tmp}) | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                    if inf.mail:
                        send_email(f'[D][F][Mode RND BTC] (PG:{tmp}) | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                    print(f'[D][F][Mode RND BTC] (PG:{tmp}) | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                    logger_found.info(f'[D][F][Mode RND BTC] (PG:{tmp}) | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                    logger_dbg.debug(f'[D][Mode RND BTC] {bip32_h160_uc.hex()} | {bip32_h160_c.hex()}, {bip32_h160_cs.hex()}')
                if inf.debug < 1:
                    addr_c = secp256k1_lib.hash_to_address(0, False, bip32_h160_c)
                    addr_uc = secp256k1_lib.hash_to_address(0, False, bip32_h160_uc)
                    addr_cs = secp256k1_lib.hash_to_address(1, False, bip32_h160_cs)
                    addr_cbc = secp256k1_lib.hash_to_address(2, False, bip32_h160_c)
                    if inf.balance:
                        tx1, b1 = get_balance(addr_c,'BTC')
                        tx2, b2 = get_balance(addr_uc,'BTC')
                        tx3, b3 = get_balance(addr_cs,'BTC')
                        tx4, b4 = get_balance(addr_cbc,'BTC')
                        if (tx1 > 0) or (tx2 > 0) or (tx3 > 0) or (tx4 > 0):
                            print(f'\n[F][Mode RND BTC] Found transaction! (PG:{tmp}) | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                            logger_found.info(f'[F][Mode RND BTC] Found transaction! (PG:{tmp}) | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                        if (b1 > 0) or (b2 > 0) or (b3 > 0) or (b4 > 0):
                            print(f'\n[F][Mode RND BTC] Found address in balance! (PG:{tmp}) | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                            logger_found.info(f'[F][Mode RND BTC] Found address in balance! (PG:{tmp}) | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                            if inf.telegram:
                                send_telegram(f'[F][Mode RND BTC] (PG:{tmp}) | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')    
                            if inf.mail:
                                send_email(f'[F][Mode RND BTC] (PG:{tmp}) | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')    
                            fc.increment(1)
                        else:
                            print(f'\n[F][Mode RND BTC] Found address balance 0.0 (PG:{tmp}) | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                            logger_found.info(f'[F][Mode RND BTC] Found address balance 0.0 (PG:{tmp}) | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                            if inf.telegram:
                                send_telegram(f'[F][Mode RND BTC] Found address balance 0.0 (PG:{tmp}) | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                            if inf.mail:
                                send_email(f'[F][Mode RND BTC] Found address balance 0.0 (PG:{tmp}) | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                    else:
                        print(f'\n[F][Mode RND BTC] Found address (PG:{tmp}) | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                        logger_found.info(f'[F][Mode RND BTC] Found address (PG:{tmp}) | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                        if inf.telegram:
                            send_telegram(f'[F][Mode RND BTC] Found address (PG:{tmp}) | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                        if inf.mail:
                            send_email(f'[F][Mode RND BTC] Found address (PG:{tmp}) | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                        fc.increment(1)
            co += 3
        return co
    def reth(group_size,Pv):
        co = 0
        for t in range(group_size):
            addr = secp256k1_lib.pubkey_to_ETH_address(Pv[t*65:t*65+65])
            if inf.debug > 0:
                print(f'[D][Mode RND ETH] (PG:{t}) | PVK:{hex(current_pvk+t)[2:]} | addr:0x{addr}')
                logger_dbg.debug(f'[D][Mode RND ETH] (PG:{t}) | PVK:{hex(current_pvk+t)[2:]} | addr:0x{addr}')
            if addr in inf.bf_eth:
                if inf.debug > 0:
                    print(f'[D][F][Mode RND ETH] (PG:{t}) | PVK:{hex(current_pvk+t)[2:]} | addr:0x{addr}')
                    logger_found.info(f'[D][F][Mode RND ETH] (PG:{t}) | PVK:{hex(current_pvk+t)[2:]} | addr:0x{addr}')
                if inf.debug < 1:
                    if inf.balance:
                        b1 = get_balance(addr,'ETH')
                        if (b1 > 0):
                            print(f'[F][Mode RND ETH] Found address in balance! (PG:{t}) | PVK:{hex(current_pvk+t)[2:]} | addr:0x{addr}')
                            logger_found.info(f'[F][Mode RND ETH] Found address in balance! (PG:{t}) | PVK:{hex(current_pvk+t)[2:]} | addr:0x{addr}')
                            if inf.telegram:
                                send_telegram(f'[F][Mode RND ETH] Found address in balance! (PG:{t}) | PVK:{hex(current_pvk+t)[2:]} | addr:0x{addr}')
                            if inf.mail:
                                send_email(f'[F][Mode RND ETH] Found address in balance! (PG:{t}) | PVK:{hex(current_pvk+t)[2:]} | addr:0x{addr}')
                            fc.increment(1)
                        else:
                            print(f'\n[F][Mode RND ETH] Found address balance 0.0: (PG:{t}) | PVK:{hex(current_pvk+t)[2:]} | addr:0x{addr}')
                            logger_found.info(f'[F][Mode RND ETH] Found address balance 0.0 (PG:{t}) | PVK:{hex(current_pvk+t)[2:]} | addr:0x{addr}')
                            if inf.telegram:
                                send_telegram(f'[F][Mode RND ETH] Found address balance 0.0 (PG:{t}) | PVK:{hex(current_pvk+t)[2:]} | addr:0x{addr}')
                            if inf.mail:
                                send_email(f'[F][Mode RND ETH] Found address balance 0.0 (PG:{t}) | PVK:{hex(current_pvk+t)[2:]} | addr:0x{addr}')
                    else:
                        print(f'\n[F][Mode RND ETH] (PG:{t}) | PVK:{hex(current_pvk+t)[2:]} | addr:0x{addr}')
                        logger_found.info(f'[F][Mode RND ETH] (PG:{t}) | PVK:{hex(current_pvk+t)[2:]} | addr:0x{addr}')
                        if inf.telegram:
                            send_telegram(f'[F][Mode RND ETH] (PG:{t}) | PVK:{hex(current_pvk+t)[2:]} | addr:0x{addr}')
                        if inf.mail:
                            send_email(f'[F][Mode RND ETH] (PG:{t}) | PVK:{hex(current_pvk+t)[2:]} | addr:0x{addr}')
                        fc.increment(1)
            co += 1
        return co

    group_size = 15000
    pvk_int = generate_private_key()
    P = secp256k1_lib.scalar_multiplication(pvk_int)
    current_pvk = pvk_int + 1
    Pv = secp256k1_lib.point_sequential_increment(group_size, P)
    if bip == 'btc':
        res = rbtc(group_size,Pv)
        return res
    else:
        res = reth(group_size,Pv)
        return res


def b32(mnem, seed, fc):
    co = 0
    group_size = 100
    bip32 = BIP32.from_seed(seed)
    for path in inf.l32:
        for num1 in range(1):
            for t in inf.l32_:
                for num2 in range(20):
                    for t1 in inf.l32_:
                        patchs = f"{path}{num1}{t}/{num2}{t1}"
                        pvk = bip32.get_privkey_from_path(patchs)
                        pvk_int = int(pvk.hex(),16)
                        pvk_int = pvk_int - 1
                        P = secp256k1_lib.scalar_multiplication(pvk_int)
                        current_pvk = pvk_int + 1
                        Pv = secp256k1_lib.point_sequential_increment(group_size, P)
                        for tmp in range(group_size):
                        #----------------------------------------------------------------    
                            bip32_h160_cs = secp256k1_lib.pubkey_to_h160(1, True, Pv[tmp*65:tmp*65+65])
                            bip32_h160_c = secp256k1_lib.pubkey_to_h160(0, True, Pv[tmp*65:tmp*65+65])
                            bip32_h160_uc = secp256k1_lib.pubkey_to_h160(0, False, Pv[tmp*65:tmp*65+65])
                            if inf.debug > 0:
                                addr_c = secp256k1_lib.hash_to_address(0, False, bip32_h160_c)
                                addr_uc = secp256k1_lib.hash_to_address(0, False, bip32_h160_uc)
                                addr_cs = secp256k1_lib.hash_to_address(1, False, bip32_h160_cs)
                                addr_cbc = secp256k1_lib.hash_to_address(2, False, bip32_h160_c)
                                print(f'[D][Mode 32] {patchs}(PG:{tmp}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                                print(f'[D][Mode 32] {bip32_h160_uc.hex()} | {bip32_h160_c.hex()} | {bip32_h160_cs.hex()}')
                                logger_dbg.debug(f'[D][Mode 32] {patchs}(PG:{tmp}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                                logger_dbg.debug(f'[D][Mode 32] {bip32_h160_uc.hex()} | {bip32_h160_c.hex()} | {bip32_h160_cs.hex()}')
                            if (bip32_h160_c.hex() in inf.bf_btc) or (bip32_h160_uc.hex() in inf.bf_btc) or (bip32_h160_cs.hex() in inf.bf_btc):
                                if inf.debug > 0:
                                    if inf.telegram:
                                        send_telegram(f'[D][F][Mode 32] {patchs}(PG:{tmp}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                                    if inf.mail:
                                        send_email(f'[D][F][Mode 32] {patchs}(PG:{tmp}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                                    print(f'[D][F][Mode 32] {patchs}(PG:{tmp}) | {seed.hex()} | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                                    logger_found.info(f'[D][F][Mode 32] {patchs}(PG:{tmp}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                                    logger_dbg.debug(f'[D][Mode 32] {bip32_h160_uc.hex()} | {bip32_h160_c.hex()}, {bip32_h160_cs.hex()}')
                                if inf.debug < 1:
                                    addr_c = secp256k1_lib.hash_to_address(0, False, bip32_h160_c)
                                    addr_uc = secp256k1_lib.hash_to_address(0, False, bip32_h160_uc)
                                    addr_cs = secp256k1_lib.hash_to_address(1, False, bip32_h160_cs)
                                    addr_cbc = secp256k1_lib.hash_to_address(2, False, bip32_h160_c)
                                    if inf.balance:
                                        tx1, b1 = get_balance(addr_c,'BTC')
                                        tx2, b2 = get_balance(addr_uc,'BTC')
                                        tx3, b3 = get_balance(addr_cs,'BTC')
                                        tx4, b4 = get_balance(addr_cbc,'BTC')
                                        if (tx1 > 0) or (tx2 > 0) or (tx3 > 0) or (tx4 > 0):
                                            print(f'\n[F][Mode 32] Found transaction! {patchs}(PG:{tmp}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                                            logger_found.info(f'[F][Mode 32] Found transaction! {patchs}(PG:{tmp}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                                        if (b1 > 0) or (b2 > 0) or (b3 > 0) or (b4 > 0):
                                            print(f'\n[F][Mode 32] Found address in balance! {patchs}(PG:{tmp}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                                            logger_found.info(f'[F][Mode 32] Found address in balance! {patchs}(PG:{tmp}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                                            if inf.telegram:
                                                send_telegram(f'[F][Mode 32] {patchs}(PG:{tmp}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')    
                                            if inf.mail:
                                                send_email(f'[F][Mode 32] {patchs}(PG:{tmp}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')    
                                            fc.increment(1)
                                        else:
                                            print(f'\n[F][Mode 32] Found address balance 0.0 {patchs}(PG:{tmp}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                                            logger_found.info(f'[F][Mode 32] Found address balance 0.0 {patchs}(PG:{tmp}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                                            if inf.telegram:
                                                send_telegram(f'[F][Mode 32] Found address balance 0.0 {patchs}(PG:{tmp}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                                            if inf.mail:
                                                send_email(f'[F][Mode 32] Found address balance 0.0 {patchs}(PG:{tmp}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                                    else:
                                        print(f'\n[F][Mode 32] Found address {patchs}(PG:{tmp}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                                        logger_found.info(f'[F][Mode 32] Found address {patchs}(PG:{tmp}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                                        if inf.telegram:
                                            send_telegram(f'[F][Mode 32] Found address {patchs}(PG:{tmp}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                                        if inf.mail:
                                            send_email(f'[F][Mode 32] Found address {patchs}(PG:{tmp}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                                        fc.increment(1)
                            co += 3
    return co

def bETH(mnem, seed, fc):
    co = 0
    group_size = 150
    w = BIP32.from_seed(seed)
    for bi in range(2):
        for p in inf.leth:
            for nom2 in range(1):#accaunt
                for nom3 in range(2):#in/out
                    for nom in range(20):
                        if bi == 0:
                            patchs = f"m/44'/{p}'/{nom2}'/{nom3}/{nom}"
                        elif bi == 1:
                            patchs = f"m/44'/{p}'/{nom3}'/{nom}"
                        pvk = w.get_privkey_from_path(patchs)
                        pvk_int = int(pvk.hex(),16)
                        pvk_int = pvk_int - 1
                        P = secp256k1_lib.scalar_multiplication(pvk_int)
                        Pv = secp256k1_lib.point_sequential_increment(group_size, P)
                        current_pvk = pvk_int + 1
                        for t in range(group_size):
                            addr = secp256k1_lib.pubkey_to_ETH_address(Pv[t*65:t*65+65])
                            if inf.debug > 0:
                                print(f'[D][Mode ETH] {patchs}(PG:{t}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+t)[2:]} | addr:0x{addr}')
                                logger_dbg.debug(f'[D][Mode ETH] {patchs}(PG:{t}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+t)[2:]} | addr:0x{addr}')
                            if addr in inf.bf_eth:
                                if inf.debug > 0:
                                    print(f'[D][F][Mode ETH] {patchs}(PG:{t}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+t)[2:]} | addr:0x{addr}')
                                    logger_found.info(f'[D][F][Mode ETH] {patchs}(PG:{t}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+t)[2:]} | addr:0x{addr}')
                                if inf.debug < 1:
                                    if inf.balance:
                                        b1 = get_balance(addr,'ETH')
                                        if (b1 > 0):
                                            print(f'[F][Mode ETH] Found address in balance! {patchs}(PG:{t}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+t)[2:]} | addr:0x{addr}')
                                            logger_found.info(f'[F][Mode ETH] Found address in balance! {patchs}(PG:{t}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+t)[2:]} | addr:0x{addr}')
                                            if inf.telegram:
                                                send_telegram(f'[F][Mode ETH] Found address in balance! {patchs}(PG:{t}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+t)[2:]} | addr:0x{addr}')
                                            if inf.mail:
                                                send_email(f'[F][Mode ETH] Found address in balance! {patchs}(PG:{t}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+t)[2:]} | addr:0x{addr}')
                                            fc.increment(1)
                                        else:
                                            print(f'\n[F][Mode ETH] Found address balance 0.0: {patchs}(PG:{t}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+t)[2:]} | addr:0x{addr}')
                                            logger_found.info(f'[F][Mode ETH] Found address balance 0.0 {patchs}(PG:{t}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+t)[2:]} | addr:0x{addr}')
                                            if inf.telegram:
                                                send_telegram(f'[F][Mode ETH] Found address balance 0.0 {patchs}(PG:{t}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+t)[2:]} | addr:0x{addr}')
                                            if inf.mail:
                                                send_email(f'[F][Mode ETH] Found address balance 0.0 {patchs}(PG:{t})  {mnem} | {seed.hex()} || PVK:{hex(current_pvk+t)[2:]} | addr:0x{addr}')
                                    else:
                                        print(f'\n[F][Mode ETH] {patchs}(PG:{t}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+t)[2:]} | addr:0x{addr}')
                                        logger_found.info(f'[F][Mode ETH] {patchs}(PG:{t}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+t)[2:]} | addr:0x{addr}')
                                        if inf.telegram:
                                            send_telegram(f'[F][Mode ETH] {patchs}(PG:{t}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+t)[2:]} | addr:0x{addr}')
                                        if inf.mail:
                                            send_email(f'[F][Mode ETH] {patchs}(PG:{t}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+t)[2:]} | addr:0x{addr}')
                                        fc.increment(1)
                            co += 1
    return co

def b44(mnem, seed, fc):
    co = 0
    group_size = 100
    w = BIP32.from_seed(seed)
    for p in inf.l44:
        for nom2 in range(1):#accaunt
            for nom3 in range(2):#in/out
                for nom in range(20):
                    patchs = f"m/44'/{p}'/{nom2}'/{nom3}/{nom}"
                    pvk = w.get_privkey_from_path(patchs)
                    pvk_int = int(pvk.hex(),16)
                    pvk_int = pvk_int - 1
                    P = secp256k1_lib.scalar_multiplication(pvk_int)
                    current_pvk = pvk_int + 1
                    Pv = secp256k1_lib.point_sequential_increment(group_size, P)
                    for tmp in range(group_size):
                        bip44_h160_cs = secp256k1_lib.pubkey_to_h160(1, True, Pv[tmp*65:tmp*65+65])
                        bip44_h160_c = secp256k1_lib.pubkey_to_h160(0, True, Pv[tmp*65:tmp*65+65])
                        bip44_h160_uc = secp256k1_lib.pubkey_to_h160(0, False, Pv[tmp*65:tmp*65+65])  
                        if inf.debug > 0 :
                                logger_dbg.debug(f'[D][P:{multiprocessing.current_process().name}] {patchs} | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+tmp)[2:]} | HASH160:{bip44_h160_c.hex()} | HASH160:{bip44_h160_uc.hex()} | HASH160:{bip44_h160_cs.hex()}')
                                print(f'\n[D] {patchs} | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+tmp)[2:]} | HASH160:{bip44_h160_c.hex()} | HASH160:{bip44_h160_uc.hex()} | HASH160:{bip44_h160_cs.hex()}')
                        if (bip44_h160_c.hex() in inf.bf_btc) or (bip44_h160_uc.hex() in inf.bf_btc) or (bip44_h160_cs.hex() in inf.bf_btc):
                            if inf.debug > 0:
                                logger_found.info(f'[D][F][P:{multiprocessing.current_process().name}] {patchs} | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+tmp)[2:]} | HASH160:{bip44_h160_c.hex()} | HASH160:{bip44_h160_uc.hex()} | HASH160:{bip44_h160_cs.hex()}')
                            if inf.debug < 1:
                                print(f'\n[F][Mode 44 BTC] {patchs} | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+tmp)[2:]} | HASH160:{bip44_h160_c.hex()} | HASH160:{bip44_h160_uc.hex()} | HASH160:{bip44_h160_cs.hex()}')
                                logger_found.info(f'[F][Mode 44 BTC] {patchs} | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+tmp)[2:]} | HASH160:{bip44_h160_c.hex()} | HASH160:{bip44_h160_uc.hex()} | HASH160:{bip44_h160_cs.hex()}')
                                if inf.telegram:
                                    send_telegram(f'[F][Mode 44 BTC] {patchs} | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+tmp)[2:]} | HASH160:{bip44_h160_c.hex()} | HASH160:{bip44_h160_uc.hex()} | HASH160:{bip44_h160_cs.hex()}')
                                if inf.mail:
                                    send_email(f'[F][Mode 44 BTC] {patchs} | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+tmp)[2:]} | HASH160:{bip44_h160_c.hex()} | HASH160:{bip44_h160_uc.hex()} | HASH160:{bip44_h160_cs.hex()}')
                                fc.increment(1)
                        co += 3
    return co

def bBTC(mnem, seed, fc):
    co = 0
    group_size = 100
    w = BIP32.from_seed(seed)
    for bip_ in inf.lbtc:
        for nom2 in range(1):
            for nom3 in range(2):
                for nom in range(20):
                    patchs = f"m/{bip_}'/0'/{nom2}'/{nom3}/{nom}"
                    pvk = w.get_privkey_from_path(patchs)
                    pvk_int = int(pvk.hex(),16)
                    pvk_int = pvk_int - 1
                    P = secp256k1_lib.scalar_multiplication(pvk_int)
                    current_pvk = pvk_int + 1
                    Pv = secp256k1_lib.point_sequential_increment(group_size, P)
                    for tmp in range(group_size):
                        bip44_h160_cs = secp256k1_lib.pubkey_to_h160(1, True, Pv[tmp*65:tmp*65+65])
                        bip44_h160_c = secp256k1_lib.pubkey_to_h160(0, True, Pv[tmp*65:tmp*65+65])
                        bip44_h160_uc = secp256k1_lib.pubkey_to_h160(0, False, Pv[tmp*65:tmp*65+65])                        
                        if inf.debug > 0:
                        #----------------------------------------------------------------    
                            addr_c = secp256k1_lib.hash_to_address(0, False, bip44_h160_c)
                            addr_uc = secp256k1_lib.hash_to_address(0, False, bip44_h160_uc)
                            addr_cs = secp256k1_lib.hash_to_address(1, False, bip44_h160_cs)
                            addr_cbc = secp256k1_lib.hash_to_address(2, False, bip44_h160_c)
                            print(f'\n[D][Mode BTC] {patchs}(PG:{tmp}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                            print(f'[D][Mode BTC] {bip_,bip44_h160_c.hex()} | {bip44_h160_uc.hex()} | {bip_,bip44_h160_cs.hex()}')
                            logger_dbg.debug(f'[D][Mode BTC][P:{multiprocessing.current_process().name}] {patchs}(PG:{tmp}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                            logger_dbg.debug(f'[D][Mode BTC] {bip_,bip44_h160_c.hex()} | {bip44_h160_uc.hex()} | {bip_,bip44_h160_cs.hex()}')
                        if (bip44_h160_c.hex() in inf.bf_btc) or (bip44_h160_uc.hex() in inf.bf_btc) or (bip44_h160_cs.hex() in inf.bf_btc):
                            if inf.debug > 0:
                                if inf.telegram:
                                    send_telegram(f'[D][F][Mode BTC] {patchs}(PG:{tmp}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                                if inf.mail:
                                    send_email(f'[D][F][Mode BTC] {patchs}(PG:{tmp}) | | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                                print(f'[D][F][Mode BTC][P:{multiprocessing.current_process().name}] {patchs}(PG:{tmp}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                                logger_found.info(f'[D][F][Mode BTC][P:{multiprocessing.current_process().name}] {patchs}(PG:{tmp}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                            if inf.debug < 1:
                                addr_c = secp256k1_lib.hash_to_address(0, False, bip44_h160_c)
                                addr_uc = secp256k1_lib.hash_to_address(0, False, bip44_h160_uc)
                                addr_cs = secp256k1_lib.hash_to_address(1, False, bip44_h160_cs)
                                addr_cbc = secp256k1_lib.hash_to_address(2, False, bip44_h160_c)
                                if inf.balance:
                                    tx1, b1 = get_balance(addr_c,'BTC')
                                    tx2, b2 = get_balance(addr_uc,'BTC')
                                    tx3, b3 = get_balance(addr_cs,'BTC')
                                    tx4, b4 = get_balance(addr_cbc,'BTC')
                                    if (tx1 > 0) or (tx2 > 0) or (tx3 > 0) or (tx4 > 0):
                                        print(f'[F][Mode BTC] Found transaction! {patchs}(PG:{tmp}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                                        logger_found.info(f'[F][Mode BTC] Found transaction! {patchs}(PG:{tmp}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                                    if (b1 > 0) or (b2 > 0) or (b3 > 0) or (b4 > 0):
                                        print(f'\n[F][Mode BTC] Found balance! {patchs}(PG:{tmp}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                                        logger_found.info(f'[F][Mode BTC] Found balance! {patchs}(PG:{tmp}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                                        if inf.telegram:
                                            send_telegram(f'[F][Mode BTC] {patchs}(PG:{tmp}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                                        if inf.mail:
                                            send_email(f'[F][Mode BTC] Found balance! {patchs}(PG:{tmp}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')    
                                        fc.increment(1)
                                    else:
                                        print(f'\n[F False][Mode BTC] Found address balance 0.0  {patchs}(PG:{tmp}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                                        logger_found.info(f'[F False][Mode BTC] Found address balance 0.0 {patchs} | {patchs}(PG:{tmp}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                                        if inf.telegram:
                                            send_telegram(f'[F][Mode BTC] {patchs}(PG:{tmp}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                                        if inf.mail:
                                            send_email(f'[F False][Mode BTC] Found address balance 0.0 {patchs}(PG:{tmp}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                                else:
                                    print(f'\n[F][Mode BTC] {patchs}(PG:{tmp}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                                    logger_found.info(f'[F][Mode BTC] {patchs}(PG:{tmp}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                                    if inf.telegram:
                                        send_telegram(f'[F][Mode BTC] {patchs}(PG:{tmp}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                                    if inf.mail:
                                        send_email(f'[F][Mode BTC] {patchs}(PG:{tmp}) | {mnem} | {seed.hex()} | PVK:{hex(current_pvk+tmp)[2:]} | {addr_c} | {addr_uc} | {addr_cs} | {addr_cbc}')
                                    fc.increment(1)
                        co += 3
    return co

def nnmnem(mem):
    if inf.mode == 'e':
        mnemo:Mnemonic = Mnemonic(mem)
        if inf.bit == 128: bit = 16
        if inf.bit == 160: bit = 20
        if inf.bit == 192: bit = 24
        if inf.bit == 224: bit = 28
        if inf.bit == 256: bit = 32
        ran = secrets.token_hex(bit)
        mnemonic = mnemo.to_mnemonic(bytes.fromhex(ran))
        seed_bytes = mnemo.to_seed(mnemonic, passphrase='')
    elif inf.mode =='g':
        mnemonic = ''
        mnemo:Mnemonic = Mnemonic(mem)
        rw = randint(1,25)
        mnemonic = ' '.join(choice(inf.game_list) for i in range(rw))
        seed_bytes:bytes = mnemo.to_seed(mnemonic, passphrase='')
    elif inf.mode =='c':
        mnemonic = ''
        mnemo:Mnemonic = Mnemonic(mem)
        rw = inf.custom_words
        mnemonic = ' '.join(choice(inf.custom_list) for i in range(rw))
        seed_bytes:bytes = mnemo.to_seed(mnemonic, passphrase='')
    else:
        mnemo:Mnemonic = Mnemonic(mem)
        mnemonic:str = mnemo.generate(strength=inf.bit)
        seed_bytes:bytes = mnemo.to_seed(mnemonic, passphrase='')
 
    if inf.debug==1:
        mnemo = Mnemonic('english')
        mnemonic = 'world evolve cry outer garden common differ jump few diet cliff lumber'
        seed_bytes:bytes = mnemo.to_seed(mnemonic, passphrase='')
        print(f'Debug Mnemonic : {mnemonic}')
        print(f'Debug SEED : {seed_bytes.hex()}')
        logger_dbg.debug(f'[D] Debug Mnemonic : {mnemonic}')
        logger_dbg.debug(f'[D] Debug SEED : {seed_bytes.hex()}')
    if inf.debug==2:
        print('Debug Mnemonic : '+ mnemonic)
        print(f'Debug SEED : {seed_bytes.hex()}')
        logger_dbg.debug(f'[D] Debug Mnemonic : {mnemonic}')
        logger_dbg.debug(f'[D] Debug SEED : {seed_bytes.hex()}')
        
    if inf.mode == 'e' : return mnemonic, seed_bytes , ran
    else: return mnemonic, seed_bytes

def test():
    try:
        requests.get('https://api.telegram.org/bot{}/sendMessage'.format(telegram.token), params=dict(
        chat_id=telegram.channel_id,
        text=f'Сommunication check. HUNT-to-mnemonic ver.{inf.version}. run client {email.desc}'
        ))
    except:
        print(f'{red} check your internet connection, could not send message to telegram')
        logger_err.error(f'check your internet connection, could not send message to telegram')
        
    print('-'*70,end='\n')
    print('DEPENDENCY TESTING:')
    if platform.system().lower().startswith('win'):
        dllfile = 'ice_secp256k1.dll'
        if os.path.isfile(dllfile) == True:
            pass
        else:
            print(f'{red} File {dllfile} not found')
            logger_err.error(f'File {dllfile} not found')
            
            
    elif platform.system().lower().startswith('lin'):
        dllfile = 'ice_secp256k1.so'
        if os.path.isfile(dllfile) == True:
            pass
        else:
            print(f'{red} File {dllfile} not found')
            logger_err.error(f'File {dllfile} not found')
    else:
        print(f'{red} * Unsupported Platform currently for ctypes dll method. Only [Windows and Linux] is working')
        logger_err.error(f'* Unsupported Platform currently for ctypes dll method. Only [Windows and Linux] is working')
        
        exit
    mnemo:Mnemonic = Mnemonic('english')
    mnemonic = 'world evolve cry outer garden common differ jump few diet cliff lumber'
    seed_bytes:bytes = mnemo.to_seed(mnemonic, passphrase='')
    if seed_bytes.hex() !='bd85556143de177ed9781ac3b24ba33d0bc4f8d6f34d9eaa1d9b8ab0ee3a7e84d42638b520043234bcedb4e869464b9f964e7e8dbf1588395f7a7782588ae664':
        print(f'{red} ERROR: Generate mnemonic')
        print(f'{red} Please reinstall https://github.com/trezor/python-mnemonic')
        logger_err.error(f'ERROR: Generate mnemonic')
        logger_err.error(f'Please reinstall https://github.com/trezor/python-mnemonic')
        exit
    bip32 = BIP32.from_seed(seed_bytes)
    patchs = "m/0'/0'/0"
    pvk = bip32.get_privkey_from_path(patchs)
    pvk_int = int(pvk.hex(),16)
    bip_hash_c = secp256k1_lib.privatekey_to_h160(0,True,pvk_int)
    bip_hash_uc = secp256k1_lib.privatekey_to_h160(0,False,pvk_int)
    addr_c = secp256k1_lib.hash_to_address(0,True,bip_hash_c)
    addr_uc = secp256k1_lib.hash_to_address(0,False,bip_hash_uc)
    if (addr_c != '1JiG9xbyAPNfX8p4M6qxE6PwyibnqARkuq') or (addr_uc != '1EHciAwg1thir7Gvj5cbrsyf3JQbxHmWMW'):
        print(f'{red} ERROR: Convert address from mnemonic')
        print(f'{red} Please recopy https://github.com/iceland2k14/secp256k1')
        logger_err.error(f'ERROR: Convert address from mnemonic')
        logger_err.error(f'Please recopy https://github.com/iceland2k14/secp256k1')
        exit
    return True