from sqlalchemy import create_engine, select,func
from sqlalchemy.orm import sessionmaker
from models import Base, Produto, Usuario, Pedido  # Importe o MODELO 'Produto', não a lista

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

with Session() as session:
    query = select(Usuario).where(Usuario.ativo)
    idade = session.execute(query).scalars()

    for idade_obj in idade:
        print(idade_obj)

with Session() as session:
    query = select(Pedido).where(Pedido.quantidade > 5)
    pedidos = session.execute(query).scalars()

    for pedido_obj in pedidos:
        print(pedido_obj)


 # --- questão 4 ---
with Session() as session:
    query = select(Usuario).where(Usuario.id)
    Usu = session.execute(query).scalars().first()

    if Usu:
        print(f'primeiro usuario: {Usu.nome},id:{Usu.id}')
    
    else:
        print('não encontrado')
  

