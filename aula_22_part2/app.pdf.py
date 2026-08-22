from groq import Groq
import os
import pypdf



client =  Groq(api_key = os.environ.get("GROQ_API _KEY", "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"))



def ler_texto_pdf(caminho_pdf):


    reader = pypdf.PdfReader('p.pdf')
    text_completo = ''
    for page in reader.pages:
        text_completo += page.extract_text() or ""
    return text_completo



# print(ler_texto_pdf('arquivo_.pdf'))


# retrievel


contexto_pdf  =  ler_texto_pdf('p.pdf')
pergunta  =  input('Pergunta: ')


# base RAG:  GENERATIONS 


prompt_rag =  f'''


{contexto_pdf}
pergunta: {pergunta}


'''


chat_completion = client.chat.completions.create(
messages = [


    {"role":"user", "content":prompt_rag}
], model = "openai/gpt-oss-20b" 


)



print(chat_completion.choices[0].message.content)


