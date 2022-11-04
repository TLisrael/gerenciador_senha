import sqlite3
import dotenv
import os

# Carrega os valores do dotenv
dotenv.load_dotenv(dotenv.find_dotenv())



MASTER_PASSWORD = os.getenv("MASTER_PASSWORD")
senha = input(' Insira sua senha: ')
if senha != MASTER_PASSWORD:
    print('Senha inválida! Encerrando programa...')
    exit()

# Criando banco de dados
connection = sqlite3.connect('passwords.db')

cursor = connection.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    service TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);
 ''')

#Função menu
def menu():
    print("******************************************")
    print("* i : inserir nova senha *")
    print("* l : listar serviços salvos *")
    print("* r : recuperar uma senha *")
    print("* s : sair  *")
    print("******************************************")
    
def get_password(service):
    cursor.execute(f'''
                    SELECT username, password FROM users
                    WHERE service = '{service}'
                    ''')
        
    if cursor.rowcount == 0:
        print('Serviço não cadastrado. Use "l" para verificar todos os serviços. ')
    else:
        for user in cursor.fetchall():
            print(user)

def insert_password( service, username, password):
    cursor.execute(f'''
                   INSERT INTO users (service, username, password) 
                   VALUES ('{service}', '{username}', '{password}')
                   ''')
    connection.commit()

def show_services():
    cursor.execute('''
                   SELECT service FROM users;
                   ''')
    for service in cursor.fetchall():
        print(service)
while True:
    menu()
    op = input('O que deseja fazer? ')
    if op not in ['l', 'i', 'r', 's']:
        print('Essa opção é inválida.')
        continue
    
    if op == 's':
        break
    
    if op == 'i':
        service = input('Qual o nome do serviço? ')
        username = input('Qual o nome do usuario? ')
        password = input('Qual a senha? ')
        insert_password(service, username, password)
        
        
    if op == 'l':
        show_services()
        
    if op == 'r':
        service = input('Qual serviço deseja obter a senha? ')
        get_password(service)
        
connection.close()