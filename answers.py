from sqlalchemy import create_engine, select,desc,distinct,func,exists
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models import Base, Produto, Usuario, Pedido  # Importe o MODELO 'Produto', não a lista

# --- Configuração da Sessão (Necessário para este script rodar) ---
engine = create_engine('sqlite:///exercicios.db')
Session = sessionmaker(bind=engine)
# ----------------------------------------------------------------

print("--- Consultando todos os produtos no banco de dados ---")

with Session() as session:
    
    query = select(Produto)
    lista_de_produtos = session.scalars(query).all()

    for produto_obj in lista_de_produtos:
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

print("--- 5. Produto mais barato da categoria 'eletrônicos' ---")

with Session() as session:
    query_barato = select(Produto).where(
        Produto.categoria == 'eletrônicos'
    ).order_by(Produto.preco)


    produto_mais_barato = session.execute(query_barato).scalars().first()

    if produto_mais_barato:
        print(f"O produto eletrônico mais barato é: {produto_mais_barato.nome}")
        print(f"Preço: R$ {produto_mais_barato.preco:.2f}")
    else:
        print("Nenhum produto da categoria 'eletrônicos' foi encontrado.")


print("\n--- 6. Último pedido realizado ---")

with Session() as session:

    query_ultimo = select(Pedido, Usuario.nome).join(
        Usuario, Pedido.usuario_id == Usuario.id
    ).order_by(
        desc(Pedido.data_pedido) 
    )
    ultimo_pedido_info = session.execute(query_ultimo).first()

    if ultimo_pedido_info:
        ultimo_pedido = ultimo_pedido_info[0] 
        nome_usuario = ultimo_pedido_info[1]  

        print(f"O último pedido foi feito em: {ultimo_pedido.data_pedido.strftime('%Y-%m-%d')}")
        print(f"Usuário: {nome_usuario} (ID: {ultimo_pedido.usuario_id})")
        print(f"Produto ID: {ultimo_pedido.produto_id}")
        print(f"Status: {ultimo_pedido.status}")
    else:
        print("Nenhum pedido encontrado no banco de dados.")

print("--- 7. Recupere os dados completos do usuário com ID 7 ---")

with Session() as session:
    usuario_7 = session.get(Usuario, 7)

    if usuario_7:
        print(f"ID: {usuario_7.id}")
        print(f"Nome: {usuario_7.nome}")
        print(f"E-mail: {usuario_7.email}")
        print(f"Idade: {usuario_7.idade}")
        print(f"Ativo: {usuario_7.ativo}")
    else:
        print("Usuário com ID 7 não encontrado.")

print("--- 8. Verifique se existe um produto com ID 5 e estoque positivo. ---")

with Session() as session:
    query_8 = select(Produto).where(
        Produto.id == 5,
        Produto.estoque > 0
    )
    
 
    produto_8 = session.execute(query_8).scalars().first()

    if produto_8:
        print(f"Sim, o produto '{produto_8.nome}' (ID 5) existe e tem estoque positivo ({produto_8.estoque} unidades).")
    else:
    
        print("Não, o produto com ID 5 não existe ou não possui estoque positivo.")


print("\n--- 9. Obtenha o pedido de ID 3 junto com os dados do usuário associado. ---")

with Session() as session:
    query_9 = select(Pedido, Usuario).where(
        Pedido.id == 3
    ).join(
        Usuario, Pedido.usuario_id == Usuario.id
    )

    resultado_9 = session.execute(query_9).first()

    if resultado_9:
        pedido = resultado_9.Pedido   
        usuario = resultado_9.Usuario 
        print("Dados do Pedido:")
        print(f"  ID: {pedido.id}")
        print(f"  Status: {pedido.status}")
        print(f"  Data: {pedido.data_pedido.strftime('%Y-%m-%d')}")
        print(f"  Produto ID: {pedido.produto_id}")
        print("Dados do Usuário Associado:")
        print(f"  ID: {usuario.id}")
        print(f"  Nome: {usuario.nome}")
        print(f"  Email: {usuario.email}")
    else:
        print("Pedido com ID 3 não encontrado.")

