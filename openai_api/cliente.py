import openai
import ollama
#=================================================================================================================#
#                           MODELO OPEN AI                                                                        #
def get_car_ai_bio_GPT(model, brand, year):
    openai.api_key = 'key'

    instrucao = f'''Me mostre uma descrição de venda para o carro {brand} {model} {year} em apenas 250 caracteres.
     Fale coisas específicas desse modelo de carro.'''

    response = openai.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {'role': 'user', 'content': instrucao}
        ],
        max_tokens=1000,
    )

    return response.choices[0].message.content
#=================================================================================================================#

#=================================================================================================================#
#                           MOLEDO OLLAMA (TESTE LOCAL)                                                           #

def get_car_ai_bio_ollama(model, brand, year):
    instrucao = f'''Me mostre uma descrição de venda para o carro {brand} {model} {year} em apenas 250 caracteres.
     Fale coisas específicas desse modelo de carro. Responda apenas com a descrição, sem explicações.'''

    response = ollama.chat(
        model='llama3.2',
        messages=[
            {'role': 'user', 'content': instrucao}
        ]
    )

    return response['message']['content']

