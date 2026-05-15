let canais = [];
let series = []
let filmes = []

async function carregarCategoria() {
    const box = document.getElementById('box1')
    box.style.display = 'flex'
    const server = document.getElementById("server").value;
    const user = document.getElementById("user").value;
    const pass = document.getElementById("pass").value;

    const url = `${server}/player_api.php?username=${user}&password=${pass}&action=get_live_categories`;
    const urlCanaisAll = `${server}/player_api.php?username=${user}&password=${pass}&action=get_live_streams`;

    try {
        const response = await fetch(url);
        const data = await response.json();
        const responseCanaisAll = await fetch(urlCanaisAll);
        const dataCanaisAll = await responseCanaisAll.json();
        categoriasCache = data;
        canais = dataCanaisAll

        mostrarCategoria();
    } catch (err) {
        box.style.display = 'none'
        alert(err)
        document.getElementById("lista").innerHTML = "Erro ao carregar categoria de Canais.";
        console.error(err);
    }

}
async function carregarCanais(categoria) {
    const box = document.getElementById('box1')
    box.style.display = 'flex'
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
        box.style.display = 'none'
        alert(err)
        document.getElementById("lista").innerHTML = "Erro ao carregar lista de Canais.";
        console.error(err);
    }

}

function buscarCanais() {
    const box = document.getElementById('box1')
    box.style.display = 'flex'
    const categoriaExcluida = '6736'
    const server = document.getElementById("server").value;
    const user = document.getElementById("user").value;
    const pass = document.getElementById("pass").value;
    const listaCanais = canais
    const pesquisa = document.getElementById('pesquisar').value
    const buscarCanal = pesquisa.trim().toLowerCase()
    const listaAtual = listaCanais.filter(c => (c.name || "").toLowerCase().includes(buscarCanal) && c.category_id !== categoriaExcluida)
    const lista = document.getElementById("lista")
    let html = `<h3 class='canal'>Busca por: ${pesquisa}</h3>`;
    html += `<input type="text" id="pesquisar" placeholder="buscar canais...">
             <button onclick="buscarCanais()">Buscar</button>`
    if (listaAtual.length === 0) {
        html += `<p>Nenhum resultado encontrado.</p>`
    } else {
        listaAtual.forEach(c => {
            const url = `${server}/live/${user}/${pass}/${c.stream_id}.m3u8`
            html += `<button onclick="abrirCanal('${url}', '${c.name}')">${c.name}</button>`;
        })
    }
    lista.style.border = '3px solid white'
    lista.innerHTML = html;
    setTimeout(() => {
        box.style.display = 'none'
    }, 1000)
}

function mostrarCategoria() {
    const box = document.getElementById('box1')
    const lista = document.getElementById("lista")
    let html = "<h3 class='canal'>Canais Ao Vivo:</h3>";
    html += `<input type="text" id="pesquisar" placeholder="buscar canais...">
             <button onclick="buscarCanais()">Buscar</button>`
    categoriasCache.forEach((c, i) => {
        html += `<button onclick="carregarCanais('${c.category_id}')">${c.category_name}</button>`;
    });
    lista.style.border = '3px solid white'
    lista.innerHTML = html;
    box.style.display = 'none'
}

function mostrarCanais() {
    const box = document.getElementById('box1')
    const lista = document.getElementById("lista")
    lista.innerHTML = ''
    const server = document.getElementById("server").value;
    const user = document.getElementById("user").value;
    const pass = document.getElementById("pass").value;
    let html = "<h3 class='canal'>Canais:</h3>";
    canaisCache.forEach((c, i) => {
        const url = `${server}/live/${user}/${pass}/${c.stream_id}.m3u8`
        html += `<button onclick="abrirCanal2('${url}', '${c.name}')">${c.name}</button>`;
    });
    lista.style.border = '3px solid white'
    lista.innerHTML = html;
    box.style.display = 'none'
}

