from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"mensaje": "Aion funcionando"}

@app.get("/ping")
def ping():
    return {"status": "ok"}