from sqlalchemy import (
    Column, Integer, String, ForeignKey, Float,
    DateTime, Boolean, func, UniqueConstraint
)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

# Base declarativa para os modelos
Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    idade = Column(Integer)
    ativo = Column(Boolean, default=True)

    # Relações (links para outras tabelas)
    pedidos = relationship('Pedido', back_populates='usuario')
    
    # Adicionado para a classe 'Avaliacao'
    avaliacoes = relationship('Avaliacao', back_populates='usuario') 

    def __str__(self):
        return (f"Usuario(id={self.id}, nome='{self.nome}', "
                f"email='{self.email}', idade={self.idade}, ativo={self.ativo})")

class Produto(Base):
    __tablename__ = 'produtos'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    preco = Column(Float, nullable=False)
    categoria = Column(String(50))
    estoque = Column(Integer, default=0)
    criado_em = Column(DateTime, default=datetime.now)

    # Adicionado para a classe 'Pedido' (baseado na sua nova definição)
    pedidos = relationship('Pedido', back_populates='produto')

    def __str__(self):
        return (f"Produto(id={self.id}, nome='{self.nome}', "
                f"preco={self.preco}, categoria='{self.categoria}', "
                f"estoque={self.estoque}, criado_em={self.criado_em})")

class Pedido(Base):
    __tablename__ = 'pedidos'
    id = Column(Integer, primary_key=True)
    
    # Chaves Estrangeiras
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    produto_id = Column(Integer, ForeignKey('produtos.id'), nullable=False)
    
    # Colunas de dados
    quantidade = Column(Integer, nullable=False)
    status = Column(String(20), default='pendente')
    data_pedido = Column(DateTime, default=datetime.now)

    # Relações
    usuario = relationship('Usuario', back_populates='pedidos')
    produto = relationship('Produto', back_populates='pedidos')

    # Regra: Um usuário só pode ter uma entrada de pedido por produto
    __table_args__ = (
        UniqueConstraint('usuario_id', 'produto_id', name='uq_usuario_produto'),
    )

    def __str__(self):
        return (f"Pedido(id={self.id}, usuario_id={self.usuario_id}, "
                f"produto_id={self.produto_id}, quantidade={self.quantidade}, "
                f"status='{self.status}', data_pedido={self.data_pedido})")

class Avaliacao(Base):
    __tablename__ = 'avaliacoes'
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    nota = Column(Integer, nullable=False)
    comentario = Column(String(300))

    # Relação (link para 'Usuario')
    usuario = relationship('Usuario', back_populates='avaliacoes')

    def __str__(self):
        return (f"Avaliacao(id={self.id}, usuario_id={self.usuario_id}, "
                f"nota={self.nota}, comentario='{self.comentario}')")