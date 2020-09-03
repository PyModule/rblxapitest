from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

class userlvl(BaseModel):
    username: str
    level: int

app = FastAPI()


create_table= """
CREATE TABLE IF NOT EXISTS userlvl (
  username text,
  level integer
);
"""


@app.get('/')
def root():
    return {"Message": 'Hello World!'}


@app.post('/userlvl')
async def userlvl(userlvl: userlvl):

    connection = sqlite3.connect("lvl.sqlite3")

    cursor = connection.cursor()

    cursor.execute(create_table)


    insertion_query = f"""
    INSERT INTO userlvl (username, level)
    VALUES
    {tuple((userlvl.username, userlvl.level))}
    """
    cursor.execute(insertion_query)

    connection.commit()
    
    connection.close()

    return "Added to the db?"




