"""
Módulo de base de datos para Yamaki usando SQLAlchemy.
Requiere la variable de entorno DATABASE_URL (p. ej., postgresql+psycopg2://user:pass@host/dbname)
"""

from __future__ import annotations

import os
import uuid
from datetime import datetime
from typing import Optional, Dict, Any

from sqlalchemy import (
    create_engine,
    String,
    DateTime,
    Boolean,
    JSON,
    ForeignKey,
)
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship, Session


DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL) if DATABASE_URL else None
Base = declarative_base()


class YamakiRequest(Base):
    __tablename__ = "yamaki_requests"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user_phone: Mapped[str] = mapped_column(String(64))
    category: Mapped[str] = mapped_column(String(64))
    subcategory: Mapped[Optional[str]] = mapped_column(String(128))
    brand: Mapped[Optional[str]] = mapped_column(String(64))
    model: Mapped[Optional[str]] = mapped_column(String(128))
    city: Mapped[Optional[str]] = mapped_column(String(128))
    details: Mapped[Optional[str]] = mapped_column(String(2048))
    source_channel: Mapped[str] = mapped_column(String(32), default="whatsapp")
    status: Mapped[str] = mapped_column(String(32), default="abierto")

    pqr: Mapped["YamakiPqr"] = relationship("YamakiPqr", back_populates="request", uselist=False)


class YamakiPqr(Base):
    __tablename__ = "yamaki_pqrs"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    request_id: Mapped[str] = mapped_column(String(40), ForeignKey("yamaki_requests.id"))
    pqr_type: Mapped[str] = mapped_column(String(32))  # Petición/Queja/Reclamo/Solicitud
    subject: Mapped[str] = mapped_column(String(256))
    description: Mapped[str] = mapped_column(String(2048))
    category: Mapped[str] = mapped_column(String(64))
    classification: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON)
    response_text: Mapped[Optional[str]] = mapped_column(String(4096))
    requires_human: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[str] = mapped_column(String(32), default="abierto")

    request: Mapped[YamakiRequest] = relationship("YamakiRequest", back_populates="pqr")


def init_db() -> None:
    """Crea tablas si no existen."""
    if not engine:
        print("[yamaki_db] WARNING: DATABASE_URL no configurado. No se crearán tablas.")
        return
    Base.metadata.create_all(engine)


def save_interaction(
    user_phone: str,
    category: str,
    subject: str,
    description: str,
    subcategory: Optional[str],
    brand: Optional[str],
    model: Optional[str],
    city: Optional[str],
    classification_data: Optional[dict],
    response_text: Optional[str],
    pqr_id: str,
    pqr_type: str,
    requires_human: bool,
) -> None:
    """Guarda la solicitud y su PQR asociado."""
    if not engine:
        print("[yamaki_db] WARNING: DATABASE_URL no configurado. No se guardarán datos.")
        return

    req_id = str(uuid.uuid4())[:12]

    with Session(engine) as session:
        req = YamakiRequest(
            id=req_id,
            user_phone=user_phone,
            category=category or "General",
            subcategory=subcategory,
            brand=brand,
            model=model,
            city=city,
            details=description,
            status="escalado" if requires_human else "abierto",
        )

        pqr = YamakiPqr(
            id=pqr_id,
            request_id=req_id,
            pqr_type=pqr_type or "Solicitud",
            subject=subject or "Consulta",
            description=description,
            category=category or "General",
            classification=classification_data,
            response_text=response_text,
            requires_human=requires_human,
            status="escalado" if requires_human else "abierto",
        )

        session.add(req)
        session.add(pqr)
        session.commit()


