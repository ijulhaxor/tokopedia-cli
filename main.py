import json, time, os, pickle
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

class color:
    normal = "\033[1;37;49m"
    red    = "\033[1;31;49m"
    green  = "\033[1;32;49m"

def clear():
    os.system('clear')
    pass

def banner():
    clear()
    print(f'''{color.green}
  ______      __                        ___       ________    ____
 /_  __/___  / /______  ____  ___  ____/ (_)___ _/ ____/ /   /  _/
  / / / __ \/ //_/ __ \/ __ \/ _ \/ __  / / __ `/ /   / /    / /
 / / / /_/ / ,< / /_/ / /_/ /  __/ /_/ / / /_/ / /___/ /____/ /
/_/  \____/_/|_|\____/ .___/\___/\__,_/_/\__,_/\____/_____/___/ 1.2
                    /_/
{color.normal}
[1] Login Akun               [0] Exit
[2] Beli Pulsa
[3] Kode Promo Checker
''')

    pass

def paymentMethod(id):
    driver.find_element_by_xpath('//span[contains(@class,"css-15y7da7")]').click()
    time.sleep(1)
    driver.find_element_by_xpath(f'//div[contains(@id,"{id}")]').click()
    time.sleep(1.5)
    driver.find_element_by_xpath('//div[contains(@class,"css-v98haz")]').click()
    time.sleep(1)
    totalHarga   = driver.find_elements_by_xpath('//div[contains(@class,"css-1fl8ljt")]')
    totalTagihan = driver.find_element_by_xpath('//div[contains(@class,"css-1lh5lee")]').text
    print(' ')
    print('='*55)
    for th in totalHarga:
        print(th.text.replace("\n"," : "))
        pass

    print(f'Total Tagihan : {totalTagihan}')
    print('='*55)
    driver.find_element_by_xpath('//div[contains(@class,"css-1f2kkgg")]').click()
    input('\nTekan [Enter] untuk melanjutkan... ')
    driver.find_element_by_xpath('//button[contains(@id,"btn-pay-confirm")]').click()
    time.sleep(3)
    try:
        driver.find_element_by_xpath('//button[contains(@class,"css-bvfvsj-unf-btn")]').click()
    except Exception as e:
        pass

    time.sleep(5)
    payDeadline  = driver.find_element_by_xpath('//p[contains(@class,"css-6q98d4-unf-heading-unf-heading")]').text
    payMethod    = driver.find_element_by_xpath('//div[contains(@class,"css-1jr489l")]').text
    NoVirtualAcc = driver.find_element_by_xpath('//div[contains(@id,"copy-code")]').text
    totalPayment = driver.find_element_by_xpath('//div[contains(@class,"css-158s7cq")]').text
    print(f'''
{'='*55}
Batas Akhir Pembayaran : {payDeadline}
Metode Pembayaran      : {payMethod}
Nomor Virtual Account  : {NoVirtualAcc}
Total Pembayaran       : {totalPayment}
{'='*55}''')
    input('\nTekan [Enter] untuk melanjutkan... ')
    pass

def login(phone):
    driver.get('https://tokopedia.com/login/')
    driver.find_element_by_id("email-phone").send_keys(phone)
    driver.find_element_by_tag_name('button').click()
    time.sleep(3)

    try:
        driver.find_element_by_xpath('//img[contains(@src,"https://ecs7.tokopedia.net/otp/cotp/ICON_SMS_NEW.png")]').click()
    except Exception as e:
        print(f'{color.red}Login gagal!{color.normal}')

    time.sleep(1)
    text = driver.find_element_by_xpath('//div[contains(@class,"css-t8bpct")]').text
    clear()
    print(f'{color.green}{text}{color.normal}')

    try:
        driver.find_element_by_tag_name('input').send_keys(input('Kode OTP : '))
    except Exception as e:
        print(f'{color.red}Login gagal!{color.normal}')
        exit()

    time.sleep(2)

    try:
        driver.find_element_by_xpath('//img[contains(@class, "image-user")]').click()
    except Exception as e:
        pass

    time.sleep(3)
    driver.get("https://www.tokopedia.com/")
    pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
    driver.get("https://www.tokopedia.com/user/settings")
    time.sleep(3)

    name = driver.find_element_by_xpath('//span[contains(@class,"css-5hicrt")]').text
    print(f'{color.green}\nLogin Berhasil!{color.normal}\nNama     : {name}\nNo Telp  : {phone}\n')
    input('Press [Enter] key to continue... ')
    driver.get("https://www.tokopedia.com/")

