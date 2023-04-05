import contextlib
import os
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect, reverse, get_object_or_404
from base.models import  products_names, User, Cart
from utility import JsonData
from django.db.models import Q, Sum, F
from django.contrib.auth.decorators import login_required
from mailjet_rest import Client

keys = JsonData()


def send_email(mail_id):
    
    api_key = keys.getMailJet()['Key']
    api_secret = keys.getMailJet()['SecretCode']
    
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')

    data = {
        'Messages': [
            {
                "From": {
                    "Email": "likhithpindi@gmail.com",
                    "Name": "Me"
                },
                "To": [
                    {
                        "Email": f"{mail_id}",
                        "Name": "You"
                    }
                ],
                "Subject": "Details Regarding Your Order",
                "TextPart": "Greetings from Strandfield!",
                "HTMLPart": "<h3>Thank for Shopping with strandfield  <a href=\"https://www.mailjet.com/\"></a>!</h3><br />May the delivery force be with you!"
            }
        ]
    }
    result = mailjet.send.create(data=data)
    result.status_code
    result.json()


def login_page(request):

    if request.method == 'POST':

        email = request.POST.get('login_email').lower()
        password = request.POST.get('login_password')

        try:
            user = User.objects.get(email=email)
        except Exception:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'welcome {user}')
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    return render(request, 'login.html')


def logout_page(request):
    logout(request)
    return redirect('home')


