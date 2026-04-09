from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from mutagen.mp3 import MP3
from mutagen.id3 import ID3
import os

CARPETA_MUSICA = "C:/_pedroolopz"

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/musica")
def musica():
    canciones = os.listdir(CARPETA_MUSICA)
    cancionesfiltradas = []
    for cancion in canciones:
        if cancion.endswith(".mp3"):
            ruta = CARPETA_MUSICA + "/" + cancion
            tags = ID3(ruta)
            cancionesfiltradas.append({
                "artista": tags.get("TPE1").text[0] if tags.get("TPE1") else "Desconocido",
                "titulo": tags.get("TIT2").text[0] if tags.get("TIT2") else "Desconocido",
                "album": tags.get("TALB").text[0] if tags.get("TALB") else "Desconocido",
                "año": tags.get("TDRC").text[0] if tags.get("TDRC") else "Desconocido",
                "duracion": MP3(ruta).info.length
            })
    return {"lista": cancionesfiltradas}