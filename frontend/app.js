const contenedor = document.getElementById("canciones");
const btn = document.getElementById("btnDark");
const numeroPagina = document.getElementById("numeroPagina")
const loading = document.getElementById("loading");
const porPag = 28;
let paginaAct = 0;
let listaCompleta = [];
let listaActual = [];

// boton modo de visualizacion
btn.onclick = function () 
{
  document.body.classList.toggle("dark");

  btn.textContent = document.body.classList.contains("dark")
    ? "Modo Claro"
    : "Modo Oscuro";
};

// fetch canciones
fetch("http://127.0.0.1:8000/musica")
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