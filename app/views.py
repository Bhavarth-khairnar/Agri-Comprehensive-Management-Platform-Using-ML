from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from app.auth import authentication,input_verification,input_verification1
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from app.models import *
import keras
from keras.models import load_model
from keras.preprocessing.image import img_to_array, load_img
from keras.applications.vgg19 import preprocess_input
import numpy as np
import tensorflow as tf
import pickle
from datetime import datetime
# Create your views here.
def index(request):
    return render(request, "index.html", {'navbar' : 'home'})

def e_market(request):
    return render(request, "e_market.html", {'navbar' : 'home'})

def register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone_number = request.POST['phone_number']
        username = request.POST['username']
        password = request.POST['password']
        password1 = request.POST['password1']
        # print(first_name, contact_no, ussername)
        verify = authentication(first_name, last_name, password, password1, phone_number)
        if verify == "success":
            user = User.objects.create_user(username, password, password1)          #create_user
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            messages.success(request, "Your Account has been Created.")
            return redirect("/")
            
        else:
            messages.error(request, verify)
            return redirect("register")
            # return HttpResponse("This is Home page")
    return render(request, "register.html", {'navbar' : 'register'})

def log_in(request):
    if request.method == "POST":
        # return HttpResponse("This is Home page")  
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, "Log In Successful...!")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid User...!")
            return redirect("log_in")
    return render(request, "log_in.html", {'navbar' : 'log_in'})

@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def log_out(request):
    logout(request)
    messages.success(request, "Log out Successfuly...!")
    return redirect("/")

@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def dashboard(request):
    context = {
        'first_name': request.user.first_name, 
        'last_name': request.user.last_name, 
    }
    
    return render(request, "dashboard.html", context)


@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def crop_report(request):
    crop_data = Crop_Details.objects.last()
    context = {
        'first_name': request.user.first_name, 
        'last_name': request.user.last_name, 
        'crop_data' : crop_data
    }
    if request.method == "POST":
        return redirect("report")
    return render(request, "crop_report.html", context)

@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def fert_report(request):
    fert_data = fert_Details.objects.last()
    context = {
        'first_name': request.user.first_name, 
        'last_name': request.user.last_name, 
        'fert_data' : fert_data
    }
    if request.method == "POST":
        return redirect("report1")
    return render(request, "fert_report.html", context)


@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def report(request):
    crop_data = Crop_Details.objects.last()
    context = { 
        'crop_data' : crop_data
    }
    return render(request, "report.html", context)


@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def report1(request):
    fert_data = fert_Details.objects.last()
    context = {
        'fert_data' : fert_data
    }
    return render(request, "report1.html", context)


def loan1(request):
    return render(request, "loan1.html", {'navbar' : 'home'})

def insurance(request):
    return render(request, "insurance.html", {'navbar' : 'home'})

def crop_prediction(request):
    if request.method == "POST":
        farmer_name = request.POST['farmer_name']
        contact_no = request.POST['contact_no']
        n = request.POST['n']
        p = request.POST['p']
        k = request.POST['k']
        temperature = request.POST['temperature']
        humidity = request.POST['humidity']
        ph = request.POST['ph']
        rainfall = request.POST['rainfall']
        
        verify = input_verification(farmer_name, contact_no, n, p, k, temperature, humidity, ph, rainfall)
        if verify == "Success":
            
            with open('dataset/crop_prediction.pkl', 'rb') as f:
                model = pickle.load(f)
            
            
            with open('dataset/label_encoder.pkl', 'rb') as f:
                le = pickle.load(f)
            
           
            data = np.array([[n, p, k, temperature, humidity, ph, rainfall]], dtype=float)
            
            # Predict
            pred_id = model.predict(data)[0]  # numeric label
            crop_name = le.inverse_transform([pred_id])[0]  # convert to string
            
            # Message
            message = 'Predicted Crop is : ' + str(crop_name)
            
            # Save to DB
            crop = Crop_Details(
                farmer_name = farmer_name,
                contact_no = contact_no,
                n = n,
                p = p,
                k = k,
                temperature = temperature,
                humidity= humidity,
                ph = ph,
                rainfall = rainfall
            )
            crop.prediction = message
            crop.date = datetime.today()
            crop.save()
            
            messages.info(request, message)
            return redirect("crop_report")
        else:
            messages.error(request, verify)
            return redirect("dashboard")
    
    return render(request, "crop_prediction.html", {'navbar': 'home'})