print("--- 10.Encontre usuários com idade entre 25 e 35 anos. ---")

with Session() as session:
    query_10 = select(Usuario).filter(
        Usuario.idade.between(25, 35)
    ).order_by(Usuario.idade)

    usuarios_10 = session.execute(query_10).scalars().all()

    if usuarios_10:
        print("Usuários encontrados (idade 25-35):")
        for usuario in usuarios_10:
            print(f"  - ID: {usuario.id}, Nome: {usuario.nome}, Idade: {usuario.idade}")
    else:
        print("Nenhum usuário encontrado nessa faixa de idade.")


print("\n--- 11.Liste pedidos com status 'cancelado' ou 'pendente' feitos depois de 2024. ---")

with Session() as session:
    data_limite = datetime(2024, 12, 31)
    query_11 = select(Pedido).filter(
        Pedido.status.in_(['cancelado', 'pendente']), 
        Pedido.data_pedido > data_limite            
    ).order_by(Pedido.data_pedido)

    pedidos_11 = session.execute(query_11).scalars().all()

    if pedidos_11:
        print("Pedidos 'cancelados' ou 'pendentes' feitos depois de 2024:")
        for pedido in pedidos_11:
            print(f"  - ID: {pedido.id}, Status: {pedido.status}, Data: {pedido.data_pedido.strftime('%Y-%m-%d')}")
    else:
        print("Nenhum pedido encontrado com esses critérios.")


print("\n--- 12.Selecione produtos com preço acima de R$ 500 que tiveram pelo menos 1 pedido. ---")

with Session() as session:
    query_12 = select(Produto).join(
        Pedido, Produto.id == Pedido.produto_id
    ).filter(
        Produto.preco > 500
    ).distinct().order_by(Produto.id)

    produtos_12 = session.execute(query_12).scalars().all()
    if produtos_12:
        print("Produtos com preço > R$ 500 e que possuem pedidos:")
        for produto in produtos_12:
            print(f"  - ID: {produto.id}, Nome: {produto.nome}, Preço: R$ {produto.preco:.2f}")
    else:
        print("Nenhum produto encontrado com esses critérios.")

print("--- 13.Busque todos os usuários com status inativo. ---")

with Session() as session:
    query_13 = select(Usuario).filter_by(ativo=False)
    
    usuarios_13 = session.execute(query_13).scalars().all()

    if usuarios_13:
        print("Usuários inativos encontrados:")
        for usuario in usuarios_13:
            print(f"  - ID: {usuario.id}, Nome: {usuario.nome} (Ativo: {usuario.ativo})")
    else:
        print("Nenhum usuário inativo encontrado.")


print("\n--- 14.Produtos 'livros' com preço < R$ 100. ---")

with Session() as session:
    query_14 = select(Produto).filter_by(
        categoria='livros' 
    ).filter(
        Produto.preco < 100 
    )

    produtos_14 = session.execute(query_14).scalars().all()

    if produtos_14:
        print("Livros com preço inferior a R$ 100,00:")
        for produto in produtos_14:
            print(f"  - ID: {produto.id}, Nome: {produto.nome}, Preço: R$ {produto.preco:.2f}")
    else:
        print("Nenhum livro encontrado com esses critérios.")


print("\n--- 15.Obtenha os 3 produtos mais caros com estoque disponível. ---")

with Session() as session:
    query_15 = select(Produto).filter(
        Produto.estoque > 0
    ).order_by(
        desc(Produto.preco) 
    ).limit(3) 
    produtos_15 = session.execute(query_15).scalars().all()

    if produtos_15:
        print("Os 3 produtos mais caros com estoque:")
        for produto in produtos_15:
            print(f"  - Nome: {produto.nome}, Preço: R$ {produto.preco:.2f}, Estoque: {produto.estoque}")
    else:
        print("Nenhum produto com estoque disponível encontrado.")

print("--- 16. Liste todos os usuários em ordem alfabética de nome. ---")

