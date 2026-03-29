# 🚗 Savi Garagem

Plataforma web de compra e venda de veículos com chatbot de recomendação por IA, desenvolvida com Django.

---

## ✨ Funcionalidades

- **Autenticação completa** — cadastro, login e logout de usuários
- **CRUD de veículos** — cadastrar, visualizar, editar e deletar carros
- **Bio gerada por IA** — descrição automática via Ollama ao cadastrar um carro
- **Chatbot com RAG** — assistente inteligente que recomenda carros do catálogo usando busca vetorial
- **Banco vetorial** — Qdrant armazena as bios dos carros como vetores para busca semântica
- **Dois modelos de IA** — Ollama local (gratuito) e Gemini (Google)
- **Otimização de imagens** — múltiplas resoluções com django-imagekit
- **Busca e filtro por preço** — client-side sem recarregar a página
- **Garagem pessoal** — página exclusiva com os carros do usuário logado
- **Signals automáticos** — bio gerada e vetor salvo automaticamente ao cadastrar
- **Tema claro/escuro** — alternância persistente via localStorage
- **Interface moderna** — dark industrial com Bebas Neue + DM Sans

---

## 🛠️ Stack

| Tecnologia | Uso |
|---|---|
| Django 6.0 | Framework principal |
| PostgreSQL | Banco de dados relacional |
| Qdrant | Banco de dados vetorial |
| sentence-transformers | Geração de embeddings |
| Ollama (llama3.2) | IA local para bio e chatbot |
| Google Gemini | IA cloud para chatbot |
| django-imagekit | Otimização de imagens |
| Pillow | Processamento de imagens |
| psycopg2 | Driver PostgreSQL |
| python-dotenv | Variáveis de ambiente |
| Docker | Container do Qdrant |

---

## 🚀 Como rodar localmente

### Pré-requisitos

- Python 3.10+
- PostgreSQL
- Docker
- Ollama — [ollama.com](https://ollama.com)

### 1 — Clone e instale

```bash
git clone https://github.com/Saviozii/Projeto_Django
cd Projeto_Django

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

### 2 — Configure o ambiente

```bash
cp .env.example .env
# edite o .env com suas credenciais
```

### 3 — Suba o Qdrant com Docker

```bash
docker run -d -p 6333:6333 -v qdrant_storage:/qdrant/storage qdrant/qdrant
```

### 4 — Configure o Ollama

```bash
ollama pull llama3.2
ollama serve
```

### 5 — Rode as migrations e o servidor

```bash
python manage.py migrate
python manage.py runserver
```

### 6 — Indexe os carros no Qdrant

```bash
python manage.py shell -c "
from cars.models import Car
from cars.rag import vetorizar_e_salvar
for car in Car.objects.filter(bio__isnull=False):
    vetorizar_e_salvar(car)
    print(f'Indexado: {car}')
"
```

---

## ⚙️ Variáveis de ambiente

```env
SECRET_KEY=
DEBUG=True

DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=5432

GEMINI_API_KEY=
```

Pegue sua chave do Gemini gratuitamente em [aistudio.google.com/apikey](https://aistudio.google.com/apikey).

---

## 🤖 Como funciona o RAG

```
Usuário cadastra carro
        ↓
post_save signal dispara
        ↓
bio gerada pelo Ollama
        ↓
sentence-transformers transforma a bio em vetor
        ↓
vetor salvo no Qdrant

Usuário pergunta no chat
        ↓
pergunta vira vetor
        ↓
Qdrant busca vetores mais próximos (similaridade semântica)
        ↓
LLM responde usando APENAS os carros encontrados
```

---

## 📁 Estrutura

```
Projeto_Django/
├── app/              # settings, urls
├── cars/
│   ├── models.py     # Car, Brand, Inventory
│   ├── views.py      # views + chatbot_view
│   ├── forms.py      # CarForm com validações
│   ├── signals.py    # bio + vetorização automática
│   ├── rag.py        # Qdrant — indexar e buscar
│   ├── chatbot.py    # Ollama + Gemini + RAG
│   └── templates/
│       ├── cars.html
│       ├── car_infor.html
│       ├── car_update.html
│       ├── my_cars.html
│       ├── add_car.html
│       ├── base.html
│       └── chatbot.html
├── acounts/          # login, register, logout
├── .env.example
├── .gitignore
└── manage.py
```

---

## 📄 Licença

MIT License

---

Desenvolvido por [@Saviozii](https://github.com/Saviozii)