def crop_dis(request):
    return render(request, "crop_dis.html", {'navbar' : 'home'})


def fert_rec(request):
    if request.method == "POST":
        farmer_name = request.POST['farmer_name']
        n = request.POST['n']
        p = request.POST['p']
        k = request.POST['k']
        temperature = request.POST['temperature']
        humidity = request.POST['humidity']
               
        verify = input_verification1(farmer_name, n, p, k, temperature, humidity)
        if verify == "Success":
            with open('dataset/Fertilizer_Classifier.pkl', 'rb') as f:
                NaiveBayes = pickle.load(f)
            data = np.array([[n,p,k,temperature,humidity]], dtype=float)
            pred = NaiveBayes.predict(data)
            message = 'Predicted Fertilizer is : ' + pred[0]
            fert = fert_Details(farmer_name = farmer_name, n = n, p = p, k = k, temperature = temperature, humidity= humidity,fertilizer = pred)
            fert.prediction = message
            fert.date = datetime.today()
            fert.save()
            messages.info(request, message)
            return redirect("fert_report")
        else:
            messages.error(request, verify)
            return redirect("dashboard")
    return render(request, "fert_rec.html", {'navbar': 'home'})


label_mapping = {0: 'Apple___Apple_scab',
 1: 'Apple___Black_rot',
 2: 'Apple___Cedar_apple_rust',
 3: 'Apple___healthy',
 4: 'Blueberry___healthy',
 5: 'Cherry_(including_sour)___Powdery_mildew',
 6: 'Cherry_(including_sour)___healthy',
 7: 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
 8: 'Corn_(maize)__Common_rust',
 9: 'Corn_(maize)___Northern_Leaf_Blight',
 10: 'Corn_(maize)___healthy',
 11: 'Grape___Black_rot',
 12: 'Grape__Esca(Black_Measles)',
 13: 'Grape__Leaf_blight(Isariopsis_Leaf_Spot)',
 14: 'Grape___healthy',
 15: 'Orange__Haunglongbing(Citrus_greening)',
 16: 'Peach___Bacterial_spot',
 17: 'Peach___healthy',
 18: 'Pepper,bell__Bacterial_spot',
 19: 'Pepper,bell__healthy',
 20: 'Potato___Early_blight',
 21: 'Potato___Late_blight',
 22: 'Potato___healthy',
 23: 'Raspberry___healthy',
 24: 'Soybean___healthy',
 25: 'Squash___Powdery_mildew',
 26: 'Strawberry___Leaf_scorch',
 27: 'Strawberry___healthy',
 28: 'Tomato___Bacterial_spot',
 29: 'Tomato___Early_blight',
 30: 'Tomato___Late_blight',
 31: 'Tomato___Leaf_Mold',
 32: 'Tomato___Septoria_leaf_spot',
 33: 'Tomato___Spider_mites Two-spotted_spider_mite',
 34: 'Tomato___Target_Spot',
 35: 'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
 36: 'Tomato___Tomato_mosaic_virus',
 37: 'Tomato___healthy'}

