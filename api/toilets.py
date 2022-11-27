from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import get_db
from models.toilet import Toilet
from utils.MapParser import getAddressByCoords

# toilets_router = APIRouter(prefix='/toilets', tags=['toilets'])
toilets_router = APIRouter()


@toilets_router.post("/addToilet")
def addToilet(lat: float,
              lon: float,
              title: str,
              desc: str,
              db: Session = Depends(get_db)):
    toilet_model = Toilet()
    toilet_model.lat = lat
    toilet_model.lon = lon
    toilet_model.title = title
    toilet_model.desc = desc
    toilet_model.address = getAddressByCoords(lat, lon)

    db.add(toilet_model)
    db.commit()
    return getToiletById(toilet_model.id, db)


@toilets_router.get("/getAllToilets")
def getAllToilets(db: Session = Depends(get_db)):
    toilets_list = db.query(Toilet).all()
    # LOGGER.info("GET all toilets")
    return toilets_list


@toilets_router.get("/getToiletById")
def getToiletById(toilet_id: int, db: Session = Depends(get_db)):
    toilet_model = db.query(Toilet).filter(Toilet.id == toilet_id).first()

    if toilet_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"Toilet with ID {toilet_id} is not exist"
        )

    return toilet_model


@toilets_router.get("/getToiletByAddress")
def getToiletByAddress(address: int, db: Session = Depends(get_db)):
    toilet_model = db.query(Toilet).filter(Toilet.address == address).first()

    if toilet_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"Toilet with Address {address} is not exist"
        )

    return toilet_model


@toilets_router.get("/getToiletByCoords")
def getToiletByCoords(lat: float, lon: float, db: Session = Depends(get_db)):
    toilet_model = db.query(Toilet).filter(
        Toilet.lat == lat and Toilet.lon == lon
    ).first()

    if toilet_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"Toilet with Coords {lat}, {lon} is not exist"
        )

    return toilet_model


@toilets_router.put("/updateToilet")
def updateToilet(toilet_id: int,
                 lat: float,
                 lon: float,
                 title: str,
                 desc: str,
                 db: Session = Depends(get_db)):
    toilet_model = db.query(Toilet).filter(Toilet.id == toilet_id).first()

    if toilet_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"Toilet with ID {toilet_id} is not exist"
        )

    toilet_model.lat = lat
    toilet_model.lon = lon
    toilet_model.title = title
    toilet_model.desc = desc
    toilet_model.address = getAddressByCoords(lat, lon)

    db.add(toilet_model)
    db.commit()
    return getToiletById(toilet_model.id, db)


@toilets_router.delete("/removeToiletById")
def removeToiletById(toilet_id: int, db: Session = Depends(get_db)):
    toilet_model = db.query(Toilet).filter(Toilet.id == toilet_id).first()

    if toilet_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"Toilet with ID {toilet_id} is not exist"
        )

    db.query(Toilet).filter(Toilet.id == toilet_id).delete()
    db.commit()
