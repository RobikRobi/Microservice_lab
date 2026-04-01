from sqlalchemy.orm import Mapped, mapped_column
from  DateBase.db import Base



# модель таблицы для сохранения данных о счетах
class Account(Base):
    __tablename__ = 'accounts'

    id: Mapped[int] = mapped_column (primary_key=True)
    balance: Mapped[float] = mapped_column(default=0.0)
