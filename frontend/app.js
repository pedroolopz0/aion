const contenedor = document.getElementById("canciones");
const btn = document.getElementById("btnDark");
const numeroPagina = document.getElementById("numeroPagina")
const loading = document.getElementById("loading");
const porPag = 28;
let paginaAct = 0;
let listaCompleta = [];
let listaActual = [];
let faltantes = [];

// boton modo de visualizacion
btn.onclick = function () 
{
  document.body.classList.toggle("dark");

  btn.textContent = document.body.classList.contains("dark")
    ? "Modo Claro"
    : "Modo Oscuro";
};

// fetch canciones
fetch(`http://${window.location.hostname}:8000/musica`) 
  .then(response => response.json())
  .then(data => 
  {
    loading.style.display = "none"
    listaCompleta = data.lista;
    listaActual = listaCompleta;
    mostrarCanciones(listaActual);
    const unicos = [...new Set(listaCompleta.map(c => c.artista))]
    unicos.forEach(artista => {
    const option = document.createElement("option")
    option.value = artista
    option.textContent = artista
    document.getElementById("filtroArtista").appendChild(option)
    })
  })
  
.catch(error => console.error("Error:", error));

document.getElementById("btnSiguiente").onclick = function() {
    if ((paginaAct + 1) * porPag < listaActual.length) {
        paginaAct++;
        mostrarCanciones(listaActual);
        numeroPagina.textContent = paginaAct + 1;
    }
}

document.getElementById("btnAnterior").onclick = function() {
    if (paginaAct > 0) {
        paginaAct--;
        mostrarCanciones(listaActual);
        numeroPagina.textContent = paginaAct + 1;
    }
}

function mostrarCanciones(lista){
  let html = "";
  lista.slice(paginaAct*porPag, (paginaAct + 1) * porPag).forEach((elemento) => {
    html += `
      <div class="cancion">
        <p class="titulo">${elemento.titulo || ""}</p>
        <p class="artista">${elemento.artista || ""}</p>
      </div>
    `;
  });

  contenedor.innerHTML = html;
}

const select = document.getElementById("filtroArtista")

function filtrar(event) {
  const artistafiltrado = event.target.value;
  if (artistafiltrado === ""){
    listaActual = listaCompleta;
  }
  else{
    listaActual = listaCompleta.filter(c => c.artista === artistafiltrado); 
  }
paginaAct = 0;
numeroPagina.textContent = 1;
mostrarCanciones(listaActual);
}

select.addEventListener("change", filtrar)

document.getElementById("inputMusica").onchange = function(event) {
    const archivos = []
    for (const archivo of event.target.files) {
        archivos.push(archivo.name)
    }
    console.log(archivos)
    faltantes = listaCompleta.filter(c => !archivos.includes(c.archivo))
    console.log(faltantes)
}

document.getElementById("btnSincronizar").onclick = async function() {
    for (const cancion of faltantes) {
        const respuesta = await fetch(`http://${window.location.hostname}:8000/descargar/${cancion.archivo}`);
        const blob = await respuesta.blob();
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = cancion.archivo;
        link.click();
        await new Promise(resolve => setTimeout(resolve, 50));
        document.getElementById("progreso").textContent = `Descargando ${faltantes.indexOf(cancion) + 1} de ${faltantes.length}`;
        URL.revokeObjectURL(link.href);
    }
}

