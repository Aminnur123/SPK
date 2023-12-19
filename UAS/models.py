from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class cafe(Base):
    __tablename__ = 'tb_cafe'
    id_cafe: Mapped[str] = mapped_column(primary_key=True)
    rating_minuman: Mapped[int] = mapped_column()
    harga: Mapped[int] = mapped_column()
    kualitas_pelayanan: Mapped[int] = mapped_column()
    suasana: Mapped[int] = mapped_column()
    rasa: Mapped[int] = mapped_column()  
    
    def __repr__(self) -> str:
        return f"cafe(id_cafe={self.id_cafe!r}, harga={self.harga!r})"