with Session() as session:
    query_16 = select(Usuario).order_by(Usuario.nome.asc())

    usuarios_16 = session.execute(query_16).scalars().all()

    print("Usuários em ordem alfabética:")
    for usuario in usuarios_16:
        print(f"  - {usuario.nome}")


print("\n--- 17. Ordene os produtos do mais caro para o mais barato. ---")

with Session() as session:
    query_17 = select(Produto).order_by(desc(Produto.preco))

    produtos_17 = session.execute(query_17).scalars().all()
    
    print("Produtos do mais caro para o mais barato:")
    for produto in produtos_17:
        print(f"  - {produto.nome} (R$ {produto.preco:.2f})")


print("\n--- 18. Organize os pedidos por status e depois data de criação (mais recentes primeiro). ---")

with Session() as session:
    query_18 = select(Pedido).order_by(
        Pedido.status.asc(),
        desc(Pedido.data_pedido)
    )

    pedidos_18 = session.execute(query_18).scalars().all()

    print("Pedidos ordenados por status e data (mais recente):")
    for pedido in pedidos_18:
        print(f"  - Status: {pedido.status.ljust(10)} | Data: {pedido.data_pedido.strftime('%Y-%m-%d')} | ID: {pedido.id}")
    
print("--- 19. Liste os 6 primeiros usuários cadastrados no sistema. ---")

with Session() as session:
    query_19 = select(Usuario).order_by(Usuario.id).limit(6)
    
    usuarios_19 = session.execute(query_19).scalars().all()

    print("Os 6 primeiros usuários cadastrados:")
    for usuario in usuarios_19:
        print(f"  - ID: {usuario.id}, Nome: {usuario.nome}")


print("\n--- 20. Obtenha os 5 produtos mais baratos disponíveis no estoque. ---")

with Session() as session:
    query_20 = select(Produto).filter(
        Produto.estoque > 0
    ).order_by(
        Produto.preco.asc() 
    ).limit(5)
    
    produtos_20 = session.execute(query_20).scalars().all()

    print("Os 5 produtos mais baratos com estoque:")
    for produto in produtos_20:
        print(f"  - {produto.nome} (R$ {produto.preco:.2f}) - Estoque: {produto.estoque}")


print("\n--- 21. Selecione os 3 pedidos mais recentes feitos por usuários com idade > 30. ---")

with Session() as session:
    query_21 = select(Pedido, Usuario.nome).join(
        Usuario, Pedido.usuario_id == Usuario.id
    ).filter(
        Usuario.idade > 30
    ).order_by(
        desc(Pedido.data_pedido)
    ).limit(3)

    pedidos_21 = session.execute(query_21).all()

    if pedidos_21:
        print("Os 3 pedidos mais recentes de usuários com mais de 30 anos:")
        for pedido, nome_usuario in pedidos_21:
            print(f"  - Pedido ID: {pedido.id}, Data: {pedido.data_pedido.strftime('%Y-%m-%d')} (Feito por: {nome_usuario})")
    else:
        print("Nenhum pedido encontrado para usuários com mais de 30 anos.")

print("--- 22. Liste os usuários cadastrados, ignorando os 5 primeiros resultados. ---")

with Session() as session:

    query_22 = select(Usuario).order_by(Usuario.id).offset(5)
    usuarios_22 = session.execute(query_22).scalars().all()

    print("Usuários cadastrados (pulando os 5 primeiros):")
    for usuario in usuarios_22:
        print(f"  - ID: {usuario.id}, Nome: {usuario.nome}")


print("\n--- 23. Obtenha os produtos mais caros, pulando os 3 primeiros resultados... ---")

with Session() as session:
    query_23 = select(Produto).order_by(
        desc(Produto.preco)
    ).offset(3)
    
    produtos_23 = session.execute(query_23).scalars().all()

    print("Produtos mais caros (pulando os 3 primeiros):")
    for produto in produtos_23:
        print(f"  - {produto.nome} (R$ {produto.preco:.2f})")


print("\n--- 24. Liste os pedidos... ignorando os 8 primeiros, ordenados por data decrescente. ---")

