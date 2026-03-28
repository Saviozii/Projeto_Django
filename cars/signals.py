from django.dispatch import receiver
from cars.models import Car, inventory
from django.db.models import Sum
from openai_api.cliente import get_car_ai_bio_ollama, get_car_ai_bio_GPT
from django.contrib.auth.models import User
from django.db import connection
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from cars.models import Car
from cars.rag import vetorizar_e_salvar, remover_vetor
import ollama
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
#Ele so atualiza o inventario
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

@receiver(pre_save, sender=Car)
def car_pre_save(sender, instance, **kwargs):
    if not instance.bio:
        try:
            instrucao = f"""
            Crie uma descrição de venda persuasiva para o carro {instance.brand} {instance.model} {instance.model_year}.
            Destaque desempenho, conforto e diferencial do modelo.
            Máximo 250 caracteres. Seja específico e natural.
            Evite usar simbolos
            """

            response = ollama.chat(
                model='llama3.2',
                messages=[{'role': 'user', 'content': instrucao}]
            )

            conteudo = response.get('message', {}).get('content', '').strip()

            if conteudo:
                instance.bio = conteudo
            else:
                raise ValueError("Resposta vazia do modelo")

        except Exception as a:
            print("ERRO AO GERAR BIO:", a)
            instance.bio = f'{instance.brand} {instance.model} {instance.model_year or ""}'
#==================================================================#

@receiver(post_save, sender=Car)
def car_post_save(sender, instance, created, **kwargs):
    if instance.bio:
        vetorizar_e_salvar(instance)  # salva no Qdrant


@receiver(post_delete, sender=Car)
def car_post_delete(sender, instance, **kwargs):
    remover_vetor(instance.id)  # remove do Qdrant


@receiver(post_save, sender=User)
def usuario_cadastrado(sender, instance, created, **kwargs):
    if created:
        from django.db import connection
        db = connection.settings_dict['NAME']
        print(f'Usuário: {instance.username} | Banco: {db}')
