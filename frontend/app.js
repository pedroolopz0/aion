fetch("http://127.0.0.1:8000/musica")
  .then(response => response.json())
  .then(data => {
    const contenedor = document.getElementById("canciones");
    data.lista.forEach((elemento) => {
      contenedor.innerHTML += `<div class="cancion"><p class="titulo">${elemento.titulo}</p><p class="artista">${elemento.artista}</p></div>`
    });
  });