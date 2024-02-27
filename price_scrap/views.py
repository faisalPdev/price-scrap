from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from pathlib import Path
from selenium.webdriver.common.by import By
import smtplib
from price_scrap.models import searchHistory,TrackHistory
from django.contrib import messages


# Create your views here.

def home(request):
    return render(request,"authentication/index.html")

def signup(request):
    if request.method=="POST":
        uname=request.POST.get('username')
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        email=request.POST.get('email')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')

        if pass1!=pass2:
            messages.error(request,"Your password and confirm password are not same")
        else:
            my_user=User.objects.create_user(uname,email,pass1)
            my_user.first_name=fname
            my_user.last_name=lname
            my_user.save()
            messages.success(request,"Your account has been succefully created")
            return redirect('signin')
       
        
    
    return render(request,"authentication/signup.html")

def signin(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass1')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            fname=user.first_name
            
            return redirect('userview'.format({'fname':fname}))
        else:
            messages.error(request,"Invalid username or password")

    return render(request,"authentication/signin.html")

def about(request):
    return render(request,"authentication/about.html")

def contactus(request):
    return render(request,"authentication/contactus.html")
@login_required(login_url='signin')
def userview(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')

        #amazon
        a_search=product_name.replace(" ","+")
        f_search=product_name.replace(" ","%20")
        c_search=product_name.replace(" ","%20")
        g_search=product_name.replace(" ","+")
        amazon_url=f"https://www.amazon.in/s?k={a_search}&crid=1NC44QS7OT8EV&sprefix={a_search}%2Caps%2C464&ref=nb_sb_noss_1"
        croma_url=f"https://www.croma.com/searchB?q={c_search}%3Arelevance&text={c_search}"
        gadget_url=f'https://shop.gadgetsnow.com/mtkeywordsearch?SEARCH_STRING={g_search}'
        tataneu_url=f'https://www.tatadigital.com/v2/serp?search={g_search}&q={g_search}&scope=Phones+%2526+Wearables&store=&currentPage=1&selectedFacets=&sort='
        jio_url=f'https://www.jiomart.com/search/{c_search}'
        wait_imp = 10
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
        CO = webdriver.ChromeOptions()
        CO.add_experimental_option('useAutomationExtension', False)
        CO.add_argument('--ignore-certificate-errors')

        # CO.headless=True
        # CO.add_argument(f'user_agent={user_agent}')
        # CO.add_argument("--window-size=1920,1080")
        # CO.add_argument('--ignore-certificate-errors')
        # CO.add_argument('--allow-running-insecure-content')
        # CO.add_argument("--disable-extensions")
        # CO.add_argument("--proxy-server='direct://'")
        # CO.add_argument("--proxy-bypass-list=*")
        # CO.add_argument("--start-maximized")
        # CO.add_argument('--disable-gpu')
        # CO.add_argument('--disable-dev-shm-usage')
        # CO.add_argument('--no-sandbox')

        
        wd = webdriver.Chrome(executable_path='C:/Users/FAISAL P/Downloads/chromedriver/chromedriver.exe',options=CO)
        #wd.minimize_window()
        
        wd.get(amazon_url)
        wd.implicitly_wait(wait_imp)
        amazon_price = wd.find_element(By.XPATH,"//span[@class='a-price-whole']")
        amazon_name =wd.find_element(By.XPATH,"//span[@class='a-size-medium a-color-base a-text-normal']")
        amazon_product_name=amazon_name.text.strip()
        amazon_product_price = amazon_price.text.strip()
        amazon_product_image=wd.find_element(By.XPATH,"//img[@class='s-image']").get_attribute('src')
        amazon_link=wd.find_element(By.XPATH,"//a[@class='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal']").get_attribute('href')
        amazon_product_url=amazon_link

        #croma

        wd.get(croma_url)
        wd.implicitly_wait(wait_imp)
        croma_price=wd.find_element(By.XPATH,"//span[@class='amount']")
        croma_product_price=croma_price.text.strip().replace("₹","")
        titles=wd.find_element(By.XPATH,"//h3[@class='product-title plp-prod-title']")

        if titles is not None:
        

                title_name=titles.find_element(By.TAG_NAME,"a")
        else:
                titles=None

        croma_product_name=title_name.text.strip()

        images=wd.find_element(By.XPATH,"//div[@class='product-img plp-card-thumbnail']")

        if images is not None:
             images_src=images.find_element(By.TAG_NAME,"img").get_attribute('src')
        else:
             images=None
        
        croma_product_image=images_src

        link=wd.find_element(By.XPATH,"//div[@class='cp-rating plp-ratings ratings-plp-line']")

        if link is not None:
             link_href=link.find_element(By.TAG_NAME,"a").get_attribute('href')
        else:
             link=None
        
        croma_product_url=link_href

        #jiomart

        # wd.get(jio_url)
        # wd.implicitly_wait(wait_imp)
        # jio_product_price=wd.find_element(By.XPATH,"//span[@class='jm-heading-xxs jm-mb-xxs']").text.strip()
        # jio_product_name=wd.find_element(By.XPATH,"//div[@class='plp-card-details-name line-clamp jm-body-xs jm-fc-primary-grey-80']").text
        # jio_product_image=wd.find_element(By.XPATH,"//img[@class='lazyautosizes ls-is-cached lazyloaded']").get_attribute('src')
        # jio_product_url=wd.find_element(By.XPATH,"//li[@class='ais-InfiniteHits-item jm-col-4 jm-mt-base']/a").get_attribute('href')



        # Flipkart
        flipkart_url = f"https://www.flipkart.com/search?q={f_search}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
        flipkart_response = requests.get(flipkart_url)
        flipkart_soup = BeautifulSoup(flipkart_response.text, 'html.parser')

        flipkart_product_card=flipkart_soup.find('div',{'class':'_2kHMtA'})
        if flipkart_product_card:
            flipkart_product_name=flipkart_product_card.find('div',{'class':'_4rR01T'}).text.strip()
            flipkart_product_url='https://www.flipkart.com'+flipkart_product_card.find('a',{'class':'_1fQZEK'})['href']
            flipkart_product_image=flipkart_product_card.find('img',{'class':'_396cs4'})['src']
            flipkart_product_price=flipkart_product_card.find('div',{'class':'_30jeq3 _1_WHN1'})
            flipkart_product_price=flipkart_product_price.text.strip()[1:]
        else:
            flipkart_product_card=None


        #gadgetsnow
        wd.get(gadget_url)
        wd.implicitly_wait(wait_imp)

        gadget_product_name=wd.find_element(By.XPATH,"//span[@class='product-name']").text
        gadget_product_price=wd.find_element(By.XPATH,"//span[@class='offerprice']").text.replace("`","").strip()
        try:
           gadget_product_url=wd.find_element(By.XPATH,"//a[@class='product-anchor']").get_attribute('href')
        except:
             gadget_product_url=wd.find_element(By.XPATH,"//a[@class='itemname']").get_attribute('href')
        #if gadget_product_url1 is not None:
             # gadget_product_url=wd.find_element(By.XPATH,"//a[@class='product-anchor']").get_attribute('href')
        #else:
        #gadget_product_url=wd.find_element(By.XPATH,"//a[@class='itemname']").get_attribute('href')
        images1=wd.find_element(By.XPATH,"//div[@class='product-img-align']")

        if images1 is not None:
                images_src1=images1.find_element(By.TAG_NAME,"img").get_attribute('src')
        else:
                images_src1=None

        gadget_product_image=images_src1


        # tataneu
        wd.get(tataneu_url)
        wd.implicitly_wait(wait_imp)
        tataneu_product_name=wd.find_element(By.XPATH,"//span[@class='MuiTypography-root MuiTypography-body.small-regular css-1o60qtd']").text
        tataneu_product_price=wd.find_element(By.XPATH,"//span[@class='MuiTypography-root MuiTypography-body-m css-15d90lv']").text.replace("₹","").strip()
        image2=wd.find_element(By.XPATH,"//div[@class='css-50wgu']")
        if image2 is not None:
             tataneu_product_image=image2.find_element(By.TAG_NAME,"img").get_attribute('src')
        else:
             tataneu_product_image=None
        tataneu_product_url=tataneu_url
        context = {
            'product_name':product_name,
            #'amazon_price': amazon_price,
            #'flipkart_price': flipkart_price,
            #'flipkart_link' :link_fipkart,
            #'amazon_link':link_amazon,
            #'croma_price': croma_price,
            #'reliance_price':reliance_price,
            'flipkart_product_card':flipkart_product_card,
            'flipkart_product_name':flipkart_product_name,
            'flipkart_product_url':flipkart_product_url,
            'flipkart_product_image':flipkart_product_image,
            'flipkart_product_price':flipkart_product_price,
           # 'amazon_product_card':amazon_product_card,
            'amazon_product_name':amazon_product_name,
            'amazon_product_url':amazon_product_url,
            'amazon_product_image':amazon_product_image,
           'amazon_product_price':amazon_product_price,
           'croma_product_name':croma_product_name,
           'croma_product_price':croma_product_price,
           'croma_product_image':croma_product_image,
           'croma_product_url':croma_product_url,
           'gadget_product_name':gadget_product_name,
           'gadget_product_price':gadget_product_price,
           'gadget_product_image':gadget_product_image,
           'gadget_product_url':gadget_product_url,
           'tataneu_product_name':tataneu_product_name,
           'tataneu_product_price':tataneu_product_price,
           'tataneu_product_image':tataneu_product_image,
           'tataneu_product_url':tataneu_product_url,
        #    'jio_product_name':jio_product_name,
        #    'jio_product_price':jio_product_price,
        #    'jio_product_image':jio_product_image,
        #    'jio_product_url':jio_product_url,

            
        }
        obj=searchHistory()
        obj.search_term=product_name
        obj.flipkart_title=flipkart_product_name
        obj.flipkart_price=flipkart_product_price
        obj.amazon_title=amazon_product_name
        obj.amazon_price=amazon_product_price
        obj.croma_title=croma_product_name
        obj.croma_price=croma_product_price
        obj.gadget_title=gadget_product_name
        obj.gadget_price=gadget_product_price
        obj.tata_title=tataneu_product_name
        obj.tata_price=tataneu_product_price
       
        
        obj.save()
        return render(request, "authentication/userview.html", context)
  
    return render(request, 'authentication/userview.html')  




def Logoutpage(request):
    logout(request)
    return redirect('home')

def tracking(request):
        if request.method == 'POST':
            url= request.POST.get('url')
            user_price=int(request.POST.get('user_price'))
            website=request.POST.get('website')
            user_email=request.POST.get('user_email')

                
            wait_imp = 10
            CO = webdriver.ChromeOptions()
            CO.add_experimental_option('useAutomationExtension', False)
            CO.add_argument('--ignore-certificate-errors')
            CO.add_argument('--start-minimized')
            wd = webdriver.Chrome(executable_path='C:/Users/FAISAL P/Downloads/chromedriver/chromedriver.exe',options=CO)

            def flipkart():
                def check_price():
                    wd.get(url)
                    wd.implicitly_wait(wait_imp)
                    price1=wd.find_element(By.XPATH,"//div[@class='_30jeq3 _16Jk6d']").text.strip()[1:]
            #name =wd.find_element(By.XPATH,"//span[@class='a-size-large product-title-word-break']")
                    converted_price1=int(price1.replace(',',''))
#product_name=name.text
       # if(price<=userprice):
            #   send_mail()

                    print(converted_price1)
                    if(converted_price1<=user_price):
                            send_mail1()
       # if(price<)

                def send_mail1():
                        server=smtplib.SMTP('smtp.gmail.com', 587)
                        server.ehlo()
                        server.starttls()
                        server.ehlo()

                        server.login('mohdfaisal9072@gmail.com','suyajhqimeipjjhq')
                        subject=' Flipkart price fell down'
                        body=f'hey price is dropped for your product  check the link {url}' 
                        msg=f"Subject: {subject}\n\n{body}"
                        server.sendmail(
                                'mohdfaisal9072@gmail.com',
                                {user_email},
                                msg
                        )
                        print('hey mail has been send')
                        messages.success(request,"hey!. mail has been send")
                        server.quit()

                check_price()

            def croma():
                def check2_price():
                    wd.get(url)
                    wd.implicitly_wait(wait_imp)
                    price2=wd.find_element(By.XPATH,"//span[@class='amount']").text.strip()[1:]
            #name =wd.find_element(By.XPATH,"//span[@class='a-size-large product-title-word-break']")
                    converted_price2=int(price2.replace(',','').replace('"','').replace('₹','').replace('.','')) //100
#product_name=name.text
       # if(price<=userprice):
            #   send_mail()

                    print(converted_price2)
                    if(converted_price2<=user_price):
                            send_mail2()
       # if(price<)

                def send_mail2():
                            server=smtplib.SMTP('smtp.gmail.com', 587)
                            server.ehlo()
                            server.starttls()
                            server.ehlo()

                            server.login('mohdfaisal9072@gmail.com','suyajhqimeipjjhq')
                            subject='Croma price fell down'
                            body=f'hey price is dropped for your product  check the link {url}'
                            msg=f"Subject: {subject}\n\n{body}"
                            server.sendmail(
                                    'mohdfaisal9072@gmail.com',
                                    {user_email},
                                    msg
                            )
                            print('hey mail has been send')
                            server.quit()
                check2_price()

            def gadgetnow():
                def check2_price():
                    wd.get(url)
                    wd.implicitly_wait(wait_imp)
                    price2=wd.find_element(By.XPATH,"//span[@class='offerprice flt']").text.strip()
            #name =wd.find_element(By.XPATH,"//span[@class='a-size-large product-title-word-break']")
                    converted_price2=int(price2.replace(',','').replace('`','').replace('Offer Price :',''))

#product_name=name.text
       # if(price<=userprice):
            #   send_mail()

                    print(converted_price2)
                    if(converted_price2<=user_price):
                            send_mail2()
       # if(price<)

                def send_mail2():
                            server=smtplib.SMTP('smtp.gmail.com', 587)
                            server.ehlo()
                            server.starttls()
                            server.ehlo()

                            server.login('mohdfaisal9072@gmail.com','suyajhqimeipjjhq')
                            subject=' GADGET NOW price fell down'
                            body=f'hey price is dropped for your product  check the link {url}'
                            msg=f"Subject: {subject}\n\n{body}"
                            server.sendmail(
                                    'mohdfaisal9072@gmail.com',
                                    {user_email},
                                    msg
                            )
                            print('hey mail has been send')
                            server.quit()
                check2_price()
            
            def tataneu():
                def check2_price():
                    wd.get(url)
                    wd.implicitly_wait(wait_imp)
                    price2=wd.find_element(By.XPATH,"//span[@class='amount']").text.strip()[1:]
            #name =wd.find_element(By.XPATH,"//span[@class='a-size-large product-title-word-break']")
                    converted_price2=int(price2.replace(',','').replace('"','').replace('₹','').replace('.','')) //100

#product_name=name.text
       # if(price<=userprice):
            #   send_mail()

                    print(converted_price2)
                    if(converted_price2<=user_price):
                            send_mail2()
       # if(price<)

                def send_mail2():
                            server=smtplib.SMTP('smtp.gmail.com', 587)
                            server.ehlo()
                            server.starttls()
                            server.ehlo()

                            server.login('mohdfaisal9072@gmail.com','suyajhqimeipjjhq')
                            subject='TATA NEU price fell down'
                            body=f'hey price is dropped for your product  check the link {url}'
                            msg=f"Subject: {subject}\n\n{body}"
                            server.sendmail(
                                    'mohdfaisal9072@gmail.com',
                                    {user_email},
                                    msg
                            )
                            print('hey mail has been send')
                            server.quit()
                check2_price()

            def switch_case(website):
                if website=='flipkart':
                        flipkart()
                elif website=='croma':
                        croma()
                elif website=='gadgetnow':
                        gadgetnow()
                elif website=='tataneu':
                        tataneu()
            switch_case(website)
            context={
                'url':url,
                'website':website,
                'user_email':user_email,
                'user_price':user_price,
                
                
            }
            obj=TrackHistory()
            obj.url=url
            obj.user_email=user_email
            obj.user_price=user_price
            obj.website=website
            obj.save()

            return render(request, 'authentication/tracking.html', context)

        return render(request, 'authentication/tracking.html')
def search(request):
   mydata=searchHistory.objects.all()
   return render(request,'authentication/searcHistory.html',{'datas':mydata})
def trackHistory(request):
    mytrack=TrackHistory.objects.all()
    return render(request,'authentication/trackHistory.html',{'datas':mytrack})