def home(request):
    items_name = products_names.objects.all()
    if len(items_name) == 0:
        data = {
            'items': [
                {"name": "Basmati Rice 20kg Garimaa Shahi", "price": '25.00',
                 'img': """/media/img/2023/03/11/large_4f4bfbad4a3f9c4bf9726ff5890a-1-removebg-preview.png"""},
                {"name": "White sesame seeds 1 KG", "price": '27.00',
                 'img': """/media/img/2023/03/11/large_sesame-leves.jpg"""},
                {"name": "Toor Daal  2 KG TRS", "price": '32.00',
                 'img': """/media/img/2023/03/11/large_sam-1109-copy.jpg"""},
                {"name": "Tamarind - 400g", "price": '12.00',
                 'img': """/media/img/2023/03/11/large_IMG-3992.jpg"""},

                {"name": "Spicebox 9", "price": '120.00',
                 'img': """/media/img/2023/03/11/large_s-s-masala-peti-500x500.jpg"""},
                {"name": "Ryż Basmati Super JAISAL 5kg", "price": '15.00',
                 'img': """/media/img/2023/03/11/large_jaisal03.jpg"""},
                {"name": "Rice Basmati Exotic/Dubar INDIA GATE 10kg", "price": '105.00',
                 'img': """/media/img/2023/03/11/large_indiagate-exotic-rice-5kg-little-india.jpg"""},
                {"name": "Ryż Basmati Extra Long Premium 10 kg", "price": '150.00',
                 'img': """/media/img/2023/03/11/large_WhatsApp-Image-2022-11-09-at-6-11-08-PM.jpeg"""},

                {"name": "Monaco Jeffs Zeera Biscuits 200G Parle", "price": '5.00',
                 'img': """/media/img/2023/03/11/large_Parle-Jeff-Jeera-Sixer-Cookies-SDL100973706-2-3795a.jpg"""},
                {"name": "Soft Crunch Toast 350G Pran", "price": '15.00',
                 'img': """/media/img/2023/03/11/large_9-3.jpg"""},
                {"name": "Sat Isabgol  100G Pran", "price": '5.00',
                 'img': """/media/img/2023/03/11/large_Sat-Isabgol-100G-Pran.jpeg"""},
                {"name": "Hot Oil Hair Mask- Blackseed 500g Vatika", "price": '20.00',
                 'img': """/media/img/2023/03/11//large_vatika-blackseed-multivitamin-hair-mask-grande.png"""},


                {"name": "Blackseed Multivitamin+ Hair Oil 200ml Vatika Dabur", "price": '19.00',
                 'img': """/media/img/2023/03/11/large_vatika-naturals-blackseed-multivitamin-hair-oil-grande.png"""},
                {"name": "Vatika Naturals Cactus Hair Oil 200ml", "price": '10.00',
                 'img': """/media/img/2023/03/11/large_vatika-naturals-cactus-multivitamin-hair-oil-grande.png"""},
                {"name": "Idiyappam Powder  500G Aachi", "price": '5.00',
                 'img': """/media/img/2023/03/11/large_Kozhukattai-1000x1000.png"""},
                {"name": "Saffola Masala oats,40g", "price": '3.00',
                 'img': """/media/img/2023/03/11/large_Saffola-Masala-Oats-Classic-Masala40g..jpg"""},

                {"name": "Rice Dosa Mix Aachi 1kg", "price": '12.00',
                 'img': """/media/img/2023/03/11/large_Rice-dosa.jpg"""},
                {"name": " Sugar Coated Fennel Seed 250G Little India",
                 "price": '7.00',  'img': """/media/img/2023/03/11/large_moti.png"""},
                {"name": "Vimal Pan Masala V-1Tobacco", "price": '80.00',
                 'img': """/media/img/2023/03/11/large_Vimal.jpg"""},
                {"name": "Vicco Vajradanti Tooth Powder 50g", "price": '2.00',
                 'img': """/media/img/2023/03/11/large_Vicco-Proszek-do-Czyszczenia-Zebow-i-Dziasel-50g.jpg"""},

                {"name": "Mint Chutney 190G Ashoka", "price": '5.00',
                 'img': """/media/img/2023/03/11/large_Bez-nazwy.png"""},
                {"name": "Schezwan Chutney (with olive oil) 190g Ashoka", "price": '5.00',
                 'img': """/media/img/2023/03/11/large_landscape-white-bg-shadow-designify-29-.png"""},
                {"name": "Samosa Chutney 410G Suhana", "price": '8.00',
                 'img': """/media/img/2023/03/11/large_WhatsApp-Image-2021-05-09-at-13-00-54.jpeg"""},
                {"name": "Sandwich Chutney 190G Ashoka", "price": '9.00',
                 'img': """/media/img/2023/03/11/large_Bez-nazwy.png"""},

                {"name": "Ridge Gourd Beerakaaya Chutney 100g Priya", "price": '4.00',
                 'img': """/media/img/2023/03/11/large_61jgtbrcQHL-SX679-.jpg"""},
                {"name": "Coconut milk - 12 x 400g", "price": '65.00',
                 'img': """/media/img/2023/03/11/large_mleko-kokosowe.jpg"""},
                {"name": "Pudina Chana 400g Little India", "price": '7.00',
                 'img': """/media/img/2023/03/11/large_WhatsApp-Image-2022-07-29-at-15-35-19.jpeg"""},
                {"name": "Tapioca Chips Classic Salt 160g A-1 Chips", "price": '3.00',
                 'img': """/media/img/2023/03/11/large_Tapiaco-Chips-Classic-Salt.jpg"""},

                {"name": "Tapioca Chips Salsa Masala 160g A-1 Chips", "price": '4.00',
                 'img': """/media/img/2023/03/11/large_1069-12-2015-A1-chips-Tapioca-Chips-Salsa-Masala.jpg"""},
                {"name": "Tapioca Chips Classic Salt 160g A-1 Chips", "price": '13.00',
                 'img': """/media/img/2023/03/11/large_35-24a557aa-1963-4550-9d19-02c6f3ac2552-1-.png"""},
                {"name": "Gentle Baby Wash HIMALAYA 200ml", "price": '20.00',
                 'img': """/media/img/2023/03/11/large_Himalaya-Gentle-Baby-Wash-200ml.jpg"""},
                {"name": "Vadu Mango Pickle Aachi 300g", "price": '10.00',
                 'img': """/media/img/2023/03/11/large_pobrane.jpeg"""},

                {"name": "Sweet Mango Pickle (with peeled) 500g Rasanand", "price": '7.00',
                 'img': """/media/img/2023/03/11/large_portrait-white-bg-shadow-designify.png"""},
                {"name": "Ahmed Mango Pickle in oil 330g/400g/1kg", "price": '19.00',
                 'img': """/media/img/2023/03/11/large_big-Ahmed-Mangopickle.jpg"""},
                {"name": "Pav Bhaji - 280g Ashoka", "price": '3.00',
                 'img': """/media/img/2023/03/11/large_Bombay-Pav.jpg"""},
                {"name": "Rajma Pulao 280G Ashoka", "price": '8.00',
                 'img': """/media/img/2023/03/11/large_ashoka-rajma-pulao-1.jpg"""},
            ],
        }
        length = len(data["items"])
        for i in range(length):
            items_insert = products_names.objects.create(
                item_name=data['items'][i]['name'], price=data['items'][i]['price'], item_img=data['items'][i]['img'])
            items_insert.save()
    else:
        print('already existed')
    view = products_names.objects.all()
    return render(request, "Index.html")


def register(request):

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_no = request.POST.get('phone_number')
        mail_id = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.create(
                username=first_name,
                first_name=first_name,
                last_name=last_name,
                email=mail_id,
                phone_no=phone_no
            )
            user.set_password(password)
            user.save()
            return redirect('login')
        except BaseException as e:
            print(e)
            messages.error(request, f"Failed in adding {mail_id}")
    return render(request, 'register.html')


