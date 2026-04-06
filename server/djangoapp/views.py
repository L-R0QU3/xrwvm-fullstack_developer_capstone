# Uncomment the required imports before adding the code

# from django.shortcuts import render
# from django.http import HttpResponseRedirect, HttpResponse
# from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404, render, redirect
# from django.contrib.auth import logout
# from django.contrib import messages
# from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from .models import CarMake, CarModel
from .populate import initiate
from .restapis import get_request, post_review, analyze_review_sentiments
import json
# from .populate import initiate


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

@csrf_exempt
def logout_user(request):
    logout(request)
    return JsonResponse({"userName": ""})

@csrf_exempt
def registration(request):
    try:
        data = json.loads(request.body)
        username = data['userName']
        password = data['password']
        first_name = data['firstName']
        last_name = data['lastName']
        email = data['email']
        
        # Verificar si el usuario ya existe
        from django.contrib.auth.models import User
        if User.objects.filter(username=username).exists():
            return JsonResponse({"userName": username, "error": "Already Registered"})
        
        # Crear nuevo usuario
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        # Iniciar sesión automáticamente después del registro
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

def get_cars(request):
    count = CarMake.objects.filter().count()
    if count == 0:
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({
            "CarModel": car_model.name,
            "CarMake": car_model.car_make.name,
            "Year": car_model.year,
            "Type": car_model.type,
            "DealerId": car_model.dealer_id
        })
    return JsonResponse({"CarModels": cars})


def get_dealerships(request, state="All"):
    """
    Proxy para /fetchDealers (todos) o /fetchDealers/:state
    """
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = f"/fetchDealers/{state}"
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})

def get_dealer_details(request, dealer_id):
    """
    Proxy para /fetchDealer/<dealer_id>
    """
    if dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    else:
        return JsonResponse({"status": 400, "message": "Bad request"}, status=400)

def get_dealer_reviews(request, dealer_id):
    """
    Obtiene reseñas del dealer desde /fetchReviews/dealer/<dealer_id>
    y agrega el campo 'sentiment' usando el microservicio.
    """
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)
        if reviews is None:
            reviews = []
        for review_detail in reviews:
            # Asumiendo que la reseña tiene un campo 'review' (texto)
            text = review_detail.get('review', '')
            sentiment_response = analyze_review_sentiments(text)
            review_detail['sentiment'] = sentiment_response.get('sentiment', 'neutral')
        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad request"}, status=400)

@csrf_exempt
def add_review(request):
    """
    Recibe una reseña en formato JSON (POST) y la envía al backend.
    Solo usuarios autenticados.
    """
    if not request.user.is_authenticated:
        return JsonResponse({"status": 403, "message": "Unauthorized"}, status=403)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            response = post_review(data)
            return JsonResponse({"status": 200, "message": "Review added"})
        except Exception as e:
            return JsonResponse({"status": 500, "message": f"Error: {str(e)}"}, status=500)
    else:
        return JsonResponse({"status": 405, "message": "Method not allowed"}, status=405)