def beliPulsa():
    driver.get("https://www.tokopedia.com/pulsa")
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.get("https://www.tokopedia.com/pulsa/")
    time.sleep(0.5)
    try:
        element = driver.find_element_by_xpath('//img[contains(@class,"css-6bc98m")]')
        driver.execute_script("""
        var element = arguments[0];
        element.parentNode.removeChild(element);
        """, element)
        element = driver.find_element_by_xpath('//button[contains(@class,"css-1oojfrg-unf-btn")]')
        driver.execute_script("""
        var element = arguments[0];
        element.parentNode.removeChild(element);
        """, element)
        element = driver.find_element_by_xpath('//div[contains(@class,"css-1dawwf7-unf-modal")]')
        driver.execute_script("""
        var element = arguments[0];
        element.parentNode.removeChild(element);
        """, element)
        element = driver.find_element_by_xpath('//div[contains(@class,"css-1hw146f-unf-overlay")]')
        driver.execute_script("""
        var element = arguments[0];
        element.parentNode.removeChild(element);
        """, element)
    except Exception as e:
        pass

    driver.find_element_by_xpath('//input[contains(@type,"tel")]').send_keys(input('Nomor Pembeli : '))
    nominal = driver.find_elements_by_xpath('//div[contains(@class, "css-e2jol")]')

    print('\nPilih Nominal Pulsa\n')
    for i, nom in enumerate(nominal):
        print([i], nom.text)
        data = nom.text
        f = open("nominal.txt", "a")
        f.write(f'{data}\n')
        f.close()

    n = int(input('\nPilih : '))
    f = open("nominal.txt", "r")
    result = f.read().split('\n')
    result = json.dumps(result[n])
    index = result.replace('"', '')

    driver.find_element_by_xpath(f'//div[contains(text(),"{index}")]').click()

    os.remove('nominal.txt')

    driver.find_element_by_xpath('//button[contains(@data-test, "beli-btn")]').click()
    time.sleep(2)
    try:
        ket = driver.find_element_by_xpath('//div[contains(@class, "css-1b6t3r5")]').text
        print(f"{color.red}{ket}{color.normal}")
        driver.close()
        exit()
    except Exception as e:
        pass

    time.sleep(1.5)

    select = input('\nGunakan kode promo? [y/n] ')

    if select == "y":
        driver.find_element_by_class_name("promo-title").click()
        time.sleep(2)
        driver.find_element_by_xpath('//div[contains(@class,"css-5bbumj")]').click()
        driver.find_element_by_xpath('//input[contains(@class,"css-ubsgp5")]').click()
        promo = driver.find_elements_by_xpath('//div[contains(@class, "promo-info")]')
        print("\nPromo Untukmu\n")
        for p in promo:
            print(f"{p.text}\n")
            pass

        kode = input('\nMasukkan kode promo : ').upper()
        time.sleep(1.5)
        driver.find_element_by_xpath('//input[contains(@class,"css-ubsgp5")]').send_keys(kode)
        driver.find_element_by_xpath('//span[contains(text(),"Terapkan")]').click()
        time.sleep(1.5)
        try:
            ket = driver.find_element_by_xpath('//p[contains(@class,"css-t9c9fq")]').text
            print(f'''\n{color.red}[{kode}] {ket}{color.normal}
            ''')
        except Exception as e:
            print(f'''\n{color.green}[{kode}] Kode promo dapat digunakan!{color.normal}
            ''')
        pass

    driver.find_element_by_xpath('//span[contains(text(),"Pilih Promo")]').click()

    if select == "n":
        pass

    try:
        print(driver.find_element_by_xpath('//div[contains(@class,"css-dj7unj")]').text)
        time.sleep(1)
        driver.find_element_by_xpath('//span[contains(text(),"Ya, saya mengerti")]').click()
    except Exception as e:
        pass

    details = driver.find_elements_by_xpath('//div[contains(@class,"value")]')
    print('\nCheckout\n')
    for detail in details:
        print(detail.find_element_by_tag_name("p").text)

    input('\nPress [Enter] key to continue... ')
    driver.find_element_by_tag_name("button").click()
    time.sleep(6)
    print('''
[1] Mandiri Virtual Account     [8]  Mitra Tokopedia
[2] BCA Virtual Account         [9]  Alfamart / Alfamidi / Lawson / Dan+Dan
[3] BRIVA                       [10] Indomaret / Ceriamart
[4] BNI Virtual Account         [11] JNE
[5] BTN Virtual Account         [12] Kantorpos
[6] Danamon Virtual Account     [13] FamilyMart
[7] CIMB Virtual Account        [14] Gerai Tokopedia
    ''')
    select = input('Pilih Metode Pembayaran : ')
    if select == "1":
        paymentMethod('mandiriva')
    elif select == "2":
        paymentMethod('bcava')
    elif select == "3":
        paymentMethod('briva')
    elif select == "4":
        paymentMethod('bniva')
    elif select == "5":
        paymentMethod('btnva')
    elif select == "6":
        paymentMethod('danamonva')
    elif select == "7":
        paymentMethod('cimbva')
    elif select == "8":
        paymentMethod('mitratokopedia')
    elif select == "9":
        paymentMethod('alfamart')
    elif select == "10":
        paymentMethod('indomaret')
    elif select == "11":
        paymentMethod('jnepayment')
    elif select == "12":
        paymentMethod('pospay')
    elif select == "13":
        paymentMethod('familymart')
    elif select == "14":
        paymentMethod('tokopediacenter')
    else:
        paymentMethod('indomaret')
    pass