function abrirCanal(url, canal) {
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

async function abrirCanal2(urlCanal, canal) {
    const box = document.getElementById('box1')
    box.style.display = 'flex'
    const video = document.getElementById('player');
    const assistindo = document.getElementById('assistindo');

    // busca o manifest original
    const res = await fetch(urlCanal, { redirect: 'follow' });
    const fixedUrl = res.url

    // usa no Hls.js
    if (Hls.isSupported()) {
        const hls = new Hls();
        hls.loadSource(fixedUrl);
        hls.attachMedia(video);
        hls.on(Hls.Events.MANIFEST_PARSED, function () {
            video.play();
            box.style.display = 'none'
            assistindo.innerHTML = `<b>Assistindo:</b> ${canal}`
        });
    } else if (video.canPlayType("application/vnd.apple.mpegurl")) {
        video.src = fixedUrl;
        video.play()
        box.style.display = 'none'
        assistindo.innerHTML = `<b>Assistindo:</b> ${canal}`
    }
}

async function carregarCategoriaSeries() {
    const box = document.getElementById('box1')
    box.style.display = 'flex'
    const server = document.getElementById("server").value;
    const user = document.getElementById("user").value;
    const pass = document.getElementById("pass").value;

    const url = `${server}/player_api.php?username=${user}&password=${pass}&action=get_series_categories`;
    const urlSeriesAll = `${server}/player_api.php?username=${user}&password=${pass}&action=get_series`;

    try {
        const response = await fetch(url);
        const data = await response.json();
        const responseSeriesAll = await fetch(urlSeriesAll);
        const dataSeriesAll = await responseSeriesAll.json();
        seriesCache = data;
        series = dataSeriesAll
        //console.log(JSON.stringify(data, null, 2))

        mostrarCategoriaSeries();
    } catch (err) {
        box.style.display = 'none'
        alert(err)
        document.getElementById("lista").innerHTML = "Erro ao carregar categoria de Séries.";
        console.error(err);
    }

}

async function carregarListaSeries(categoria, nome) {
    const box = document.getElementById('box1')
    box.style.display = 'flex'
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
        box.style.display = 'none'
        alert(err)
        document.getElementById("lista").innerHTML = "Erro ao carregar lista de Séries.";
        console.error(err);
    }
}

async function carregarEpisodiosSeries(series_id, nome, imagem) {
    const box = document.getElementById('box1')
    box.style.display = 'flex'
    const server = document.getElementById("server").value;
    const user = document.getElementById("user").value;
    const pass = document.getElementById("pass").value;

    const url = `${server}/player_api.php?username=${user}&password=${pass}&action=get_series_info&series_id=${series_id}`;

    try {
        const response = await fetch(url);
        const data = await response.json();
        episodios_seriesCache = data;
        //console.log(JSON.stringify(data, null, 2))

        mostrarEpisodiosSeries(nome, imagem);
    } catch (err) {
        box.style.display = 'none'
        alert(err)
        document.getElementById("lista").innerHTML = "Erro ao carregar Eposódios da Série.";
        console.error(err);
    }
}

function mostrarCategoriaSeries() {
    const box = document.getElementById('box1')
    const lista = document.getElementById("lista")
    let html = "<h3 class='canal'>Séries:</h3>";
    html += `<input type="text" id="pesquisar" placeholder="buscar séries...">
             <button onclick="buscarSeries()">Buscar</button>`
    seriesCache.forEach((c, i) => {
        html += `<button onclick="carregarListaSeries('${c.category_id}', '${c.category_name}')">${c.category_name}</button>`;
    });
    lista.style.border = '3px solid white'
    lista.innerHTML = html;
    box.style.display = 'none'
}

