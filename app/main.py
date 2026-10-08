"""Small FastAPI MVP for the Food Surplus Platform DevOps laboratory."""

from __future__ import annotations

import os
from threading import Lock
from uuid import uuid4

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field


class Student(BaseModel):
    name: str
    surname: str
    group: str
    student_id: str


class OfferCreate(BaseModel):
    title: str = Field(min_length=3, max_length=80)
    quantity: int = Field(gt=0, le=1000)
    pickup_window: str = Field(min_length=5, max_length=120)


class Offer(OfferCreate):
    id: str
    available_quantity: int


class ReservationRequest(BaseModel):
    quantity: int = Field(gt=0, le=1000)


class Reservation(BaseModel):
    reservation_id: str
    offer_id: str
    quantity: int
    remaining_quantity: int


def student_from_environment() -> Student:
    return Student(
        name=os.getenv("STUDENT_NAME", "Danil"),
        surname=os.getenv("STUDENT_SURNAME", "Kukurekin"),
        group=os.getenv("STUDENT_GROUP", "IT2-2312"),
        student_id=os.getenv("STUDENT_ID", "37554"),
    )


catalog_lock = Lock()
offers: dict[str, Offer] = {}


def reset_catalog() -> None:
    """Restore a deterministic catalog for a fresh local run or test."""
    with catalog_lock:
        offers.clear()
        demo_offer = Offer(
            id="bakery-bread-001",
            title="Fresh bakery bread",
            quantity=12,
            available_quantity=12,
            pickup_window="Today 18:00-20:00",
        )
        offers[demo_offer.id] = demo_offer


reset_catalog()
app = FastAPI(title="Food Surplus Platform", version="1.0.0")


@app.get("/")
def root() -> dict[str, object]:
    student = student_from_environment()
    return {
        "message": "Food Surplus Platform is running successfully!",
        "student": student.model_dump(),
        "features": ["food offers", "partial reservations", "quantity protection"],
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/offers", response_model=list[Offer])
def list_offers() -> list[Offer]:
    with catalog_lock:
        return list(offers.values())


@app.post("/offers", response_model=Offer, status_code=status.HTTP_201_CREATED)
def create_offer(payload: OfferCreate) -> Offer:
    offer = Offer(
        id=str(uuid4()),
        title=payload.title,
        quantity=payload.quantity,
        available_quantity=payload.quantity,
        pickup_window=payload.pickup_window,
    )
    with catalog_lock:
        offers[offer.id] = offer
    return offer


@app.post("/offers/{offer_id}/reserve", response_model=Reservation)
def reserve_offer(offer_id: str, payload: ReservationRequest) -> Reservation:
    """Reserve only available units; the lock models an atomic stock update."""
    with catalog_lock:
        offer = offers.get(offer_id)
        if offer is None:
            raise HTTPException(status_code=404, detail="Offer not found")
        if offer.available_quantity < payload.quantity:
            raise HTTPException(status_code=409, detail="Insufficient available quantity")
        offer.available_quantity -= payload.quantity
        return Reservation(
            reservation_id=str(uuid4()),
            offer_id=offer.id,
            quantity=payload.quantity,
            remaining_quantity=offer.available_quantity,
        )
