from django.db.models.signals import pre_save, post_save, post_delete
#Essas sao as acoes sginals mais usada
from django.dispatch import receiver
from cars.models import Car, inventory
from django.db.models import Sum
from openai_api.cliente import get_car_ai_bio_ollama, get_car_ai_bio_GPT
from django.contrib.auth.models import User
from django.db import connection

#CALCULA TUDO DO ESTOQUE
def calcular_inventory():
    #Todos os carro no inventario
    total_car_signal = Car.objects.all().count()
    
    #O Valor total de todos os carros
    valor_total_car_signal = Car.objects.aggregate(
        valor_total = Sum('value'),
    )['valor_total']

    #Adicionando as informacoes no banco de dados inventario:
    inventory.objects.create(
        car_total=total_car_signal,
        car_valor=valor_total_car_signal,
    )


#Simples signal que executa depois de um post no banco de dados
@receiver(post_save, sender = Car)
def inventory_post(sender, instance, **kwargs):
    calcular_inventory()
    print(instance)


@receiver(post_delete, sender=Car)
def car_post_delet(sender, instance, **kwargs):
    calcular_inventory()


@receiver(post_save, sender=User)
def usuario_cadastrado(sender, instance, created, **kwargs):
    if created:
        db = connection.settings_dict['NAME']
        print(f'Novo usuário cadastrado: {instance.username} — banco: {db}')



#================================================================#
@receiver(pre_save, sender = Car)
def car_pre_save(sender, instance, **kwargs):
    if not instance.bio:
        try:
            ai_bio = get_car_ai_bio_ollama(instance.model, instance.brand, instance.model_year)
            instance.bio = ai_bio
        except Exception:
            instance.bio = f'{instance.brand} {instance.model} {instance.model_year}'