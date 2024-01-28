import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI,status,Depends,APIRouter
import time
from ..database import section_local,get_db
from .. import models, schemas,oauth2


router = APIRouter(
    prefix="/post",
    tags=['UsingSql']
)


while True:
    try:
        conn = psycopg2.connect(host = 'localhost',database='fastapi',user='postgres',password= 'password', cursor_factory = RealDictCursor)
        conne = conn.cursor()
        print('data base connection was established')
        break
    except Exception as e:
        print(e)
        time.speep(2)

@router.get("/")
def get_postd(current_user:int = Depends(oauth2.get_current_user)):
    print(current_user.email)
    conne.execute("""select * from "Post" """)
    sheck_post = conne.fetchall()
    print(sheck_post)
    return sheck_post



@router.post("/")
def create_postd(post:schemas.Post,current_user:int = Depends(oauth2.get_current_user)):
    conne.execute("""insert into "Post" (title,content,published) values(%s,%s,%s) returning * """,(post.title,post.content,post.published))
    sheck_post = conne.fetchone()
    conn.commit()
    return {"new_post":sheck_post}


@router.get('/{id}')
def get_post_id(id:int,current_user:int = Depends(oauth2.get_current_user)):
    conne.execute(""" select * from "Post" where id =%s """, str((id)))
    see_data = conne.fetchone()
    return see_data

@router.put('/{id}')
def update_past(id:int,post:schemas.Post,current_user:int = Depends(oauth2.get_current_user)):
    conne.execute(""" update "Post" set title = %s, content = %s, published = %s where id = %s returning * """, (post.title,post.content,post.published,str(id)))
    check_updated_post = conne.fetchone()
    conn.commit()
    return {'updated:data':check_updated_post}
