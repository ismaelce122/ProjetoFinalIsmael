let canaisCache = [];

async function carregarCategoria() {
    const server = document.getElementById("server").value;
    const user = document.getElementById("user").value;
    const pass = document.getElementById("pass").value;

    const url = `${server}/player_api.php?username=${user}&password=${pass}&action=get_live_categories`;

    try {
        const response = await fetch(url);
        const data = await response.json();
        categoriasCache = data;

        mostrarCategoria();
    } catch (err) {
        alert(err)
        document.getElementById("lista").innerHTML = "Erro ao carregar categoria de Canais.";
        console.error(err);
    }

}
async function carregarCanais(categoria) {
    const server = document.getElementById("server").value;
    const user = document.getElementById("user").value;
    const pass = document.getElementById("pass").value;
    const url = `${server}/player_api.php?username=${user}&password=${pass}&action=get_live_streams&category_id=${categoria}`;

    try {
        const response = await fetch(url);
        const data = await response.json();
        canaisCache = data;

        mostrarCanais();
    } catch (err) {
        alert(err)
        document.getElementById("lista").innerHTML = "Erro ao carregar lista de Canais.";
        console.error(err);
    }

}

function mostrarCategoria() {
    const lista = document.getElementById("lista")
    let html = "<h3 class='canal'>Canais Ao Vivo:</h3>";
    categoriasCache.forEach((c, i) => {
        html += `<button onclick="carregarCanais('${c.category_id}')">${c.category_name}</button>`;
    });
    lista.style.border = '3px solid white'
    lista.innerHTML = html;
}

function mostrarCanais() {
    const lista = document.getElementById("lista")
    lista.innerHTML = ''
    const server = 'https://neweraserver10.top:80/live'
    const user = 489172307
    const pass = 373413098
    let html = "<h3 class='canal'>Canais:</h3>";
    canaisCache.forEach((c, i) => {
        const url = `${server}/${user}/${pass}/${c.stream_id}.m3u8`
        html += `<button onclick="abrirCanal('${url}', '${c.name}')">${c.name}</button>`;
    });
    lista.style.border = '3px solid white'
    lista.innerHTML = html;
}

function abrirCanal(url, canal) {
    const lista = document.getElementById("lista")
    const video = document.getElementById('player');
    const assistindo = document.getElementById('assistindo');
    assistindo.innerHTML = `<b>Assistindo:</b> ${canal}`

    if (Hls.isSupported()) {
        const hls = new Hls();
        hls.loadSource(url);
        hls.attachMedia(video);
        hls.on(Hls.Events.MANIFEST_PARSED, function () {
            video.play();
        });
    } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
        // Safari suporta nativamente
        video.src = url;
        video.play();
    }
}

async function carregarCategoriaSeries() {
    const server = document.getElementById("server").value;
    const user = document.getElementById("user").value;
    const pass = document.getElementById("pass").value;

    const url = `${server}/player_api.php?username=${user}&password=${pass}&action=get_series_categories`;

    try {
        const response = await fetch(url);
        const data = await response.json();
        seriesCache = data;
        //console.log(JSON.stringify(data, null, 2))

        mostrarCategoriaSeries();
    } catch (err) {
        alert(err)
        document.getElementById("lista").innerHTML = "Erro ao carregar categoria de Séries.";
        console.error(err);
    }

}

async function carregarListaSeries(categoria, nome) {
    const server = document.getElementById("server").value;
    const user = document.getElementById("user").value;
    const pass = document.getElementById("pass").value;

    const url = `${server}/player_api.php?username=${user}&password=${pass}&action=get_series&category_id=${categoria}`;

    try {
        const response = await fetch(url);
        const data = await response.json();
        lista_seriesCache = data;
        //console.log(JSON.stringify(data, null, 2))

        mostrarListaSeries(nome);
    } catch (err) {
        alert(err)
        document.getElementById("lista").innerHTML = "Erro ao carregar lista de Séries.";
        console.error(err);
    }

}

function mostrarCategoriaSeries() {
    const lista = document.getElementById("lista")
    let html = "<h3 class='canal'>Séries:</h3>";
    seriesCache.forEach((c, i) => {
        html += `<button onclick="carregarListaSeries('${c.category_id}', '${c.category_name}')">${c.category_name}</button>`;
    });
    lista.style.border = '3px solid white'
    lista.innerHTML = html;
}

async function buscarSeries() {
    const nomeSerie = document.getElementById("pesquisar").value
    const urlSeries = "https://neweraserver10.top:80/get.php?username=489172307&password=373413098&type=m3u&output=m3u8";
    const response = await fetch(urlSeries);
    const texto = await response.text();

    const linhas = texto.split("\n");
    const series = [];

    for (let i = 0; i < linhas.length; i++) {
        if (linhas[i].toLowerCase().includes(nomeSerie.toLowerCase().trim())) {
            const titulo = linhas[i].replace("#EXTINF:-1,", "").trim();
            const novoTitulo = titulo.replace(/S\d{2}E\d{2,3}/i, "").trim();
            series.push({ novoTitulo });
        }
    }

    const lista = document.getElementById("lista")
    let html = `<h3 class='canal'>Buscar por: ${nomeSerie}</h3>`;
    series.forEach((c, i) => {
        html += `<button onclick="carregarEpisodios('${c.novoTitulo}')">${c.novoTitulo}</button>`;
    });
    lista.style.border = '3px solid white'
    lista.innerHTML = html;

}

