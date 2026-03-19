
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from cars.views import cars_view, base ,add_car, CarsView, Cars_view, Car_infor
from cars.views import car_updateView, my_cars, car_delete
from acounts.views import register_view, login_view, logout_view
#funcao_view (request) aqui 


urlpatterns = [
    path('', base , name='base'),
    path('register/', register_view , name = 'register'),
    path('login/', login_view, name = 'login'),
    path('logout/', logout_view, name = 'logout'),
    path('admin/', admin.site.urls, name = 'admin'),
    path('cars/', Cars_view.as_view(), name='cars_view'),#uma funcao) o nome eh importante
    path('my_cars/', my_cars, name='my_cars'),
    path('cars/<int:car_id>/delete/', car_delete, name='car_delete'),
    path('cars/<int:car_id>/', Car_infor, name = 'car_infor'),
    path('cars/update_car/<int:car_id>/',car_updateView, name = 'car_update'),
    path('add_car/',add_car, name='add_car'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
