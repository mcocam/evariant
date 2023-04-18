from fastapi import APIRouter, Response, Depends, HTTPException
from models.validators.new_user import New_user
from controllers.SnpController import SnpController
from models.Snp import Snp

router: APIRouter = APIRouter(
    prefix="/snp",
    tags=["SNPFinder"],
    responses={404: {"description": "Not found"}}
)