function buscarSeries() {
    const box = document.getElementById('box1')
    box.style.display = 'flex'
    const server = document.getElementById("server").value;
    const user = document.getElementById("user").value;
    const pass = document.getElementById("pass").value;
    const listaSeries = series
    const pesquisa = document.getElementById('pesquisar').value
    const buscarSerie = pesquisa.trim().toLowerCase()
    const listaAtual = listaSeries.filter(c => (c.name || "").toLowerCase().includes(buscarSerie))
    const lista = document.getElementById("lista")
    let html = `<h3 class='canal'>Busca por: ${pesquisa}</h3>`;
    html += `<input type="text" id="pesquisar" placeholder="buscar séries...">
             <button onclick="buscarSeries()">Buscar</button>`
    if (listaAtual.length === 0) {
        html += `<p>Nenhum resultado encontrado.</p>`
    } else {
        listaAtual.forEach(c => {
            html += `<button onclick="carregarEpisodiosSeries('${c.series_id}', '${c.name}', '${c.cover}')">${c.name}</button>`;
        })
    }
    lista.style.border = '3px solid white'
    lista.innerHTML = html;
    setTimeout(() => {
        box.style.display = 'none'
    }, 1000)
}

function reproduzirSeries(ep_id, ep_titulo) {
    const server = document.getElementById("server").value;
    const user = document.getElementById("user").value;
    const pass = document.getElementById("pass").value;
    const url = `${server}/series/${user}/${pass}/${ep_id}.mp4`
    const video = document.getElementById('player');
    const assistindo = document.getElementById('assistindo');
    assistindo.innerHTML = `<b>Assistindo:</b> ${ep_titulo}`
    video.src = url
    video.play()
}

async function mostrarEpisodiosSeries(serieNome, imagem) {
    const box = document.getElementById('box1')
    const lista = document.getElementById("lista")
    serie = episodios_seriesCache
    lista.innerHTML = ''
    let html = `<h3 class='canal'>${serieNome}</h3>`;
    html += `<img src="${imagem}" width="130" height="130" alt="${serieNome}"><br>`
    for (const temporada in serie.episodes) {
        //console.log('Temporada: ', temporada)
        serie.episodes[temporada].forEach((ep) => {
            //console.log(ep.title)
            html += `<button onclick="reproduzirSeries('${ep.id}', '${ep.title}')">${ep.title}</button>`;
        })
    }
    lista.style.border = '3px solid white'
    lista.innerHTML = html;
    box.style.display = 'none'
}

function mostrarListaSeries(nome) {
    const box = document.getElementById('box1')
    const lista = document.getElementById("lista")
    let html = `<h3 class='canal'>${nome}:</h3>`;
    lista_seriesCache.forEach((c, i) => {
        html += `<button onclick="carregarEpisodiosSeries('${c.series_id}', '${c.name}', '${c.cover}')">${c.name}</button>`;
    });
    lista.style.border = '3px solid white'
    lista.innerHTML = html;
    box.style.display = 'none'
}

async function carregarCategoriaFilmes() {
    const box = document.getElementById('box1')
    box.style.display = 'flex'
    const server = document.getElementById("server").value;
    const user = document.getElementById("user").value;
    const pass = document.getElementById("pass").value;

    const url = `${server}/player_api.php?username=${user}&password=${pass}&action=get_vod_categories`;
    const urlFilmesAll = `${server}/player_api.php?username=${user}&password=${pass}&action=get_vod_streams`;

    try {
        const response = await fetch(url);
        const data = await response.json();
        const responseFimesAll = await fetch(urlFilmesAll);
        const dataFilmesAll = await responseFimesAll.json();
        filmesCache = data;
        filmes = dataFilmesAll

        mostrarCategoriaFilmes();
    } catch (err) {
        box.style.display = 'none'
        alert(err)
        document.getElementById("lista").innerHTML = "Erro ao carregar categoria de Filmes.";
        console.error(err);
    }

}

function mostrarCategoriaFilmes() {
    const box = document.getElementById('box1')
    const lista = document.getElementById("lista")
    let html = "<h3 class='canal'>Filmes:</h3>";
    html += `<input type="text" id="pesquisar" placeholder="buscar filmes...">
             <button onclick="buscarFilmes()">Buscar</button>`
    filmesCache.forEach((c, i) => {
        html += `<button onclick="carregarListaFilmes('${c.category_id}', '${c.category_name}')">${c.category_name}</button>`;
    });
    lista.style.border = '3px solid white'
    lista.innerHTML = html;
    box.style.display = 'none'
}