label_descriptions = {
    'Apple___Apple_scab': 'Apple scab is a disease of Malus trees, such as apple trees, caused by the ascomycete fungus Venturia inaequalis. The disease manifests as dull black or grey-brown lesions on the surface of tree leaves, buds, and fruits.',
    'Apple___Black_rot': 'Black rot is a fungal disease caused by the pathogen Botryosphaeria obtusa. It affects apple trees and manifests as dark, sunken lesions on fruits, leaves, and shoots, often leading to fruit decay.',
    'Apple___Cedar_apple_rust': 'Cedar apple rust is a fungal disease caused by Gymnosporangium juniperi-virginianae. It affects apple and cedar trees and manifests as orange or rust-colored spots on leaves and fruits.',
    'Apple___healthy': 'Healthy apple trees showing no signs of disease or pest infestation.',
    'Blueberry___healthy': 'Healthy blueberry plants showing no signs of disease or pest infestation.',
    'Cherry_(including_sour)___Powdery_mildew': 'Powdery mildew is a fungal disease caused by various pathogens such as Podosphaera clandestina. It affects cherry trees and manifests as white powdery spots on leaves and shoots.',
    'Cherry_(including_sour)___healthy': 'Healthy cherry trees showing no signs of disease or pest infestation.',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot': 'Cercospora leaf spot, also known as gray leaf spot, is a fungal disease caused by the pathogen Cercospora zeae-maydis. It affects corn plants and manifests as small, oval lesions with gray centers on leaves.',
    'Corn_(maize)__Common_rust': 'Common rust is a fungal disease caused by Puccinia sorghi. It affects corn plants and manifests as small, circular, orange to brown pustules on leaves.',
    'Corn_(maize)___Northern_Leaf_Blight': 'Northern leaf blight is a foliar fungal disease caused by Exserohilum turcicum. It affects corn plants and manifests as long, elliptical lesions with wavy margins on leaves.',
    'Corn_(maize)___healthy': 'Healthy corn plants showing no signs of disease or pest infestation.',
    'Grape___Black_rot': 'Black rot is a fungal disease caused by the pathogen Guignardia bidwellii. It affects grapevines and manifests as large, irregular brown lesions on leaves, shoots, and berries.',
    'Grape__Esca(Black_Measles)': 'Esca, also known as black measles, is a complex disease of grapevines caused by various fungi, including Phaeomoniella chlamydospora and Phaeoacremonium spp. It affects grapevines and manifests as leaf discoloration, wood necrosis, and decline.',
    'Grape__Leaf_blight(Isariopsis_Leaf_Spot)': 'Leaf blight, caused by the fungus Isariopsis spp., affects grapevines and manifests as small, circular lesions on leaves, which later develop into larger, irregular spots with gray centers and dark borders.',
    'Grape___healthy': 'Healthy grapevines showing no signs of disease or pest infestation.',
    'Orange__Haunglongbing(Citrus_greening)': 'Huanglongbing, also known as citrus greening disease, is a bacterial disease caused by Candidatus Liberibacter spp. It affects citrus trees, including oranges, and manifests as yellow shoots, mottled leaves, and bitter, misshapen fruits.',
    'Peach___Bacterial_spot': 'Bacterial spot is a disease caused by Xanthomonas arboricola pv. pruni. It affects peach trees and manifests as small, dark spots on leaves and fruits, which may enlarge and develop a raised, scab-like appearance.',
    'Peach___healthy': 'Healthy peach trees showing no signs of disease or pest infestation.',
    'Pepper,bell__Bacterial_spot': 'Bacterial spot, caused by Xanthomonas spp., affects pepper plants and manifests as small, water-soaked lesions on leaves, which later turn brown and necrotic with yellow halos.',
    'Pepper,bell__healthy': 'Healthy bell pepper plants showing no signs of disease or pest infestation.',
    'Potato___Early_blight': 'Early blight is a fungal disease caused by Alternaria solani. It affects potato plants and manifests as small, dark brown lesions on leaves, which may expand and develop concentric rings.',
    'Potato___Late_blight': 'Late blight, caused by Phytophthora infestans, is a devastating fungal disease affecting potato plants. It manifests as dark, water-soaked lesions on leaves, stems, and tubers, often leading to rapid plant defoliation and tuber rot.',
    'Potato___healthy': 'Healthy potato plants showing no signs of disease or pest infestation.',
    'Raspberry___healthy': 'Healthy raspberry plants showing no signs of disease or pest infestation.',
    'Soybean___healthy': 'Healthy soybean plants showing no signs of disease or pest infestation.',
    'Squash___Powdery_mildew': 'Powdery mildew is a fungal disease caused by various pathogens such as Podosphaera xanthii. It affects squash plants and manifests as white powdery spots on leaves, stems, and fruits.',
    'Strawberry___Leaf_scorch': 'Leaf scorch is a physiological disorder affecting strawberry plants, often caused by environmental stressors such as drought, heat, or salt. It manifests as browning and drying of leaf margins and tips.',
    'Strawberry___healthy': 'Healthy strawberry plants showing no signs of disease or pest infestation.',
    'Tomato___Bacterial_spot': 'Bacterial spot, caused by Xanthomonas spp., affects tomato plants and manifests as small, water-soaked lesions on leaves, which later turn brown and necrotic with yellow halos.',
    'Tomato___Early_blight': 'Early blight is a fungal disease caused by Alternaria solani. It affects tomato plants and manifests as small, dark brown lesions with concentric rings on lower leaves, which may lead to defoliation.',
    'Tomato___Late_blight': 'Late blight, caused by Phytophthora infestans, is a devastating fungal disease affecting tomato plants. It manifests as dark, water-soaked lesions on leaves, stems, and fruits, often leading to rapid plant defoliation and fruit rot.',
    'Tomato___Leaf_Mold': 'Leaf mold is a fungal disease caused by Passalora fulva (formerly known as Fulvia fulva). It affects tomato plants and manifests as yellowing and wilting of lower leaves, with fuzzy white or gray fungal growth on the undersides of leaves.',
    'Tomato___Septoria_leaf_spot': 'Septoria leaf spot, caused by the fungus Septoria lycopersici, affects tomato plants and manifests as small, circular lesions with dark borders on leaves, which may coalesce and cause leaf yellowing and defoliation'
}