def voucherPulsaChecker():
    driver.get("https://www.tokopedia.com/")
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.get("https://www.tokopedia.com/pulsa")
    time.sleep(2)
    try:
        element = driver.find_element_by_xpath('//img[contains(@class,"css-6bc98m")]')
        driver.execute_script("""
        var element = arguments[0];
        element.parentNode.removeChild(element);
        """, element)
        element = driver.find_element_by_xpath('//button[contains(@class,"css-1oojfrg-unf-btn")]')
        driver.execute_script("""
        var element = arguments[0];
        element.parentNode.removeChild(element);
        """, element)
    except Exception as e:
        pass

    driver.find_element_by_xpath('//input[contains(@type,"tel")]').send_keys('08951234567')
    nominal = driver.find_elements_by_xpath('//div[contains(@class, "css-e2jol")]')

    print('\nPilih Nominal Pulsa\n')
    for i, nom in enumerate(nominal):
        print([i], nom.text)
        data = nom.text
        f = open("nominal.txt", "a")
        f.write(f'{data}\n')
        f.close()

    n = int(input('\nPilih : '))
    f = open("nominal.txt", "r")
    result = f.read().split('\n')
    result = json.dumps(result[n])
    index = result.replace('"', '')

    driver.find_element_by_xpath(f'//div[contains(text(),"{index}")]').click()

    os.remove('nominal.txt')

    driver.find_element_by_xpath('//button[contains(@data-test, "beli-btn")]').click()

    time.sleep(1)
    driver.find_element_by_class_name("promo-title").click()
    time.sleep(1.5)

    file = open(f'vouchers.txt', 'r', encoding="utf8")
    vouchers = []
    for line in file:
        line = line.strip()
        vouchers.append(line)
    file.close()
    for voucher in vouchers:
        driver.find_element_by_xpath('//span[contains(@class,"css-1u1gysd")]').click()
        driver.find_element_by_xpath('//input[contains(@placeholder,"Masukkan kode promo")]').send_keys(voucher)
        driver.find_element_by_xpath('//span[contains(text(),"Terapkan")]').click()
        time.sleep(1)

        try:
            ket = driver.find_element_by_xpath('//p[contains(@class,"css-t9c9fq")]').text
            print(f'''{color.red}[{voucher}] {ket}{color.normal}
            ''')
        except Exception as e:
            print(f'''{color.green}[{voucher}] Kode promo dapat digunakan!{color.normal}
            ''')

    input('Press [Enter] key to continue... ')


while True:
    banner()
    select = input('>> ')
    if select == "1":
        login(input('Nomor HP : '))
    if select == "2":
        beliPulsa()
    if select == "3":
        voucherPulsaChecker()
    if select == "0":
        driver.close()
        exit()
        pass
pass
