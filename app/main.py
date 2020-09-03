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


    getuser_query = f"""
        SELECT
            *
        FROM userlvl
        where userlvl.username = "{userlvl.username}"
    """

    output = connection.execute(getuser_query).fetchall()

    if output:
        update_user = f"""
        UPDATE 
            userlvl
        SET
            level = {userlvl.level}
        WHERE username = "{userlvl.username}"
        """
        cursor.execute(update_user)

        connection.commit()

        connection.close()

        return "User already existed, updated DB"
    
    else:
        insertion_query = f"""
        INSERT INTO userlvl (username, level)
        VALUES
        {tuple((userlvl.username, userlvl.level))}
        """
        cursor.execute(insertion_query)

        connection.commit()

        connection.close()

        return "Added to the db"


@app.get('/user/{username}')
async def getuserlvl(username: str):

    connection = sqlite3.connect("lvl.sqlite3")

    cursor = connection.cursor()

    getuser_query = f"""
        SELECT
            *
        FROM userlvl
        where userlvl.username = "{username}"
    """

    output = cursor.execute(getuser_query).fetchall()

    connection.commit()
    
    connection.close()
    if not output:
        return "User was not found in the DB!"

    else:
        return {output[0][0]: output[0][1]}