prevention_methods = {
    'Apple___Apple_scab': "1. Prune to increase air circulation.\n2. Remove fallen leaves and debris.\n3. Apply fungicides during the growing season.",
    'Apple___Black_rot': "1. Prune to increase air circulation.\n2. Remove mummified fruit and leaves.\n3. Apply fungicides during the growing season.",
    'Apple___Cedar_apple_rust': "1. Plant resistant varieties.\n2. Remove cedar trees from proximity to apple trees.\n3. Apply fungicides during the growing season.",
    'Apple___healthy': "Maintain overall tree health through proper pruning, watering, and fertilization.",
    'Blueberry___healthy': "Maintain overall plant health through proper pruning, watering, and fertilization.",
    'Cherry_(including_sour)___Powdery_mildew': "1. Prune to increase air circulation.\n2. Apply fungicides before symptoms appear.",
    'Cherry_(including_sour)___healthy': "Maintain overall tree health through proper pruning, watering, and fertilization.",
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot': "1. Rotate crops to reduce disease pressure.\n2. Use resistant varieties when available.\n3. Apply fungicides preventatively.",
    'Corn_(maize)__Common_rust': "1. Plant resistant varieties.\n2. Monitor fields and apply fungicides as necessary.",
    'Corn_(maize)___Northern_Leaf_Blight': "1. Rotate crops to reduce disease pressure.\n2. Use resistant varieties when available.\n3. Apply fungicides preventatively.",
    'Corn_(maize)___healthy': "Maintain overall plant health through proper spacing, irrigation, and fertilization.",
    'Grape___Black_rot': "1. Prune to increase air circulation.\n2. Remove mummified fruit and leaves.\n3. Apply fungicides during the growing season.",
    'Grape__Esca(Black_Measles)': "1. Prune to remove infected wood.\n2. Apply fungicides during the growing season.",
    'Grape__Leaf_blight(Isariopsis_Leaf_Spot)': "1. Prune to increase air circulation.\n2. Apply fungicides preventatively.",
    'Grape___healthy': "Maintain overall vine health through proper pruning, trellising, and canopy management.",
    'Orange__Haunglongbing(Citrus_greening)': "1. Use disease-free planting material.\n2. Control insect vectors.\n3. Remove infected trees promptly.",
    'Peach___Bacterial_spot': "1. Prune to increase air circulation.\n2. Apply copper-based fungicides during the growing season.",
    'Peach___healthy': "Maintain overall tree health through proper pruning, watering, and fertilization.",
    'Pepper,bell__Bacterial_spot': "1. Rotate crops to reduce disease pressure.\n2. Use disease-free seeds or transplants.\n3. Apply copper-based fungicides preventatively.",
    'Pepper,bell__healthy': "Maintain overall plant health through proper spacing, irrigation, and fertilization.",
    'Potato___Early_blight': "1. Rotate crops to reduce disease pressure.\n2. Remove infected plant debris.\n3. Apply fungicides preventatively.",
    'Potato___Late_blight': "1. Rotate crops to reduce disease pressure.\n2. Use certified disease-free seed potatoes.\n3. Apply fungicides preventatively.",
    'Potato___healthy': "Maintain overall plant health through proper spacing, irrigation, and fertilization.",
    'Raspberry___healthy': "Maintain overall plant health through proper pruning, trellising, and fertilization.",
    'Soybean___healthy': "Maintain overall plant health through proper crop rotation, weed control, and pest management.",
    'Squash___Powdery_mildew': "1. Space plants properly to increase air circulation.\n2. Apply fungicides preventatively.\n3. Remove and destroy infected plant parts.",
    'Strawberry___Leaf_scorch': "1. Plant in well-drained soil.\n2. Avoid overhead irrigation.\n3. Apply fungicides preventatively.",
    'Strawberry___healthy': "Maintain overall plant health through proper spacing, irrigation, and fertilization.",
    'Tomato___Bacterial_spot': "1. Rotate crops to reduce disease pressure.\n2. Use disease-resistant varieties.\n3. Apply copper-based fungicides preventatively.",
    'Tomato___Early_blight': "1. Rotate crops to reduce disease pressure.\n2. Mulch to prevent soil splash.\n3. Apply fungicides preventatively.",
    'Tomato___Late_blight': "1. Rotate crops to reduce disease pressure.\n2. Remove infected plant debris.\n3. Apply fungicides preventatively.",
    'Tomato___Leaf_Mold': "1. Prune to increase air circulation.\n2. Use drip irrigation to keep foliage dry.\n3. Apply fungicides preventatively.",
    'Tomato___Septoria_leaf_spot': "1. Rotate crops to reduce disease pressure.\n2. Prune to increase air circulation.\n3. Apply fungicides preventatively.",
    'Tomato___Spider_mites Two-spotted_spider_mite': "1. Monitor for mites and apply miticides as necessary.\n2. Use reflective mulches to deter mites.\n3. Introduce natural predators of mites.",
    'Tomato___Target_Spot': "1. Rotate crops to reduce disease pressure.\n2. Apply fungicides preventatively.\n3. Remove and destroy infected plant material.",
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus': "1. Use virus-free transplants.\n2. Control whiteflies, which transmit the virus.\n3. Remove and destroy infected plants.",
    'Tomato___Tomato_mosaic_virus': "1. Use virus-free transplants.\n2. Control aphids, which transmit the virus.\n3. Remove and destroy infected plants.",
    'Tomato___healthy': "Maintain overall plant health through proper spacing, irrigation, and fertilization."
}