def shop(request):
    view = products_names.objects.all()
    return render(request, "shop.html", {'view': view})


def getSearchProducts(request):
    query = request.GET.get('search')

    if query is None:
        query = ""

    items = products_names.objects.filter(
        Q(item_name__icontains=query)
    ).values()
    return JsonResponse(list(items), safe=False)


def orderPlaced(request):
    
    items = Cart.objects.filter(user=request.user)
    
    if not items:
        messages.info(request, 'No products in Cart to plce order')
        return redirect('cart_page')
        
    items.delete()
    
    try:
        send_email(request.user)
    except BaseException as e:
        print(e)
        
    messages.success(request, 'order placed sucessfully')
    return redirect('home')


def CartAddProduct(request):  # sourcery skip: use-named-expression
    user = request.user
    stock_id = request.POST.get('stock_id')
    quantaty = request.POST.get('quantity')
    if user.is_authenticated:
        try:
            cart = Cart(product=products_names.objects.get(id=stock_id),
                        user=user, quantaty=quantaty)
            cart.save()
            return JsonResponse({'success': 'success added to cart'})

        except BaseException as e:
            print(e)
            return JsonResponse({'failed': 'failed added to cart'})

    return JsonResponse({'url': reverse('login')})


@login_required(login_url='login')
def cart_page(request):
    
    products = Cart.objects.filter(user=request.user)
    total_quantity = 0
    total_cart = 0

    for product in products:
        total_quantity += product.quantaty
        total_cart += product.amount

    context = {'products': products,
               'total_items': total_quantity, 'total_cart': total_cart}
    return render(request, "cart.html", context)



