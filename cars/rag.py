#As blibioteca usadas:
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition

#Maquina para fazer o embeddi
embedder = SentenceTransformer('all-MiniLM-L6-v2')

#Banco vetorial
client = QdrantClient(host='localhost', port= 6333)

#Vou embeddar as bios
COLLECTION = 'cars_bio'

#Aqui eu vejo se a colecao ja existe
def garantir_colecao():
    #pegando o banco vetorial:
    colecoes = [c.name for c in client.get_collections().collections]
    #Aqui eu crio uma bio no banco vetorial caso ela nao exista.
    if COLLECTION not in colecoes:
        client.create_collection(
            collection_name = COLLECTION,
            vectors_config = VectorParams(size = 384, distance=Distance.COSINE),
        )

def vetorizar_e_salvar(car):
     #Vejo se ja existe a colecao.
    garantir_colecao()
    #Junto todas as informacoes do carro em uma variavel
    texto = f"{car.brand} {car.model} {car.model_year or ''} {car.bio or ''}"
    #E transformo tudo em vetor
    vetor = embedder.encode(texto).tolist()

    #configuracoes do Qdrante:
    client.upsert(
        collection_name=COLLECTION,
        points = [PointStruct(
            id = car.id,
            vector = vetor,
            payload = {
                'car_id':  car.id,
                'nome':    f'{car.brand} {car.model}',
                'value':   car.value,
                'bio':     car.bio,
                'ano':     car.model_year,
            }
        )]
    )

#Remove do banco vetorial pelo id 
def remover_vetor(car_id):
        client.delete(
        collection_name = COLLECTION,
        points_selector = [car_id]
    )

#Aqui Ele Transforma a pergunta em vetor para fazer a assimilacao
#Vira uma skill uma ferramneta de busca
def buscar_carros(pergunta, limite=4):
    garantir_colecao()
    
    vetor = embedder.encode(pergunta).tolist()
    
    resultado = client.query_points(
        collection_name=COLLECTION,
        query=vetor,
        limit=limite,
    )
    
    return [r.payload for r in resultado.points]





