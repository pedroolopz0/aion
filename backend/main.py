from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from mutagen.mp3 import MP3
from mutagen.id3 import ID3
import os
import sqlite3
import socket

CARPETA_MUSICA = "C:/_pedroolopz"

def iniciar_db():
    conn = sqlite3.connect("aion.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS canciones (
            archivo TEXT PRIMARY KEY,
            titulo TEXT,
            artista TEXT,
            album TEXT,
            año TEXT,
            duracion REAL
        );
    """)
    conn.commit()
    conn.close()

def sincronizar_db():
    conn = sqlite3.connect("aion.db")
    cursor = conn.cursor()

    canciones = os.listdir(CARPETA_MUSICA)
    for cancion in canciones:
        if cancion.endswith(".mp3"):
            cursor.execute("SELECT archivo FROM canciones WHERE archivo = ?", (cancion,))
            resultado = cursor.fetchone()
            if resultado is None:
                ruta = CARPETA_MUSICA + "/" + cancion
                try:
                    tags = ID3(ruta)
                    cursor.execute(
                        "INSERT INTO canciones VALUES (?, ?, ?, ?, ?, ?)",
                        (
                        cancion,
                        tags.get("TIT2").text[0] if tags.get("TIT2") else "Desconocido",
                        tags.get("TPE1").text[0] if tags.get("TPE1") else "Desconocido",
                        tags.get("TALB").text[0] if tags.get("TALB") else "Desconocido",
                        str(tags.get("TDRC").text[0]) if tags.get("TDRC") else "Desconocido",
                        MP3(ruta).info.length
                        )
                    )
                except Exception as e:
                    print(f"Error con {cancion}: {e}")
    conn.commit()
    conn.close()

app = FastAPI()
iniciar_db()
sincronizar_db()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ip")
def ip():
    return{"ip": socket.gethostbyname(socket.gethostname())}

@app.get("/actualizar")
def actualizar():
    conn = sqlite3.connect("aion.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM canciones")
    antes = cursor.fetchone()[0]
    conn.close()

    sincronizar_db()

    conn = sqlite3.connect("aion.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM canciones")
    despues = cursor.fetchone()[0]
    conn.close()

    return {"nuevas": despues - antes}


@app.get("/descargar/{archivo}")
async def descargar_archivo(archivo: str):
    file_path = os.path.join(CARPETA_MUSICA, archivo)

    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail='archivo no encontrado')
    
    if not archivo.endswith(".mp3"):
        raise HTTPException(status_code=400, detail='archivo a descargar no valido')
    
    return FileResponse(
        path=file_path,
        filename=archivo,
        media_type='application/octet-stream'
    )

@app.get("/musica")
def musica():
    conn = sqlite3.connect("aion.db")      
    cursor = conn.cursor()                 
    cursor.execute("SELECT archivo, titulo, artista, album, año, duracion FROM canciones")  
    filas = cursor.fetchall()              
    conn.close()                          
    
    cancionesfiltradas = []
    for fila in filas:                   
        cancionesfiltradas.append({        
            "archivo": fila[0],          
            "titulo":  fila[1],        
            "artista": fila[2],
            "album":   fila[3],
            "año":     fila[4],
            "duracion": fila[5]
        })
    
    return {"lista": cancionesfiltradas}

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")