import requests
from bs4 import BeautifulSoup
import smtplib
from secrets import gmail, password, toGmail

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                         "Chrome/89.0.4389.114 Safari/537.36"}
URL = 'https://www.trendyol.com/sr?q=Xiaomi%20Mi%20Band%205&qt=Xiaomi%20Mi%20Band%205&st=Xiaomi%20Mi%20Band%205&os=1'
kordon_text = "kordon"
mi_band_text = "mi band 5 akıllı bileklik"

server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.ehlo()
server.login(gmail, password)
subject = 'Daily Price check'

page_content = requests.get(url=URL, headers=headers)

soup = BeautifulSoup(page_content.content, 'html.parser')

products = soup.find_all('div', class_="p-card-wrppr")

for product in products:
    try:
        product_text = product.find('span', class_="prdct-desc-cntnr-name hasRatings").text.lower()
        if not kordon_text in product_text:
            if mi_band_text in product_text:
                link = product.find('div', class_="p-card-chldrn-cntnr").a['href']
                URL = f'https://www.trendyol.com{link}'
                print(URL)
                page_content = requests.get(url=URL, headers=headers)
                soup = BeautifulSoup(page_content.content, 'html.parser')
                try:
                    normal_product_price = soup.find('span', class_="prc-org")
                    discount_product_price = soup.find('span', class_="prc-slg")
                    basket_product_price = soup.find('span', class_="prc-dsc")
                    if normal_product_price is not None or discount_product_price is not None or basket_product_price is not None:
                        if basket_product_price is not None:
                            message = f"Subject : {subject}\n\n Price is now : {basket_product_price.text.split()[0]}"
                            server.sendmail(
                                gmail,
                                toGmail,
                                message
                            )
                        else:
                            if discount_product_price is not None:
                                message = f"Subject : {subject}\n\n Price is now : {discount_product_price.text.split()[0]}"
                                server.sendmail(
                                    gmail,
                                    toGmail,
                                    message
                                )
                            else:
                                if normal_product_price is not None:
                                    message = f"Subject : {subject}\n\n Price is now : {normal_product_price.text.split()[0]}"
                                    server.sendmail(
                                        gmail,
                                        toGmail,
                                        message
                                    )
                                else:
                                    message = f"Subject : Bir sorun var!"
                                    server.sendmail(
                                        gmail,
                                        toGmail,
                                        message
                                    )
                except Exception as e:
                    print("Oops!", e, "occurred.")

    except Exception as e:
        continue

server.quit()