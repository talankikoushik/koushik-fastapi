from typing import Tuple
from fastapi import FastAPI,Depends
from pydantic import BaseModel
app = FastAPI()
class supplier(BaseModel):
   supplierID:int
   supplierName:str
class product(BaseModel):
   productID:int
   prodname:str
   price:int
   supp:supplier
class customer(BaseModel):
   custID:int
   custname:str
   prod:Tuple[product]


@app.post('/invoice')
async def getInvoice(c1:customer):
   return c1


async def dependency(id: str, name: str, age: int):
   return {"id": id, "name": name, "age": age}


@app.get("/user/")
async def user(dep: dict = Depends(dependency)):
   return dep