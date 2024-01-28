from fastapi import FastAPI
from pydantic import BaseModel
import datetime
data = []
class book(BaseModel):
    id:int
    name:str
    author: str
    publisher: str


app =FastAPI()

@app.post('/book_update')
def update_book(b1:book):
    data.append(b1.dict())
    return data

@app.get('/book/{id}')
def get_book(id:int):
    id = id -1
    return data[id]


@app.put("/book/{id}")
def add_book(id: int, books: book):
   data[id-1] = books
   return data

@app.delete("/book/{id}")
def delete_book(id: int):
   data.pop(id-1)
   return data



@app.on_event("startup")
async def startup_event():
   print('Server started :', datetime.datetime.now())
@app.on_event("shutdown")
async def shutdown_event():
   print('server Shutdown :', datetime.datetime.now())


subapp = FastAPI()
@subapp.get("/sub")
def subindex():
   return {"message": "Hello World from sub app"}

from fastapi import FastAPI
app = FastAPI()
@app.get("/app")
def mainindex():
   return {"message": "Hello World from Top level app"}

app.mount("/subapp", subapp)