import streamlit as st
import requests
from bs4 import BeautifulSoup
from groq import Groq

# Configuração da página
st.set_page_config(
    page_title="Consulta de Unidades",
    page_icon="🏫",
    layout="centered"
)

# Estilo visual limpo e minimalista
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton button {
        width: 100%;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Função de scraping com cache para otimizar a navegação
@st.cache_data(ttl=3600)
def carregar_dados_site():
    url = "https://gratuitos.netlify.app/"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove elementos desnecessários se houver
        for script in soup(["script", "style"]):
            script.extract()
            
        texto_limpo = soup.get_text(separator="\n")
        linhas = [linha.strip() for linha in texto_limpo.splitlines() if linha.strip()]
        return "\n".join(linhas)
    except Exception as e:
        return f"Erro ao carregar dados do site: {e}"

# Interface do Usuário
st.title("🏫 Consulta de Unidades")
st.write("Digite sua dúvida abaixo para encontrar endereços e informações das unidades.")

# Campo de texto para a pergunta
pergunta = st.text_input("O que você deseja saber?", placeholder="Ex: Qual o endereço da unidade centro?")

botao = st.button("Buscar Unidade / Perguntar")

if botao:
    if not pergunta.strip():
        st.warning("Por favor, digite uma dúvida antes de buscar.")
    else:
        with st.spinner("Consultando informações..."):
            # Obtém o conteúdo raspado
            contexto = carregar_dados_site()
            
            # Validação da chave da API via st.secrets
            if "GROQ_API_KEY" not in st.secrets:
                st.error("A chave GROQ_API_KEY não foi configurada nos segredos do Streamlit.")
            else:
                try:
                    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                    
                    prompt_sistema = (
                        "Você é um assistente útil para estudantes. "
                        "Responda à dúvida do usuário com base estritamente no contexto fornecido abaixo. "
                        "Se a resposta não estiver no contexto, informe educadamente que não encontrou a informação."
                    )
                    
                    chat_completion = client.chat.completions.create(
                        model="openai/gpt-oss-20b",  # Alterado para um modelo ativo
                        messages=[
                            {"role": "system", "content": f"{prompt_sistema}\n\nContexto:\n{contexto}"},
                            {"role": "user", "content": pergunta}
                        ],
                        temperature=0.3,
                        max_tokens=1024
                    )
                    
                    resposta = chat_completion.choices[0].message.content
                    
                    st.markdown("---")
                    st.subheader("Resposta:")
                    st.write(resposta)
                    
                except Exception as e:
                    st.error(f"Ocorreu um erro ao processar sua solicitação: {e}")