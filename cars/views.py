from django.shortcuts import render, redirect
from cars.models import Car
from cars.forms import CarForm
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from cars.chatbot import chat_ollama, chat_gemini

# Create your views here.
#crie sua funcao view aqui (request)

from django.contrib.auth.models import User
from cars.models import Car, Brand

def base(request):
    featured_cars = Car.objects.order_by('-id')[:5]
    total_cars    = Car.objects.count()
    total_brands  = Brand.objects.count()
    total_users   = User.objects.count()

    return render(request, 'base.html', {
        'featured_cars': featured_cars,
        'total_cars':    total_cars,
        'total_brands':  total_brands,
        'total_users':   total_users,
    })

#==================================================================================================#

def cars_view(request):
    cars = Car.objects.all()
    
    #aqui eu boto pra aparecer todos os carros mas se colocar
    #o search ele vai filtrar os carros de acordo com o modelo
    search = request.GET.get('search')
    if search:
        cars = Car.objects.filter(model__icontains=search).order_by('model')   

    return render(
        request, 
        'cars.html',
        {'cars':cars}
        )


class Cars_view(ListView):
    model = Car
    template_name = 'cars.html'
    context_object_name = 'cars'

    def get_queryset(self):
        cars = super().get_queryset().order_by('model')
        search = self.request.GET.get('search')
        if search:
            cars = cars.filter(model__icontains = search)
        return cars



#   C B V  = Views em forma de classes mais facil de entender
# Mas eh mais dificil de entender para iniciantes
class CarsView(View):  
    def get(self, request):
        cars = Car.objects.all()
        #aqui eu boto pra aparecer todos os carros mas se colocar
        #o search ele vai filtrar os carros de acordo com o modelo
        search = request.GET.get('search')
        if search:
            cars = Car.objects.filter(model__icontains=search).order_by('model')   

        return render(
            request, 
            'cars.html',
            {'cars':cars}
            )

#==============================================================================================#

#==============================================================================================#

@login_required
def Car_infor(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    back_url = request.META.get('HTTP_REFERER', '/cars/')
    return render(request, 'car_infor.html', {'car': car, 'back_url':back_url})

#==============================================================================================#


#==============================================================================================#
@login_required
def add_car(request):
    if request.method == 'POST':
        add_car_form = CarForm(request.POST, request.FILES)
        if add_car_form.is_valid():
            car = add_car_form.save(commit=False)
            car.dono = request.user
            car.save()
            print(f"{request.user} adicionou o carro {car.model} com a placa {car.plate}")
            return redirect('cars_view')  
    else:
        add_car_form = CarForm()
    
    return render(request,
            'add_car.html',
            {'add_car_form' : add_car_form})

#=================================================================================================#   
@login_required
def car_updateView(request, car_id):
    car = get_object_or_404(Car, id = car_id, dono = request.user)

    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            return redirect('car_infor', car_id = car_id)
    else:
        form = CarForm(instance=car)

    return render(request, 'car_update.html', {'form': form, 'car': car})

@login_required
def car_delete(request, car_id):
    car = get_object_or_404(Car, id=car_id, dono=request.user)
    if request.method == 'POST':
        car.delete()
    return redirect('my_cars')

@login_required
def my_cars(request):
    cars = Car.objects.filter(dono=request.user)
    search = request.GET.get('search')
    if search:
        cars = cars.filter(model__icontains=search).order_by('model')
    return render(request, 'my_cars.html', {'cars': cars})
#==================================================================================================#

def chatbot_view(request):
    if request.method == 'POST':
        data     = json.loads(request.body)
        pergunta = data.get('message', '')
        historico = data.get('history', [])
        provider  = data.get('provider', 'ollama')

        try:
            if provider == 'gemini':
                resposta = chat_gemini(historico, pergunta)
            else:
                resposta = chat_ollama(historico, pergunta)
        except Exception as e:
            resposta = f"Erro: {str(e)}"

        return JsonResponse({'response': resposta})

    return JsonResponse({'error': 'Método não permitido'}, status=405)