# Load the trained model
model = load_model("dataset/best_model.h5")

# Load and preprocess the image


def prediction(path):
    img = load_img(path, target_size=(224,224))
    i = img_to_array(img)
    im = preprocess_input(i)
    img = np.expand_dims(im, axis=0)
    pred = np.argmax(model.predict(img))
    label = label_mapping[pred]
    return label

def upload(request):
    if request.method == "POST":
        images = request.FILES['Images']

        s = images_data(Images=images)
        s.save()

        return redirect("predict")
    else:
        return HttpResponse("Fail")

#
def predict(request):
    img = images_data.objects.last()
    image_path = str(img.Images.url)
    image_path = image_path.replace("/media", "media")

    # Provide the path to the image you want to classify
    predicted_label = prediction(image_path)

    # Get the description corresponding to the predicted label
    predicted_description = label_descriptions.get(predicted_label, "Description not available.")
    prevention = prevention_methods.get(predicted_label, "Prevention Not Found.")
    

    contex = {
        'image': img,
        'predicted_label': predicted_label,
        # 'confidence': confidence,
        'predicted_description': predicted_description,
        'prevention' : prevention
    }
    return render(request, 'predict.html', contex)


import requests
from django.http import JsonResponse
from django.shortcuts import render

def news(request):
    return render(request, "news.html", {'navbar': 'home'})