with Session() as session:
    query_24 = select(Pedido).order_by(
        desc(Pedido.data_pedido)
    ).offset(8)

    pedidos_24 = session.execute(query_24).scalars().all()

    print("Pedidos mais recentes (pulando os 8 primeiros):")
    for pedido in pedidos_24:
        print(f"  - ID: {pedido.id}, Data: {pedido.data_pedido.strftime('%Y-%m-%d')}")

print("--- 25. Conte quantos usuários estão cadastrados no sistema. ---")

with Session() as session:
    query_25 = select(func.count()).select_from(Usuario)
    total_usuarios = session.execute(query_25).scalar()
    
    print(f"Total de usuários cadastrados: {total_usuarios}")


print("\n--- 26. Determine o número de pedidos realizados com status 'entregue'. ---")

with Session() as session:
    query_26 = select(func.count()).select_from(Pedido).filter(
        Pedido.status == 'entregue'
    )
    
    total_entregues = session.execute(query_26).scalar()

    print(f"Total de pedidos 'entregues': {total_entregues}")


print("\n--- 27. Conte quantos produtos existem na categoria 'eletrônicos' com estoque > 0 e preço > R$ 100. ---")

with Session() as session:
    query_27 = select(func.count()).select_from(Produto).filter(
        Produto.categoria == 'eletrônicos',
        Produto.estoque > 0,
        Produto.preco > 100
    )
    
    total_produtos_filtro = session.execute(query_27).scalar()

    print(f"Total de produtos (eletrônicos, c/ estoque, > R$ 100): {total_produtos_filtro}")

print("--- 28. Liste todas as categorias únicas de produtos disponíveis... ---")

with Session() as session:
    query_28 = select(Produto.categoria).distinct().order_by(Produto.categoria)
    
    categorias_unicas = session.execute(query_28).scalars().all()

    print("Categorias únicas de produtos:")
    for categoria in categorias_unicas:
        print(f"  - {categoria}")


print("\n--- 29. Identifique as idades únicas dos usuários cadastrados... ---")

with Session() as session:
    query_29 = select(Usuario.idade).distinct().order_by(Usuario.idade)
    
    idades_unicas = session.execute(query_29).scalars().all()

    print("Idades únicas dos usuários:")
    print(f"  - {', '.join([str(idade) for idade in idades_unicas])}")


print("\n--- 30. Obtenha todos os status únicos dos pedidos... (usuários ativos > 25 anos) ---")

with Session() as session:
    query_30 = select(Pedido.status).distinct().join(
        Usuario, Pedido.usuario_id == Usuario.id
    ).filter(
        Usuario.ativo == True,
        Usuario.idade > 25
    ).order_by(Pedido.status)

    status_unicos = session.execute(query_30).scalars().all()

    if status_unicos:
        print("Status únicos de pedidos (usuários ativos > 25 anos):")
        for status in status_unicos:
            print(f"  - {status}")
    else:
        print("Nenhum pedido encontrado com esses critérios de usuário.")


print("--- 31. Liste o nome dos usuários e os IDs dos pedidos que eles realizaram. ---")

with Session() as session:
    query_31 = select(
        Usuario.nome, 
        Pedido.id
    ).join(
        Usuario, Pedido.usuario_id == Usuario.id
    ).order_by(Usuario.nome, Pedido.id)

    resultados_31 = session.execute(query_31).all()

    print("Usuários e seus Pedidos (ID):")
    for nome, pedido_id in resultados_31:
        print(f"  - Usuário: {nome.ljust(10)} | Pedido ID: {pedido_id}")


print("\n--- 32. ...produtos e quantidade... pedidos realizados por 'João'. ---")

with Session() as session:
    query_32 = select(
        Produto.nome, 
        Pedido.quantidade
    ).join(
        Usuario, Pedido.usuario_id == Usuario.id  
    ).join(
        Produto, Pedido.produto_id == Produto.id  
    ).filter(
        Usuario.nome == 'João'
    )
    
    resultados_32 = session.execute(query_32).all()

    if resultados_32:
        print("Pedidos de 'João':")
        for nome_produto, qtd in resultados_32:
            print(f"  - Produto: {nome_produto.ljust(17)} | Quantidade: {qtd}")
    else:
        print("Nenhum pedido encontrado para o usuário 'João'.")


