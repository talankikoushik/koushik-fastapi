from fastapi import FastAPI
from fastapi.responses import HTMLResponse
app = FastAPI()
from fastapi.templating import Jinja2Templates

@app.get("/")
async def index():
   return {"message": "Hello World"}


from fastapi import FastAPI, Depends, Request,Body

app = FastAPI()

# Using the Request dependency to access request information
@app.get("/items/")
async def read_items(request: Request):
    client_host = request.client.host
    return {"client_host": client_host}


from typing import List
from pydantic import BaseModel, Field
app = FastAPI()
class Student(BaseModel):
   id: int
   name :str = Field(None, title="name of student", max_length=10)
   subjects: List
@app.post("/students/")
async def student_data(s1: Student):
   return s1

@app.post("/studentbody/")
async def student_data(name:str = Body(),age:int = Body(),subject:List = Body()):
   return {"Name":name,"Age":age, "subjects":subject}


@app.post("/students/{college}")
async def student_data1(college:str, age:int, student_sub:Student):
   retval={"college":college, "age":age, **student_sub.dict(), 'id':student_sub.id}
   return retval
@app.get('/')
async def html_resp():
   rat = '''<html><body><h1>hello world</h1></body></html>'''
   return HTMLResponse(content=rat)



templates = Jinja2Templates(directory='templates')
@app.get('/hello/{name}',response_class=HTMLResponse)
def hello(request:Request,name:str):
   return templates.TemplateResponse("hello.html",{'request':request,'name':name})

@app.get('/login')
def login(request:Request):
   return templates.TemplateResponse('login.html',{'request':request})

from fastapi import Form
@app.post('/submits')
def submit(nm:str =Form(),pwd:str=Form( )):
   return {'username':nm}



class User(BaseModel):
   username:str
   password:str
@app.post("/submits/", response_model=User)
async def submits(nm: str = Form(...), pwd: str = Form(...)):
   return User(username=nm, password=pwd)

@app.get("/upload", response_class=HTMLResponse)
def upload(request:Request):
   return templates.TemplateResponse('file.html',{'request':request})

from fastapi import File, UploadFile
import shutil
@app.post("/uploder")
def submit_file(file: UploadFile = File()):
   with open("destination.png", "wb") as buffer:
      shutil.copyfileobj(file.file, buffer)
   return file.filename

from typing import Optional
from fastapi import Header
@app.get("/headers/")
def read_header(accept_language: Optional[str] = Header(None)):
   return{"Readlanguage": accept_language}




class stusent_response_model(BaseModel):
   id:int
   name:str = Field(None, title="Name od student", max_length= 10)
   marks:List[int]
   persent:float
class persent(BaseModel):
   id:int
   name:str = Field(None, title="Name od student", max_length= 10)
   persent:float

@app.post('/marks',response_model= persent)
def get_persent(s1:stusent_response_model):
   s1.persent = sum(s1.marks)/len(s1.marks)
   return s1

if __name__ == "__main__":
   read_items()
