from fastapi import FastAPI

import os
app = FastAPI()

@app.get("/")
def root():
    return {"mensaje": "Aion funcionando"}

@app.get("/ping")
def ping():
    return {"status": "ok"}

@app.get("/musica")
def musica():
    canciones = os.listdir("C:/_pedroolopz")
    return {"lista": canciones}
            