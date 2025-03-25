from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    # Através do SQLAlchemy foi definido o modelo User, uma classe representando a tabela Users no Banco de Dados
    #
    # Atributos:
    #   id: identificador do usuário no Banco de Dados (Primary Key)
    #   username: nome do usuário
    #   password: senha do usuário
    #   email: email do usuário
    #   created_at: data da criação do usuário no Banco de Dados
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column()
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )