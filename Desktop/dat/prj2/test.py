from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def wri_n():
    return {"message": "hello"}  

@app.get("/data")
def wri_n():
    return {"hello": 1234}