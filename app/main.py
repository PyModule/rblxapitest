from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

class verify(BaseModel):
    username: str
    cordname: str
    rblxid: int

app = FastAPI()


create_table= """
CREATE TABLE IF NOT EXISTS verify (
  username text,
  cordname text,
  verified text,
  rblxid int
);
"""

def get_user(username):
    connection = sqlite3.connect("verification.sqlite3")

    cursor = connection.cursor()

    cursor.execute(create_table)

    getuser_query = f"""
        SELECT
            *
        FROM verify
        where verify.username = "{username}"
    """

    output = cursor.execute(getuser_query).fetchall()

    connection.close()

    return output


@app.get('/')
def root():
    return {"Message": 'Hello World!'}


@app.post('/verify')
async def userlvl(verify: verify):

    output = get_user(verify.username)

    if output:
        return "user already exists!"

    else:
        connection = sqlite3.connect("verification.sqlite3")

        cursor = connection.cursor()

        insertion_query = f"""
        INSERT INTO verify (username, cordname, verified, rblxid)
        VALUES
        {tuple((verify.username, verify.cordname, "No", verify.rblxid))}
        """
        cursor.execute(insertion_query)

        connection.commit()

        connection.close()

        return "Ready for verification"

@app.get('/rblxverify/{username}')
async def getcordname(username: str):

    output = get_user(username)

    if not output:
        return "User was not found in the DB!"

    else:
        return output[0][1]

@app.get('/rblxverify/{username}/verified')
async def verifyuser(username: str):
    connection = sqlite3.connect("verification.sqlite3")

    cursor = connection.cursor()

    update_user = f"""
        UPDATE 
            verify
        SET
            verified = "Yes"
        WHERE username = "{username}"
        """
    cursor.execute(update_user)

    connection.commit()

    connection.close()

    return 'User is now verified'


@app.get('/isverified/{username}')
async def isverified(username: str):
    output = get_user(username)

    if not output:
        return "User was not found in the DB!"

    else:
        return output[0][2]


@app.get('/allusers')
async def allusers():
    connection = sqlite3.connect("verification.sqlite3")

    cursor = connection.cursor()

    getuser_query = f"""
        SELECT
            *
        FROM verify
    """

    output = cursor.execute(getuser_query).fetchall()

    connection.commit()
    
    connection.close()

    if not output:
        return "There is nothing in the DB to display"
    
    else:
        user_dict = {}
        for i in output:
            user_dict[i[0]] = (i[1], i[2])

        return user_dict

@app.get('/rblxid/{cordname}')
async def getrblxid(cordname: str):
    connection = sqlite3.connect("verification.sqlite3")

    cursor = connection.cursor()

    cursor.execute(create_table)

    cordname = cordname.replace('-','#')

    getuser_query = f"""
        SELECT
            *
        FROM verify
        where verify.cordname = "{cordname}"
    """

    output = cursor.execute(getuser_query).fetchall()

    connection.close()

    print(output)

    return output[0][3]

@app.get('/cleartable')
async def cleartable():
    connection = sqlite3.connect("verification.sqlite3")

    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS verify")

    connection.commit()

    connection.close()

    return "DB has been cleared"