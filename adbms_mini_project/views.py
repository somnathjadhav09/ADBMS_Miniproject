import datetime
import re

import pymongo
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

cluster = MongoClient("mongodb+srv://neil:neil@cluster0.c3c7h.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["adbms_mini_project"]
invoices_collection = db["invoices"]
materials_collection = db["materials"]
traders_collection = db["traders"]
uom_collection = db["uom"]


def register(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect("list_traders")
        return render(request, "new/signin.html")
    elif request.method == 'POST':
        username = request.POST.get('username')
        if User.objects.filter(username=username).exists():
            messages.error(request, "This username already exists")
            return render(request, "new/signin.html")
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            messages.error(request, 'Passwords don\'t match.')
            return render(request, 'new/signin.html')
        user = User.objects.create_user(username=username, password=password1)
        user.save()
        messages.success(request, "Your account has been created")
        return render(request, "new/signin.html")


def login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect("list_traders")
        return render(request, "new/signin.html")
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('list_traders')
        messages.error(request, "Invalid Credentials")
        return redirect("login")


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        messages.info(request, 'You have been logged out successfully.')
        return redirect('login')
    return redirect('login')


def create_trader(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            context = {}
            return render(request, "new/add_trader.html", context)
        elif request.method == 'POST':
            fname = request.POST.get("fname")
            lname = request.POST.get("lname")
            email = request.POST.get("email")
            phone = request.POST.get("phone")
            is_merchant = request.POST.get("is_merchant")
            if is_merchant == 'False':
                is_merchant = False
            else:
                is_merchant = True
            email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            phone_regex = r'[0-9]{10}'
            if not re.fullmatch(email_regex, email):
                messages.error(request, "Please enter a valid email address")
                print("Invalid Email")
                context = {"fname": fname, "lname": lname, "email": email, "phone": phone}
                return render(request, "new/add_trader.html", context)
            if not re.fullmatch(phone_regex, phone):
                messages.error(request, "Please enter a valid phone number")
                print("Invalid Phone Number")
                context = {"fname": fname, "lname": lname, "email": email, "phone": phone}
                return render(request, "new/add_trader.html", context)
            # create new document in collection
            trader = {
                "is_merchant": is_merchant,
                "fname": fname,
                "lname": lname,
                "email": email,
                "phone": phone
            }
            traders_collection.insert_one(trader)
            return redirect('list_traders')
    messages.error(request, "Please login to view this page")
    return redirect('login')


def list_traders(request):
    if request.user.is_authenticated:
        traders = []
        for trader in traders_collection.find({}):
            print(trader)
            traders.append(trader)
        context = {"traders": traders}
        print(context)
        return render(request, "new/merchant.html", context=context)
    messages.error(request, "Please login to view this page")
    return redirect('login')


def update_trader(request, obj_id):
    if request.user.is_authenticated:
        if request.method == 'GET':
            query = {
                "_id": ObjectId(obj_id)
            }
            context = {
                "result": traders_collection.find_one(query)
            }
            print("LOOOOOOOK ATTT MEEEEE", context)
            return render(request, "new/edit_trader.html", context)
        elif request.method == 'POST':
            fname = request.POST.get("fname")
            lname = request.POST.get("lname")
            email = request.POST.get("email")
            phone = request.POST.get("phone")
            is_merchant = request.POST.get("is_merchant")
            if is_merchant == 'False':
                is_merchant = False
            else:
                is_merchant = True
            email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            phone_regex = r'[0-9]{10}'
            if not re.fullmatch(email_regex, email):
                messages.error(request, "Please enter a valid email address")
                print("Invalid Email")
                query = {
                    "_id": ObjectId(obj_id)
                }
                context = {
                    "result": traders_collection.find_one(query)
                }
                return render(request, "new/edit_trader.html", context)
            if not re.fullmatch(phone_regex, phone):
                messages.error(request, "Please enter a valid phone number")
                print("Invalid Phone Number")
                query = {
                    "_id": ObjectId(obj_id)
                }
                context = {
                    "result": traders_collection.find_one(query)
                }
                return render(request, "new/edit_trader.html", context)
            # create new document in collection
            new_values = {
                "$set": {
                    'is_merchant': is_merchant,
                    'fname': fname,
                    'lname': lname,
                    'email': email,
                    'phone': phone
                }
            }
            traders_collection.update_one({'_id': ObjectId(obj_id)}, new_values)
            return redirect('list_traders')
    messages.error(request, "Please login to view this page")
    return redirect('login')


def delete_trader(request, obj_id):
    if request.user.is_authenticated:
        traders_collection.delete_one({'_id': ObjectId(obj_id)})
        return redirect('list_traders')
    messages.error(request, "Please login to view this page")
    return redirect('login')


def create_uom(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            context = {}
            return render(request, "new/add_uom.html", context)
        elif request.method == 'POST':
            title = request.POST.get("title")
            description = request.POST.get("description")
            # create new document in collection
            uom = {
                "title": title,
                "description": description,
            }
            uom_collection.insert_one(uom)
            return redirect('list_uoms')
    messages.error(request, "Please login to view this page")
    return redirect('login')


def list_uoms(request):
    if request.user.is_authenticated:
        uoms = []
        for uom in uom_collection.find({}):
            print(uom)
            uoms.append(uom)
        context = {"uoms": uoms}
        print(context)
        return render(request, "new/uom.html", context=context)
    messages.error(request, "Please login to view this page")
    return redirect('login')


def update_uom(request, obj_id):
    if request.user.is_authenticated:
        if request.method == 'GET':
            query = {
                "_id": ObjectId(obj_id)
            }
            context = {
                "result": uom_collection.find_one(query)
            }
            print("LOOOOOOOK ATTT MEEEEE", context)
            return render(request, "new/add_uom1.html", context)
        elif request.method == 'POST':
            title = request.POST.get("title")
            description = request.POST.get("description")
            # create new document in collection
            new_values = {
                "$set": {
                    'title': title,
                    'description': description
                }
            }
            uom_collection.update_one({'_id': ObjectId(obj_id)}, new_values)
            return redirect('list_uoms')
    messages.error(request, "Please login to view this page")
    return redirect('login')


def delete_uom(request, obj_id):
    if request.user.is_authenticated:
        uom_collection.delete_one({'_id': ObjectId(obj_id)})
        return redirect('list_uoms')
    messages.error(request, "Please login to view this page")
    return redirect('login')


def create_material(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            uom_dict = {

            }
            for uom in uom_collection.find({}):
                print(uom["_id"], uom["title"])
                uom_dict[str(uom["_id"])] = uom["title"]
            print(uom_dict)
            context = {
                'uoms': uom_dict
            }
            return render(request, "new/add_user.html", context)
        elif request.method == 'POST':
            name = request.POST.get("name")
            description = request.POST.get("description")
            uom_fk = request.POST.get("uom_fk")
            price = request.POST.get("price")
            tax_rate = request.POST.get("tax_rate")

            # create new document in collection
            material = {
                "name": name,
                "description": description,
                "uom_fk": ObjectId(uom_fk),
                "price": price,
                "tax_rate": tax_rate
            }
            print("MATERIALS: ", material)
            materials_collection.insert_one(material)
            return redirect('list_materials')
    messages.error(request, "Please login to view this page")
    return redirect('login')


def list_materials(request):
    if request.user.is_authenticated:
        materials = []
        for material in materials_collection.find({}):
            print(material)
            material["uom_fk"] = uom_collection.find_one({"_id": material["uom_fk"]})["title"]
            materials.append(material)
        context = {"materials": materials}
        print(context)
        return render(request, "new/index.html", context=context)
    messages.error(request, "Please login to view this page")
    return redirect('login')


def update_material(request, obj_id):
    if request.user.is_authenticated:
        if request.method == 'GET':
            uom_dict = {

            }
            material = materials_collection.find_one({"_id": ObjectId(obj_id)})
            for uom in uom_collection.find({}):
                print(uom["_id"], uom["title"])
                uom_dict[str(uom["_id"])] = uom["title"]
            uom_dict["selected"] = str(material["uom_fk"])
            material["uom_fk"] = str(material["uom_fk"])
            print(uom_dict)
            context = {
                'uoms': uom_dict,
                'material': material
            }
            print(context)
            return render(request, "new/add_user1.html", context)
        elif request.method == 'POST':
            name = request.POST.get("name")
            description = request.POST.get("description")
            uom_fk = request.POST.get("uom_fk")
            price = request.POST.get("price")
            tax_rate = request.POST.get("tax_rate")

            # create new document in collection
            new_values = {
                "$set": {
                    "name": name,
                    "description": description,
                    "uom_fk": ObjectId(uom_fk),
                    "price": price,
                    "tax_rate": tax_rate
                }
            }
            print("UPDATED MATERIALS: ", new_values)
            materials_collection.update_one({"_id": ObjectId(obj_id)}, new_values)
            return redirect('list_materials')
    messages.error(request, "Please login to view this page")
    return redirect('login')


def delete_material(request, obj_id):
    if request.user.is_authenticated:
        materials_collection.delete_one({'_id': ObjectId(obj_id)})
        return redirect('list_materials')
    messages.error(request, "Please login to view this page")
    return redirect('login')


def list_invoices(request):
    if request.user.is_authenticated:
        invoices = []
        for invoice in invoices_collection.find({}):
            print(invoice)
            invoices.append(invoice)
        context = {"invoices": invoices}
        print(context)
        return render(request, "invoices.html", context=context)
    messages.error(request, "Please login to view this page")
    return redirect('login')


def create_invoice(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            trader_dict = {

            }
            for trader in traders_collection.find({}):
                print(trader["_id"], trader["fname"])
                trader_dict[str(trader["_id"])] = str(trader["fname"] + " " + trader["lname"])
            print(trader_dict)

            material_dict = {

            }
            for product in materials_collection.find({}):
                print(product["_id"], product["name"])
                material_dict[str(product["_id"])] = product["name"]
            print(material_dict)

            context = {
                'traders': trader_dict,
                'materials': material_dict
            }
            return render(request, "invoice_form.html", context)
        elif request.method == 'POST':
            customer_fk = request.POST.get("customer_fk")
            material_fk = request.POST.get("material_fk")
            quantity = request.POST.get("quantity")
            is_sale = request.POST.get("is_sale")
            price = int(materials_collection.find_one({"_id": ObjectId(material_fk)})["price"])
            tax_rate = int(materials_collection.find_one({"_id": ObjectId(material_fk)})["tax_rate"])
            amount = price + ((tax_rate / 100) * price)
            date = datetime.datetime.now()
            if is_sale == 'False':
                is_sale = False
            else:
                is_sale = True
            invoice = {
                'is_sale': is_sale,
                'date_time': date,
                'customer_fk': ObjectId(customer_fk),
                'materials': [
                    {
                        'material_fk': ObjectId(material_fk),
                        'quantity': quantity,
                        'price': price,
                        'tax_rate': tax_rate,
                        'amount': amount
                    },
                ]
            }
            print("INVOICE CREATED IS: ", invoice)
            # input validations
            # create new document in collection
            invoices_collection.insert_one(invoice)
            return redirect('list_invoices')
    messages.error(request, "Please login to view this page")
    return redirect('login')


def update_invoice(request, obj_id):
    if request.user.is_authenticated:
        if request.method == 'GET':
            trader_dict = {

            }
            for trader in traders_collection.find({}):
                print(trader["_id"], trader["fname"])
                trader_dict[str(trader["_id"])] = str(trader["fname"] + " " + trader["lname"])
            print(trader_dict)

            material_dict = {

            }
            for product in materials_collection.find({}):
                print(product["_id"], product["name"])
                material_dict[str(product["_id"])] = product["name"]
            print(material_dict)

            invoice = invoices_collection.find_one({"_id": ObjectId(obj_id)})
            for material in invoice["materials"]:
                material['material_fk'] = str(material['material_fk'])
                invoice["customer_fk"] = str(invoice["customer_fk"])

            context = {
                'traders': trader_dict,
                'materials': material_dict,
                'invoice': invoice
            }
            print("UPDATE INVOICE CONTEXT: ", context)
            return render(request, "invoice_update_form.html", context)
        elif request.method == 'POST':
            customer_fk = request.POST.get("customer_fk")
            material_fk = request.POST.get("material_fk")
            quantity = request.POST.get("quantity")
            is_sale = request.POST.get("is_sale")
            price = int(materials_collection.find_one({"_id": ObjectId(material_fk)})["price"])
            tax_rate = int(materials_collection.find_one({"_id": ObjectId(material_fk)})["tax_rate"])
            amount = price + ((tax_rate / 100) * price)
            date = datetime.datetime.now()
            if is_sale == 'False':
                is_sale = False
            else:
                is_sale = True
            invoice = {
                'is_sale': is_sale,
                'date_time': date,
                'customer_fk': ObjectId(customer_fk),
                'materials': [
                    {
                        'material_fk': ObjectId(material_fk),
                        'quantity': quantity,
                        'price': price,
                        'tax_rate': tax_rate,
                        'amount': amount
                    },
                ]
            }
            print("INVOICE CREATED IS: ", invoice)
            # input validations
            # create new document in collection
            invoices_collection.insert_one(invoice)
            return redirect('list_invoices')
    messages.error(request, "Please login to view this page")
    return redirect('login')


def delete_invoice(request, obj_id):
    if request.user.is_authenticated:
        invoices_collection.delete_one({'_id': ObjectId(obj_id)})
        return redirect('list_invoices')
    messages.error(request, "Please login to view this page")
    return redirect('login')
