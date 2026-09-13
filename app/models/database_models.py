from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all database models."""

    pass


class Employee(Base):
    __tablename__ = "employees"

    user_id: Mapped[str] = mapped_column(String(20), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    department: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="active")
    device_id: Mapped[str | None] = mapped_column(
        String(30),
        ForeignKey("devices.device_id"),
        nullable=True,
    )

    account: Mapped["Account | None"] = relationship(
        back_populates="employee",
        uselist=False,
    )

    device: Mapped["Device | None"] = relationship(
        back_populates="employee",
        foreign_keys=[device_id],
        uselist=False,
    )

    tickets: Mapped[list["Ticket"]] = relationship(
        back_populates="employee",
    )


class Account(Base):
    __tablename__ = "accounts"

    user_id: Mapped[str] = mapped_column(
        String(20),
        ForeignKey("employees.user_id"),
        primary_key=True,
    )
    status: Mapped[str] = mapped_column(String(30), default="active")
    locked: Mapped[bool] = mapped_column(Boolean, default=False)
    mfa_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    failed_attempts: Mapped[int] = mapped_column(Integer, default=0)
    password_last_changed: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    employee: Mapped["Employee"] = relationship(
        back_populates="account",
    )


class Device(Base):
    __tablename__ = "devices"

    device_id: Mapped[str] = mapped_column(String(30), primary_key=True)
    hostname: Mapped[str] = mapped_column(String(100), nullable=False)
    os: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="healthy")
    vpn_status: Mapped[str] = mapped_column(String(30), default="connected")
    last_seen: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    employee: Mapped["Employee | None"] = relationship(
        back_populates="device",
        foreign_keys="Employee.device_id",
        uselist=False,
    )


class Ticket(Base):
    __tablename__ = "tickets"

    ticket_id: Mapped[str] = mapped_column(String(30), primary_key=True)
    user_id: Mapped[str] = mapped_column(
        String(20),
        ForeignKey("employees.user_id"),
        nullable=False,
    )
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    priority: Mapped[str] = mapped_column(String(20), default="medium")
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="open")
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    employee: Mapped["Employee"] = relationship(
        back_populates="tickets",
    )