def createDummyData():
    items_name = products_names.objects.all()
    if len(items_name) == 0:
        data = {
            'items': [
                {"name": "Basmati Rice 20kg Garimaa Shahi", "price": '25.00',
                 'img': """/media/img/2023/03/11/large_4f4bfbad4a3f9c4bf9726ff5890a-1-removebg-preview.png"""},
                {"name": "White sesame seeds 1 KG", "price": '27.00',
                 'img': """/media/img/2023/03/11/large_sesame-leves.jpg"""},
                {"name": "Toor Daal  2 KG TRS", "price": '32.00',
                 'img': """/media/img/2023/03/11/large_sam-1109-copy.jpg"""},
                {"name": "Tamarind - 400g", "price": '12.00',
                 'img': """/media/img/2023/03/11/large_IMG-3992.jpg"""},

                {"name": "Spicebox 9", "price": '120.00',
                 'img': """/media/img/2023/03/11/large_s-s-masala-peti-500x500.jpg"""},
                {"name": "Ryż Basmati Super JAISAL 5kg", "price": '15.00',
                 'img': """/media/img/2023/03/11/large_jaisal03.jpg"""},
                {"name": "Rice Basmati Exotic/Dubar INDIA GATE 10kg", "price": '105.00',
                 'img': """/media/img/2023/03/11/large_indiagate-exotic-rice-5kg-little-india.jpg"""},
                {"name": "Ryż Basmati Extra Long Premium 10 kg", "price": '150.00',
                 'img': """/media/img/2023/03/11/large_WhatsApp-Image-2022-11-09-at-6-11-08-PM.jpeg"""},

                {"name": "Monaco Jeffs Zeera Biscuits 200G Parle", "price": '5.00',
                 'img': """/media/img/2023/03/11/large_Parle-Jeff-Jeera-Sixer-Cookies-SDL100973706-2-3795a.jpg"""},
                {"name": "Soft Crunch Toast 350G Pran", "price": '15.00',
                 'img': """/media/img/2023/03/11/large_9-3.jpg"""},
                {"name": "Sat Isabgol  100G Pran", "price": '5.00',
                 'img': """/media/img/2023/03/11/large_Sat-Isabgol-100G-Pran.jpeg"""},
                {"name": "Hot Oil Hair Mask- Blackseed 500g Vatika", "price": '20.00',
                 'img': """/media/img/2023/03/11//large_vatika-blackseed-multivitamin-hair-mask-grande.png"""},


                {"name": "Blackseed Multivitamin+ Hair Oil 200ml Vatika Dabur", "price": '19.00',
                 'img': """/media/img/2023/03/11/large_vatika-naturals-blackseed-multivitamin-hair-oil-grande.png"""},
                {"name": "Vatika Naturals Cactus Hair Oil 200ml", "price": '10.00',
                 'img': """/media/img/2023/03/11/large_vatika-naturals-cactus-multivitamin-hair-oil-grande.png"""},
                {"name": "Idiyappam Powder  500G Aachi", "price": '5.00',
                 'img': """/media/img/2023/03/11/large_Kozhukattai-1000x1000.png"""},
                {"name": "Saffola Masala oats,40g", "price": '3.00',
                 'img': """/media/img/2023/03/11/large_Saffola-Masala-Oats-Classic-Masala40g..jpg"""},

                {"name": "Rice Dosa Mix Aachi 1kg", "price": '12.00',
                 'img': """/media/img/2023/03/11/large_Rice-dosa.jpg"""},
                {"name": " Sugar Coated Fennel Seed 250G Little India",
                 "price": '7.00',  'img': """/media/img/2023/03/11/large_moti.png"""},
                {"name": "Vimal Pan Masala V-1Tobacco", "price": '80.00',
                 'img': """/media/img/2023/03/11/large_Vimal.jpg"""},
                {"name": "Vicco Vajradanti Tooth Powder 50g", "price": '2.00',
                 'img': """/media/img/2023/03/11/large_Vicco-Proszek-do-Czyszczenia-Zebow-i-Dziasel-50g.jpg"""},

                {"name": "Mint Chutney 190G Ashoka", "price": '5.00',
                 'img': """/media/img/2023/03/11/large_Bez-nazwy.png"""},
                {"name": "Schezwan Chutney (with olive oil) 190g Ashoka", "price": '5.00',
                 'img': """/media/img/2023/03/11/large_landscape-white-bg-shadow-designify-29-.png"""},
                {"name": "Samosa Chutney 410G Suhana", "price": '8.00',
                 'img': """/media/img/2023/03/11/large_WhatsApp-Image-2021-05-09-at-13-00-54.jpeg"""},
                {"name": "Sandwich Chutney 190G Ashoka", "price": '9.00',
                 'img': """/media/img/2023/03/11/large_Bez-nazwy.png"""},

                {"name": "Ridge Gourd Beerakaaya Chutney 100g Priya", "price": '4.00',
                 'img': """/media/img/2023/03/11/large_61jgtbrcQHL-SX679-.jpg"""},
                {"name": "Coconut milk - 12 x 400g", "price": '65.00',
                 'img': """/media/img/2023/03/11/large_mleko-kokosowe.jpg"""},
                {"name": "Pudina Chana 400g Little India", "price": '7.00',
                 'img': """/media/img/2023/03/11/large_WhatsApp-Image-2022-07-29-at-15-35-19.jpeg"""},
                {"name": "Tapioca Chips Classic Salt 160g A-1 Chips", "price": '3.00',
                 'img': """/media/img/2023/03/11/large_Tapiaco-Chips-Classic-Salt.jpg"""},

                {"name": "Tapioca Chips Salsa Masala 160g A-1 Chips", "price": '4.00',
                 'img': """/media/img/2023/03/11/large_1069-12-2015-A1-chips-Tapioca-Chips-Salsa-Masala.jpg"""},
                {"name": "Tapioca Chips Classic Salt 160g A-1 Chips", "price": '13.00',
                 'img': """/media/img/2023/03/11/large_35-24a557aa-1963-4550-9d19-02c6f3ac2552-1-.png"""},
                {"name": "Gentle Baby Wash HIMALAYA 200ml", "price": '20.00',
                 'img': """/media/img/2023/03/11/large_Himalaya-Gentle-Baby-Wash-200ml.jpg"""},
                {"name": "Vadu Mango Pickle Aachi 300g", "price": '10.00',
                 'img': """/media/img/2023/03/11/large_pobrane.jpeg"""},

                {"name": "Sweet Mango Pickle (with peeled) 500g Rasanand", "price": '7.00',
                 'img': """/media/img/2023/03/11/large_portrait-white-bg-shadow-designify.png"""},
                {"name": "Ahmed Mango Pickle in oil 330g/400g/1kg", "price": '19.00',
                 'img': """/media/img/2023/03/11/large_big-Ahmed-Mangopickle.jpg"""},
                {"name": "Pav Bhaji - 280g Ashoka", "price": '3.00',
                 'img': """/media/img/2023/03/11/large_Bombay-Pav.jpg"""},
                {"name": "Rajma Pulao 280G Ashoka", "price": '8.00',
                 'img': """/media/img/2023/03/11/large_ashoka-rajma-pulao-1.jpg"""},
            ],
        }
        length = len(data["items"])
        for i in range(length):
            items_insert = products_names.objects.create(
                item_name=data['items'][i]['name'], price=data['items'][i]['price'], item_img=data['items'][i]['img'])
            items_insert.save()
    else:
        print('already existed')
    view = products_names.objects.all()

    return render(request,"shop.html", {'view': view})


@login_required(login_url='login')
def deleteItem(request, pk):
    if request.method == 'POST':
        item = get_object_or_404(Cart, id=pk, user=request.user)
        item.delete()
    return redirect('cart_page')
