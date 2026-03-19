# 🚗 Savi Garagem

Plataforma web de compra e venda de veículos desenvolvida com Django. Permite que usuários cadastrem, editem e gerenciem anúncios de carros com geração automática de descrições por IA.

---

## ✨ Funcionalidades

- **Autenticação completa** — cadastro, login e logout de usuários
- **CRUD de veículos** — cadastrar, visualizar, editar e deletar carros
- **Bio gerada por IA** — descrição automática via Ollama (llama3.2) ao cadastrar um carro
- **Otimização de imagens** — múltiplas resoluções geradas automaticamente com django-imagekit
- **Busca e filtro** — busca por modelo e filtro por faixa de preço
- **Contato entre usuários** — envio de email diretamente pelo anúncio
- **Garagem pessoal** — página exclusiva com os carros do usuário logado
- **Signals automáticos** — inventário atualizado a cada cadastro/remoção
- **Tema claro/escuro** — alternância persistente via localStorage
- **Interface moderna** — dark industrial com Bebas Neue + DM Sans

---

## 🛠️ Stack

| Tecnologia | Uso |
|---|---|
| Django 6.0 | Framework principal |
| PostgreSQL | Banco de dados |
| Python 3.14 | Linguagem |
| Pillow | Processamento de imagens |
| django-imagekit | Otimização e redimensionamento de fotos |
| Ollama (llama3.2) | Geração de bio por IA (local, gratuito) |
| psycopg2 | Driver PostgreSQL |
| python-dotenv | Variáveis de ambiente |

---

## 🚀 Como rodar localmente

### Pré-requisitos

- Python 3.10+
- PostgreSQL
- Ollama instalado — [ollama.com](https://ollama.com)

### Instalação

```bash
# Clone o repositório
git clone https://github.com/Saviozii/Projeto_Django
cd Projeto_Django

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
# edite o .env com suas credenciais

# Rode as migrations
python manage.py migrate

# Crie um superusuário (opcional)
python manage.py createsuperuser

# Inicie o servidor
python manage.py runserver
```

### Ollama (IA local)

```bash
# Instale o Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Baixe o modelo
ollama pull llama3.2
```

---

## ⚙️ Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com base no `.env.example`:

```env
SECRET_KEY=sua_secret_key_aqui
DEBUG=True

DB_NAME=nome_do_banco
DB_USER=usuario_postgres
DB_PASSWORD=senha_postgres
DB_HOST=localhost
DB_PORT=5432

OPENAI_API_KEY=opcional_se_usar_openai
```

---

## 📁 Estrutura do projeto

```
Projeto_Django/
├── app/                  # configurações principais (settings, urls)
├── cars/                 # app principal
│   ├── models.py         # Car, Brand, Inventory
│   ├── views.py          # todas as views
│   ├── forms.py          # CarForm com validações
│   ├── signals.py        # pre_save e post_save
│   └── templates/        # HTMLs
├── acounts/              # autenticação
│   └── views.py          # login, register, logout
├── media/                # uploads (não versionado)
├── .env                  # variáveis sensíveis (não versionado)
├── .env.example          # template do .env
├── .gitignore
├── manage.py
└── requirements.txt
```

---

## 📸 Models

```python
class Car(models.Model):
    model        = CharField
    brand        = ForeignKey(Brand)
    factory_year = IntegerField
    model_year   = IntegerField
    plate        = CharField
    value        = FloatField
    photo        = ImageField
    dono         = ForeignKey(User)
    bio          = TextField  # gerado por IA
```

---

## 🤖 Como funciona a IA

Ao cadastrar um carro, um `pre_save` signal dispara automaticamente e chama o Ollama localmente para gerar uma descrição de venda baseada na marca, modelo e ano. Nenhuma API paga é necessária.

```python
@receiver(pre_save, sender=Car)
def car_pre_save(sender, instance, **kwargs):
    if not instance.bio:
        instance.bio = get_car_ai_bio(
            instance.model, instance.brand, instance.model_year
        )
```

---

## 📄 Licença

MIT License — sinta-se livre para usar e modificar.

---

Desenvolvido por [@Saviozii](https://github.com/Saviozii)