print("\n--- 33. ...usuários que fizeram pedidos de 'livros'... ---")

with Session() as session:
    query_33 = select(
        Usuario.nome, 
        Produto.nome, 
        Pedido.quantidade
    ).join(
        Usuario, Pedido.usuario_id == Usuario.id
    ).join(
        Produto, Pedido.produto_id == Produto.id
    ).filter(
        Produto.categoria == 'livros'
    ).order_by(Usuario.nome)
    
    resultados_33 = session.execute(query_33).all()

    if resultados_33:
        print("Pedidos de 'livros':")
        for user_nome, prod_nome, qtd in resultados_33:
            print(f"  - Usuário: {user_nome.ljust(10)} | Produto: {prod_nome.ljust(12)} | Qtd: {qtd}")
    else:
        print("Nenhum pedido de 'livros' encontrado.")

with Session() as session:
    subquery_34 = select(Usuario.id).filter_by(nome='Maria')
    
   
    query_34 = select(exists(subquery_34))

    existe_maria = session.execute(query_34).scalar()
    
    if existe_maria:
        print("Sim, existe uma usuária chamada 'Maria'.")
    else:
        print("Não, 'Maria' não foi encontrada.")


print("\n--- 35. Confirme se há algum pedido... produto com estoque igual a 0. ---")

with Session() as session:
   
    subquery_35 = select(Pedido.id).join(
        Produto, Pedido.produto_id == Produto.id
    ).filter(
        Produto.estoque == 0
    )
    
 
    query_35 = select(exists(subquery_35))
    
    existe_pedido_estoque_zero = session.execute(query_35).scalar()

    if existe_pedido_estoque_zero:
        print("Sim, existe pelo menos um pedido de um produto com estoque 0.")
    else:
        print("Não, nenhum pedido de produto com estoque 0 foi encontrado.")


print("\n--- 36. ...pedido feito por um usuário inativo com status 'pendente'. ---")

with Session() as session:
  
    subquery_36 = select(Pedido.id).join(
        Usuario, Pedido.usuario_id == Usuario.id
    ).filter(
        Usuario.ativo == False,
        Pedido.status == 'pendente'
    )
    

    query_36 = select(exists(subquery_36))

    existe_pedido_especifico = session.execute(query_36).scalar()

    if existe_pedido_especifico:
        print("Sim, existe um pedido 'pendente' de um usuário 'inativo'.")
    else:
        print("Não, nenhum pedido 'pendente' de usuário 'inativo' foi encontrado.")

print("--- 37. (Equivalente a add_columns) Retorne o nome e a idade de todos os usuários. ---")

with Session() as session:
   
    query_37 = select(Usuario.nome, Usuario.idade).order_by(Usuario.nome)
    
    resultados_37 = session.execute(query_37).all()

    print("Nome e Idade dos Usuários:")
    for nome, idade in resultados_37:
        print(f"  - Nome: {nome.ljust(10)} | Idade: {idade}")


print("\n--- 38.Liste o nome dos produtos e seus preços. ---")

with Session() as session:
    query_38 = select(Produto.nome, Produto.preco).order_by(Produto.nome)
    
    resultados_38 = session.execute(query_38).all()

    print("Nome e Preço dos Produtos:")
    for nome, preco in resultados_38:
        print(f"  - Produto: {nome.ljust(20)} | Preço: R$ {preco:.2f}")


print("\n--- 39.Usuários, IDs dos pedidos e quantidade... ---")

with Session() as session:
    query_39 = select(
        Usuario.nome, 
        Pedido.id, 
        Pedido.quantidade
    ).join(
        Usuario, Pedido.usuario_id == Usuario.id
    ).order_by(Usuario.nome, Pedido.id)

    resultados_39 = session.execute(query_39).all()

    print("Detalhes dos Pedidos por Usuário:")
    for nome, pedido_id, qtd in resultados_39:
        print(f"  - Usuário: {nome.ljust(10)} | Pedido ID: {pedido_id} | Quantidade: {qtd}")