def search_news(request):
    query = request.GET.get('query', '')

    if not query:
        return JsonResponse([])  # Return an empty JSON response if no query is provided

    # Fetch news from an API (replace with an actual API)
    api_url = f"https://newsapi.org/v2/everything?q={query}&apiKey=ef1fdd0440c648f286f01347733fc54d"
    
    try:
        response = requests.get(api_url)
        data = response.json()

        articles = []
        if data.get("status") == "ok":
            for article in data.get("articles", []):
                articles.append({
                    "title": article.get("title"),
                    "description": article.get("description"),
                    "url": article.get("url"),
                })

        return JsonResponse(articles, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def upload_crop_image(request):
    if request.method == 'POST':
        image_file = request.FILES.get('crop_image')
        quantity = request.POST.get('quantity')
        
        if image_file and quantity:
            img = image_data(user=request.user,Images=image_file, quantity=int(quantity))
            img.save()
            messages.success(request, "Image uploaded successfully!")
            return redirect('e_market')  # Redirect after upload
    return render(request, 'upload_crop_image.html')


def vendor_dashboard(request):
    vendor_id = request.session.get('vendor_id')
    if not vendor_id:
        messages.error(request, "Please log in first.")
        return redirect("vendor_log_in")

    vendor = Vendor.objects.get(id=vendor_id)
    images = image_data.objects.all().select_related('user')

    cart_ids = request.session.get('cart', [])
    cart_items = image_data.objects.filter(id__in=cart_ids)

    return render(request, "vendor_dashboard.html", {
        'vendor': vendor,
        'images': images,
        'cart_items': cart_items
    })


def vendor_register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone_number = request.POST['phone_number']
        email = request.POST['username']
        password = request.POST['password']
        password1 = request.POST['password1']

        if password != password1:
            messages.error(request, "Passwords do not match.")
            return redirect("vendor_register")

        if Vendor.objects.filter(email=email).exists():
            messages.error(request, "Vendor with this email already exists.")
            return redirect("vendor_register")

        vendor = Vendor(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            password=password  # 🔐 Consider hashing this
        )
        vendor.save()

        messages.success(request, "Vendor registration successful.")
        return redirect("vendor_log_in")

    return render(request, "vendor_register.html")

# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Vendor

def vendor_log_in(request):
    if request.method == "POST":
        email = request.POST['username']  # Same as 'username' in your form
        password = request.POST['password']

        try:
            vendor = Vendor.objects.get(email=email, password=password)
            request.session['vendor_id'] = vendor.id  # Store vendor ID in session
            messages.success(request, "Vendor login successful.")
            return redirect("vendor_dashboard")  # Redirect to dashboard
        except Vendor.DoesNotExist:
            messages.error(request, "Invalid email or password.")
            return redirect("vendor_log_in")

    return render(request, "vendor_log_in.html")


def add_to_cart(request, item_id):
    if request.method == "POST":
        cart = request.session.get('cart', [])
        if item_id not in cart:
            cart.append(item_id)
        request.session['cart'] = cart
        messages.success(request, "Item added to cart.")
    return redirect('vendor_dashboard')