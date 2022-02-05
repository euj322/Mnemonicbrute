#### Огромное спасибо iceland2k14 за его работу

#### Изменения от 30.01.22!
    Добавлен в режим ETH поддержка генерации адресов BIP32
    В режим -rnd добавлена поддержка случайного поиска ETH
#### Изменения от 29.01.22!
    Добавлен режим Random (-rnd). генерируется случайный ключ и от него последовательно проверяются 15000 приватников. (на скорость почти не влияет)
#### Изменения от 18.01.22!
    Код переведен полностью на систему логирования
    Изменены режимы поиска, смотрите внимательно описание
    Добавлен поиск по BrainWallet. (-brain) Проверяется генерированая мнемоника и seed, а также их перевернутые значения.
    Добавлена поддержка отправки сообщений в телеграм
    Добавлен новый режим -combo (использовать только тем у кого достаточно памяти.) ведет поиск одновременно по ETH и BTC


#### Ресурсы для проверки работы
  для проверки пользуюсь ресурсами:
  https://iancoleman.io/bip39/  
  https://kriptokurs.ru/bitcointools/tool/hash-to-address    

  Описание как это работает:
  https://learnmeabitcoin.com/technical/derivation-paths

#### HUNT to MNEMONIC (HASH160)
Brute Force crypto address
Программа создана в первую очередь для изучения языка PYTHON!

Что реализовано:  
#### создание BIP39 Mnemonic для 10 языков. Возможно использовать все сразу или какие-то отдельно 
    -english
    -chinese_simplified
    -chinese_traditional
    -french
    -italian
    -spanish
    -czech
    -korean
    -japanese
    -portuguese
    (список языков редактируйте в файле consts.py)
        mnemonic_lang:list = ['english','chinese_simplified'] # ['english', 'chinese_simplified', 'chinese_traditional', 'french', 'italian', 'spanish', 'korean','japanese','portuguese','czech']
    Все возможные комбинации мнемоник. если надо больше вложений, аккаунтов и т.д. несложно добавить.
    4 случайных режима
        s - Стандартный режим. Он создает мнемоник согласно спецификации BIP39
        e - режим генерации энтропии случайным образом и из нее создается мнемоническая фраза
        g - это режим для веселухи Ж-) в папке лежит файл game_en.txt в нем 3000 самых используемых английских слов, программа случайным образом выбирает количество слов от 1 до 25 и затем случайно выбирает слова
            вы можете заменить слова на свои.
        c - режим для самостоятельных переборов и словарей
    4 варианта поиска (BIP32, BIP44, ETH, BTC)
        - Режим BTC ищет только по BTC но во всех вариациях (BIP32, BIP44, BIP49)
        - Режим 44 создан для поиска по всем кошелькам (исключение это ETH и его производные)
        Режим BIP84 и выше делать не буду, этими кошельками пользуются люди.

### для установки на windows необходимо установить Microsoft build tools

