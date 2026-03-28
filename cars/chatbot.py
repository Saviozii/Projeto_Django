import ollama
import google.generativeai as genai
from django.conf import settings
from cars.rag import buscar_carros

SYSTEM_PROMPT = """Você é um assistente da Savi Garagem.
Sua única fonte de informação são os carros listados no "Catálogo relevante" abaixo.
REGRAS OBRIGATÓRIAS:
- NUNCA mencione carros que não estejam no catálogo fornecido.
- Se o catálogo estiver vazio ou nenhum carro for compatível, diga: "No momento não temos carros com esse perfil no catálogo."
- Não invente modelos, preços, anos ou especificações.
- Baseie TODAS as respostas exclusivamente nos carros do catálogo."""

def montar_contexto(resultados):
    if not resultados:
        return "Nenhum carro encontrado no catálogo."
    linhas = []
    for r in resultados:
        linha = f"- {r['nome']}"
        if r.get('ano'):   linha += f" ({r['ano']})"
        if r.get('value'): linha += f" — R$ {r['value']:,.0f}"
        if r.get('bio'):   linha += f"\n  {r['bio']}"
        linhas.append(linha)
    return "\n".join(linhas)



def chat_ollama(historico, pergunta):
    resultados = buscar_carros(pergunta)
    contexto   = montar_contexto(resultados)

    messages = [{'role': 'system', 'content': SYSTEM_PROMPT}]
    for msg in historico:
        messages.append(msg)
    messages.append({
    'role': 'user',
    'content': (
        f"CATÁLOGO DISPONÍVEL (use APENAS esses carros):\n{contexto}\n\n"
        f"PERGUNTA: {pergunta}\n\n"
        f"LEMBRETE: Só mencione carros que estão no catálogo acima."
    )
})

    response = ollama.chat(model='llama3.2', messages=messages)
    return response['message']['content']




def chat_gemini(historico, pergunta):
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

    resultados = buscar_carros(pergunta)
    contexto   = montar_contexto(resultados)

    historico_texto = ""
    for msg in historico:
        role = "Usuário" if msg['role'] == 'user' else "Assistente"
        historico_texto += f"{role}: {msg['content']}\n"

    prompt = f"""{SYSTEM_PROMPT}

    CATÁLOGO DISPONÍVEL (use APENAS esses carros):
    {contexto}

    Histórico:
    {historico_texto}
    Usuário: {pergunta}

    LEMBRETE: Só mencione carros que estão no catálogo acima.
    Assistente:"""

    response = model.generate_content(prompt)
    return response.text