print("--- 40. Agrupe os pedidos pelo status e conte quantos pedidos existem... ---")

with Session() as session:
    query_40 = select(
        Pedido.status, 
        func.count(Pedido.id)
    ).group_by(Pedido.status).order_by(Pedido.status)
    
    resultados_40 = session.execute(query_40).all()

    print("Contagem de pedidos por status:")
    for status, contagem in resultados_40:
        print(f"  - Status: {status.ljust(10)} | Total: {contagem}")


print("\n--- 41. Agrupe os produtos pela categoria e calcule o preço médio... ---")

with Session() as session:
    query_41 = select(
        Produto.categoria,
        func.avg(Produto.preco)
    ).group_by(Produto.categoria).order_by(Produto.categoria)

    resultados_41 = session.execute(query_41).all()
    
    print("Preço médio por categoria:")
    for categoria, preco_medio in resultados_41:
        print(f"  - Categoria: {categoria.ljust(12)} | Preço Médio: R$ {preco_medio:.2f}")


print("\n--- 42. ...soma total das quantidades... por usuário (ativo > 30 anos). ---")

with Session() as session:
    query_42 = select(
        Usuario.nome,
        func.sum(Pedido.quantidade)
    ).join(
        Usuario, Pedido.usuario_id == Usuario.id
    ).filter(
        Usuario.ativo == True,
        Usuario.idade > 30
    ).group_by(Usuario.nome).order_by(Usuario.nome)

    resultados_42 = session.execute(query_42).all()

    if resultados_42:
        print("Total de itens comprados por usuários (ativos, >30 anos):")
        for nome, soma_quantidades in resultados_42:
            print(f"  - Usuário: {nome.ljust(10)} | Total de Itens: {int(soma_quantidades)}")
    else:
        print("Nenhum pedido encontrado para usuários ativos com mais de 30 anos.")

print("--- 43. Agrupe os pedidos pelo status e filtre... com mais de 3 registros... ---")

with Session() as session:
    query_43 = select(
        Pedido.status, 
        func.count(Pedido.id)
    ).group_by(
        Pedido.status
    ).having(
        func.count(Pedido.id) > 3
    )
    
    resultados_43 = session.execute(query_43).all()

    print("Status com mais de 3 pedidos:")
    for status, contagem in resultados_43:
        print(f"  - Status: {status.ljust(10)} | Total: {contagem}")


print("\n--- 44. Agrupe os produtos pela categoria e filtre... preço médio > R$ 200... ---")

with Session() as session:
    query_44 = select(
        Produto.categoria,
        func.avg(Produto.preco)
    ).group_by(
        Produto.categoria
    ).having(
        func.avg(Produto.preco) > 200
    ).order_by(Produto.categoria)

    resultados_44 = session.execute(query_44).all()
    
    print("Categorias com preço médio > R$ 200,00:")
    for categoria, preco_medio in resultados_44:
        print(f"  - Categoria: {categoria.ljust(12)} | Preço Médio: R$ {preco_medio:.2f}")


print("\n--- 45. Agrupe os pedidos por usuário... soma total das quantidades > 10... ---")

with Session() as session:
    query_45 = select(
        Usuario.nome,
        func.sum(Pedido.quantidade)
    ).join(
        Usuario, Pedido.usuario_id == Usuario.id
    ).group_by(
        Usuario.nome
    ).having(
        func.sum(Pedido.quantidade) > 10
    )

    resultados_45 = session.execute(query_45).all()

    if resultados_45:
        print("Usuários com mais de 10 itens comprados (total):")
        for nome, soma_quantidades in resultados_45:
            print(f"  - Usuário: {nome.ljust(10)} | Total de Itens: {int(soma_quantidades)}")
    else:
        print("Nenhum usuário comprou mais de 10 itens no total.")