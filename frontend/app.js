const contenedor = document.getElementById("canciones");
const btn = document.getElementById("btnDark");
const porPag = 28;
let paginaAct = 0;
let listaCompleta = [];

// boton modo de visualizacion
btn.onclick = function () {
  document.body.classList.toggle("dark");

  btn.textContent = document.body.classList.contains("dark")
    ? "Modo Claro"
    : "Modo Oscuro";
};

// fetch canciones
fetch("http://127.0.0.1:8000/musica")
  .then(response => response.json())
  .then(data => {
    listaCompleta = data.lista;
    mostrarCanciones(listaCompleta);
    const unicos = [...new Set(listaCompleta.map(c => c.artista))]
    unicos.forEach(artista => {
      document.getElementById("filtroArtista").innerHTML += `<option value="${artista}">${artista}</option>`
    })
  })
  .catch(error => console.error("Error:", error));

document.getElementById("btnSiguiente").onclick = function() {
    paginaAct++;
    mostrarCanciones(listaCompleta);
    document.getElementById("numeroPagina").textContent = paginaAct + 1;
}

document.getElementById("btnAnterior").onclick = function() {
    if (paginaAct > 0) {
        paginaAct--;
        mostrarCanciones(listaCompleta);
        document.getElementById("numeroPagina").textContent = paginaAct + 1;
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