установочный файл находится в папке install
![install](https://github.com/Noname400/Hunt-to-Mnemonic/blob/main/image/inst1.jpg)
![install](https://github.com/Noname400/Hunt-to-Mnemonic/blob/main/image/inst2.jpg)
также в папке лежит уже готовый файл конфигурации
как добавить его на фото выше

#### Установка:
    pip install simplebloomfilter
    pip install bitarray==1.9.2
    Кто пользовался и ранее моей программой нужно сначало удалить:
        pip uninstall mnemonic
    pip install mnemonic
    pip install colorama
    pip install bip32
    pip install bitcoinlib
    pip install requests
    pip install bitcoin

для установки на windows необходимо установить Microsoft build tools

#### Создаем HASH160 из Адресов:
    создание HASH160 требуется для всех адресов КРОМЕ ETH и ETC. адреса ETH и ETC сразу конверируются в блюм фильтр, без дополнительной конвертиции
    python addr_to_h160.py <in file> <out file>
      in file - текстовый файл с адресами (один адрес на одну срочку)  
      out file - файл hash160  

#### Создайте BloobFilter (BF create\Cbloom.py)
    ПОМНИТЕ: адреса ETH и ETC и прочии производные должны быть без '0x'
        0x0284A72A0fe8fCC4867fbeA622D862E4a28d0DB7 такой адрес не корректен. нужен 0284A72A0fe8fCC4867fbeA622D862E4a28d0DB7
        на сайте https://gz.blockchair.com/ethereum/addresses/ как раз адреса без '0x' и вы можете их преобразовать сразу в блюм
    python create_bloom.py <in file> <out file>  
      in file - текстовый файл с hash160 (один hash на одну срочку)  
      out file - файл блюм фильтра  
  
#### Работа со списком слов   
    Сейчас реализовано работа со словами (12, 15, 18, 21, 24) 
    в битах количество слов 128, 160, 192, 224, 256 (-bit)
    например надо искать по 12 словам (-bit 128)
  
#### Ключи использования  (Проверьте свои БАТНИКИ, аргументы для запуска изменились)
    python -B PulsarMTv5.py -b BTC -db BF\btc.bf -th 3 -des source -m s -bit 128 -sl 5 -em -bal
  
    -b Режим поиска (BIP32, BIP44, ETH, BTC, combo)  (-b BTC)
    -dbbtc расположение файла ФлюмФильтра для BTC (-db BF/work.bf)
    -dbeth расположение файла ФлюмФильтра для ETH (-db BF/eth.bf)
    -th количество процесов запущеных для поиска (-th 2)
    -des описание вашей машины. Чаще всего нужно при отправке почты, если нашелся адрес. если у вас работает только одна машина на поиск то параметр можно не указывать (-des locale)
    -m режим формирования мнемоники (-m s, e, c, g) выбор за вами . (-m e)
        Режим 's' - стандартный режим по спецификации BIP39
        Режим 'e' - генерируется энтропия а из нее мнемоника.
        Режим 'c' - пользовательский режим, читайте ниже
        Режим 'g' - игровой режим. в папке wl лежит файл game.txt (можете заменить на свой) из него формируется фраза со случайными словами и случайным количеством слов.
    -bit битность мнемоники (12 слов это 128 бит) смотрите выше "Работа со списком слов" (-bit 128)
    -em контроль отправки электроной почты при нахождении мнемоники (-em) (незабудьте указать настройки в файле consts.py)
    -sl задержка по пуску блюм фильтра (у кого много ядер, рекомендую!) (-sl 5)
    -bal проверка баланса при нахождении. если балан 0 то рескан не делается (-bal)
    -brain включение функции BRAINWALLET (вычесление приватного ключа из мнемоника и сида в разных интерпритациях). В режиме ETH поиск по BRAIWALLET не будет работат.
    -telegram включение функции отправки сообщения о нахождении ключа в телеграм (-telegram) (незабудьте указать настройки в файле consts.py)
    -rnd включает режим генерации случайного ключа. Генерируется случайный ключ и от него последовательно проверяются 15000 приватников. (на скорость почти не влияет)
    -dbg это отладочная информация, при указании данного параметра программа будет показывать что и как она формирует, можно будет проверить по ссылкам выше. режима 2 (-dbg 0,1,2)
         Режим 1: вам скорее всего не пригодится так как вы не добавили в свою базу отладочные адреса (если хотите я их вам дам)
         Режим 2: этот режим отображает всю информацию которая генерируется программой. Нужна для того что бы проверить правильно ли генерируются адреса.
    Режим пользовательских словарей:
    -m custom выбор режим пользовательского словаря (-m c)
    -cd путь до пользовательского файла (-cd DB/my.txt)
    -cw количество слов для генерации (-cw 6)
    -cl язык словаря (-cl english) (english,chinese_simplified,chinese_traditional,french,italian,spanish,czech,korean,japanese,portuguese)
    Обычный режим:
    python -B PulsarMTv5.py -b BTC -db BF\btc_without_0.bf -th 1 -des test -m s -bit 128 -sl 5 -dbg 0 -em -bal
    Режим пользователя:
    python -B PulsarMTv5.py -b BTC -db BF\btc_without_0.bf -th 1 -des test -m c -cd wl\custom.txt -cw 6 -cl english -sl 5 -dbg 0 -em -bal


    
#### Не забудьте настроить параметры своей почты для отправки найденных мнемоник  
    host:str = 'smtp.mail.ru'  
    port:int = 25  
    password:str = 'password'  
    to_addr:str = 'info@mail.ru'   
    from_addr:str = 'info@mail.ru'  
  
#### Не забудьте настроить параметры Telegram для отправки найденных мнемоник  
    token = '509234912:AAE6iDOa-q1F2BWkHFF5o-qjaiM_Ra123IQ'
    channel_id = '@ВашаГруппа'
  
файлы с адресами брать здесь  
https://gz.blockchair.com/  
  
или на моем ресурсе:  
https://drive.google.com/drive/folders/1E2rC7GSc59lAIJi_gD0O-tgGiXwcS7Wl (готовые блюм фильтры)

    E:\GitHub\Hunt-to-Mnemonic>python -B PulsarMTv5.py -b combo -dbbtc BF\btc.bf -dbeth BF\eth.bf -th 3 -des test -m e -sl 5 -brain -em -telegram
    ----------------------------------------------------------------------
    Thank you very much: @iceland2k14 for his libraries!
    ----------------------------------------------------------------------
    DEPENDENCY TESTING:
    [I] TEST: OK!
    ----------------------------------------------------------------------
    [I] Version: * Pulsar v5.2.2 multiT Hash160 *
    [I] Total kernel of CPU: 4
    [I] Used kernel: 3
    [I] Mode Search: BIP-combo Mnemonic from Entropy
    [I] Bloom Filter ETH: BF\eth.bf
    [I] Bloom Filter BTC: BF\btc.bf
    [I] Languages at work ETH: ['english']
    [I] Languages at work BTC: ['english', 'japanese', 'chinese_simplified', 'chinese_traditional']
    [I] Work BIT: 128
    [I] Description client: test
    [I] Smooth start 5 sec
    [I] Send mail: On
    [I] Check balance: Off
    [I] WrainWallet: On
    [I] Telegram: On
    [I] Random check hash: On
    ----------------------------------------------------------------------
    > Cores:3 | Mnemonic: 3853 | Hash MNEM: 485.45 Mhash | Hash BRAIN: 246.59 Khash | 228.87 Khash | Found: 0
    
### Живые примеры работы: (Пока не актуальны. собираю новые)

![WORK](https://github.com/Noname400/Hunt-to-Mnemonic/blob/main/image/primer1.jpg)
![WORK](https://github.com/Noname400/Hunt-to-Mnemonic/blob/main/image/primer2.jpg)
![WORK](https://github.com/Noname400/Hunt-to-Mnemonic/blob/main/image/primer3.jpg)

#### Благодарность за мою работу:  
Bitcoin: 1NoName1LLKRfLmoh9jawLWrf6t185bC7v  
Ethereum: 0xAda9515891532dbA75145c27569e7D5704DBe87f  