function reproduzir(url, titulo) {
    const video = document.getElementById('player2');
    const assistindo = document.getElementById('assistindo2');
    assistindo.innerHTML = `<b>Assistindo:</b> ${titulo}`
    video.src = url
    video.play()
}

async function carregarEpisodios(serie, imagem) {
    // URL da lista M3U fornecida pelo provedor
    const urlLista = "https://neweraserver10.top:80/get.php?username=489172307&password=373413098&type=m3u&output=m3u8";
    const response = await fetch(urlLista);
    const texto = await response.text();

    const linhas = texto.split("\n");
    const episodios = [];

    for (let i = 0; i < linhas.length; i++) {
        if (linhas[i].includes(serie)) {
            const titulo = linhas[i].replace("#EXTINF:-1,", "").trim();
            const url = linhas[i + 1].trim(); // a linha seguinte é a URL
            episodios.push({ titulo, url });
        }
    }

    const listaEpisodios = episodios
    const lista = document.getElementById("lista")
    lista.innerHTML = ''
    let html = `<h3 class='canal'>${serie}</h3>`;
    html += `<img src="${imagem}" width="130" height="130" alt="${serie}"><br>`
    listaEpisodios.forEach((c, i) => {
        html += `<button onclick="reproduzir('${c.url}', '${c.titulo}')" >${c.titulo}</button>`;
    });
    lista.style.border = '3px solid white'
    lista.innerHTML = html;
}

function mostrarListaSeries(nome) {
    const lista = document.getElementById("lista")
    let html = `<h3 class='canal'>${nome}:</h3>`;
    lista_seriesCache.forEach((c, i) => {
        html += `<button onclick="carregarEpisodios('${c.name}', '${c.cover}')">${c.name}</button>`;
    });
    lista.style.border = '3px solid white'
    lista.innerHTML = html;
}

async function carregarCategoriaFilmes() {
    const server = document.getElementById("server").value;
    const user = document.getElementById("user").value;
    const pass = document.getElementById("pass").value;

    const url = `${server}/player_api.php?username=${user}&password=${pass}&action=get_vod_categories`;

    try {
        const response = await fetch(url);
        const data = await response.json();
        filmesCache = data;

        mostrarCategoriaFilmes();
    } catch (err) {
        alert(err)
        document.getElementById("lista").innerHTML = "Erro ao carregar categoria de Filmes.";
        console.error(err);
    }

}

function mostrarCategoriaFilmes() {
    const lista = document.getElementById("lista")
    let html = "<h3 class='canal'>Filmes:</h3>";
    filmesCache.forEach((c, i) => {
        html += `<button onclick="carregarListaFilmes('${c.category_id}', '${c.category_name}')">${c.category_name}</button>`;
    });
    lista.style.border = '3px solid white'
    lista.innerHTML = html;
}

async function carregarListaFilmes(categoria, nome) {
    const server = document.getElementById("server").value;
    const user = document.getElementById("user").value;
    const pass = document.getElementById("pass").value;

    const url = `${server}/player_api.php?username=${user}&password=${pass}&action=get_vod_streams&category_id=${categoria}`;

    try {
        const response = await fetch(url);
        const data = await response.json();
        lista_filmesCache = data;

        mostrarListaFilmes(nome);
    } catch (err) {
        alert(err)
        document.getElementById("lista").innerHTML = "Erro ao carregar lista de Filmes.";
        console.error(err);
    }

}

function mostrarListaFilmes(nome) {
    const lista = document.getElementById("lista")
    let html = `<h3 class='canal'>${nome}:</h3>`;
    lista_filmesCache.forEach((c, i) => {
        html += `<button onclick="carregarFilme('${c.stream_icon}', '${c.name}')">${c.name}</button>`;
    });
    lista.style.border = '3px solid white'
    lista.innerHTML = html;
}

async function carregarFilme(imagem, filme) {
    // URL da lista M3U fornecida pelo provedor
    const urlLista = "https://neweraserver10.top:80/get.php?username=489172307&password=373413098&type=m3u&output=m3u8";
    const response = await fetch(urlLista);
    const texto = await response.text();

    const linhas = texto.split("\n");
    const filmes = [];

    for (let i = 0; i < linhas.length; i++) {
        if (linhas[i].includes(filme)) {
            const titulo = linhas[i].replace("#EXTINF:-1,", "").trim();
            const url = linhas[i + 1].trim(); // a linha seguinte é a URL
            filmes.push({ titulo, url });
        }
    }

    //console.log(JSON.stringify(filmes, null, 2))

    const listaFilmes = filmes
    const lista = document.getElementById("lista")
    lista.innerHTML = ''
    let html = `<h3 class='canal'>${filme}</h3>`;
    html += `<img src="${imagem}" width="130" height="130" alt="${filme}"><br>`
    listaFilmes.forEach((c, i) => {
        html += `<button onclick="reproduzir('${c.url}', '${c.titulo}')" >Assistir</button>`;
    });
    lista.style.border = '3px solid white'
    lista.innerHTML = html;
}

carregarCategoria()