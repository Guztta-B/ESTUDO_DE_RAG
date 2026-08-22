from groq import Groq
import os
import sqlite3



client =  Groq(api_key = os.environ.get("GROQ_API _KEY", "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"))



conn =  sqlite3.connect(":memory:")


cursor =  conn.cursor()


cursor.execute("CREATE TABLE IF NOT EXISTS pedidos(id INT, cliente TEXT, valor REAL, status TEXT)")


cursor.execute("INSERT INTO pedidos VALUES (100,'Ana', 250.00,'Entregue')")
cursor.execute("INSERT INTO pedidos VALUES (101,'Bruna', 5000.00,'em Transito')")
cursor.execute("INSERT INTO pedidos VALUES (102,'Carlos', 5000.00,'Separação')")
cursor.execute("INSERT INTO pedidos VALUES (103,'Carlos', 5000.00,'Separação')")
cursor.execute("INSERT INTO pedidos VALUES (104,'José', 5000.00,'Separação')")
conn.commit()



perguntarr = input('Pergunter sim ou não: ')


while perguntarr:
    pergunta =  input('Pergunte: ')
 
    



    # Retrivel 
    
    id_ = int(input('ID: ')) 


    cursor.execute("SELECT cliente, valor, status FROM pedidos WHERE id = ?", (id_,))
    dados =  cursor.fetchone()


    print(dados)



    # Argumentation
    contexto = f'cliente - {dados[0]} valor - {dados[1]} status {dados[2]}'




    # Generation 
    promp_rag = f'''
                Responda perguntas do usuário utilizando apenas o contexto fonecido abaixo.
                Contexto do banco de dados:
                {contexto}
                pergunta: {pergunta}
                ''' 


chat_completion = client.chat.completions.create(
messages = [


    {"role":"user", "content":promp_rag}
], model = "openai/gpt-oss-20b" 


)



print(chat_completion.choices[0].message.content)


conn.close()


print('Digite um id existente')    