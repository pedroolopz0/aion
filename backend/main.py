from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from mutagen.mp3 import MP3
from mutagen.id3 import ID3
import os
import sqlite3

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

@app.get("/musica")
def musica():
    conn = sqlite3.connect("aion.db")      # abrís la conexión a la base de datos
    cursor = conn.cursor()                  # creás un cursor, que es el que ejecuta queries
    cursor.execute("SELECT archivo, titulo, artista, album, año, duracion FROM canciones")  # ejecutás la query
    filas = cursor.fetchall()              # traés todos los resultados como lista de tuplas
    conn.close()                           # cerrás la conexión
    
    cancionesfiltradas = []
    for fila in filas:                     # recorrés cada fila
        cancionesfiltradas.append({        # convertís cada tupla a diccionario
            "archivo": fila[0],            # fila[0] es el primer campo: archivo
            "titulo":  fila[1],            # fila[1] es el segundo: titulo
            "artista": fila[2],
            "album":   fila[3],
            "año":     fila[4],
            "duracion": fila[5]
        })
    
    return {"lista": cancionesfiltradas}