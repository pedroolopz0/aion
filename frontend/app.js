const contenedor = document.getElementById("canciones");
const btn = document.getElementById("btnDark");

// 🌙 BOTÓN MODO OSCURO
btn.onclick = function () {
  document.body.classList.toggle("dark");

  btn.textContent = document.body.classList.contains("dark")
    ? "Modo Claro"
    : "Modo Oscuro";
};

// 🎵 FETCH DE CANCIONES
fetch("http://127.0.0.1:8000/musica")
  .then(response => response.json())
  .then(data => {
    contenedor.innerHTML = ""; // limpiar

    let html = "";

    data.lista.forEach((elemento) => {
      html += `
        <div class="cancion">
          <p class="titulo">${elemento.titulo || ""}</p>
          <p class="artista">${elemento.artista || ""}</p>
        </div>
      `;
    });

    contenedor.innerHTML = html;
  })
  .catch(error => console.error("Error:", error));