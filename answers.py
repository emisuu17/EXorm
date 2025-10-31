from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from models import Base, Produto  # Importe o MODELO 'Produto', não a lista

# --- Configuração da Sessão (Necessário para este script rodar) ---
engine = create_engine('sqlite:///exercicios.db')
Session = sessionmaker(bind=engine)
# ----------------------------------------------------------------

print("--- Consultando todos os produtos no banco de dados ---")

# Abre uma nova sessão
with Session() as session:
    # 1. A consulta é feita sobre a CLASSE 'Produto'
    query = select(Produto)

    # 2. Use .scalars() para obter os objetos 'Produto' diretamente
    #    (Em vez de tuplas 'Row' que o .execute() retorna)
    #    .all() executa a query e retorna uma lista
    lista_de_produtos = session.scalars(query).all()

    # 3. Nomes de variáveis mais claros no loop
    for produto_obj in lista_de_produtos:
        # Imprime o objeto, usando o método __str__ que definimos
        print(produto_obj)