async function carregarListaFilmes(categoria, nome) {
    const box = document.getElementById('box1')
    box.style.display = 'flex'
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
        box.style.display = 'none'
        alert(err)
        document.getElementById("lista").innerHTML = "Erro ao carregar lista de Filmes.";
        console.error(err);
    }
}

async function carregarInfoFilmes(filme_id, imagem, filmeNome) {
    const box = document.getElementById('box1')
    box.style.display = 'flex'
    const server = document.getElementById("server").value;
    const user = document.getElementById("user").value;
    const pass = document.getElementById("pass").value;

    const url = `${server}/player_api.php?username=${user}&password=${pass}&action=get_vod_info&vod_id=${filme_id}`;

    try {
        const response = await fetch(url);
        const data = await response.json();
        info_filmesCache = data;

        carregarFilme(filme_id, imagem, filmeNome);
    } catch (err) {
        box.style.display = 'none'
        alert(err)
        document.getElementById("lista").innerHTML = "Erro ao carregar Informações do Filme.";
        console.error(err);
    }
}

function mostrarListaFilmes(nome) {
    const box = document.getElementById('box1')
    const lista = document.getElementById("lista")
    let html = `<h3 class='canal'>${nome}:</h3>`;
    lista_filmesCache.forEach((c, i) => {
        html += `<button onclick="carregarInfoFilmes('${c.stream_id}', '${c.stream_icon}', '${c.name}')">${c.name}</button>`;
    });
    lista.style.border = '3px solid white'
    lista.innerHTML = html;
    box.style.display = 'none'
}

function carregarFilme(filme_id, imagem, filmeNome) {
    const box = document.getElementById('box1')
    const lista = document.getElementById("lista")
    lista.innerHTML = ''
    let html = `<h3 class='canal'>${filmeNome}</h3>`;
    html += `<img src="${imagem}" width="130" height="130" alt="${filmeNome}"><br>`
    html += `<button onclick="reproduzirFilmes('${filme_id}', '${filmeNome}')" >Assistir</button>`
    lista.style.border = '3px solid white'
    lista.innerHTML = html;
    box.style.display = 'none'
}

function reproduzirFilmes(filme_id, filmeNome) {
    const server = document.getElementById("server").value;
    const user = document.getElementById("user").value;
    const pass = document.getElementById("pass").value;
    const url = `${server}/movie/${user}/${pass}/${filme_id}.mp4`
    const video = document.getElementById('player');
    const assistindo = document.getElementById('assistindo');
    assistindo.innerHTML = `<b>Assistindo:</b> ${filmeNome}`
    video.src = url
    video.play()
}

function buscarFilmes() {
    const box = document.getElementById('box1')
    box.style.display = 'flex'
    const listaFilmes = filmes
    const pesquisa = document.getElementById('pesquisar').value
    const buscarFilme = pesquisa.trim().toLowerCase()
    const listaAtual = listaFilmes.filter(c => (c.name || "").toLowerCase().includes(buscarFilme))
    const lista = document.getElementById("lista")
    let html = `<h3 class='canal'>Busca por: ${pesquisa}</h3>`;
    html += `<input type="text" id="pesquisar" placeholder="buscar filmes...">
             <button onclick="buscarFilmes()">Buscar</button>`
    if (listaAtual.length === 0) {
        html += `<p>Nenhum resultado encontrado.</p>`
    } else {
        listaAtual.forEach(c => {
            html += `<button onclick="carregarInfoFilmes('${c.stream_id}', '${c.stream_icon}', '${c.name}')">${c.name}</button>`;
        })
    }
    lista.style.border = '3px solid white'
    lista.innerHTML = html;
    setTimeout(() => {
        box.style.display = 'none'
    }, 1000)
}

carregarCategoria()