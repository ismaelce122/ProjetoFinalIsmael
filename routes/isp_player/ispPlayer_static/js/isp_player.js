let canais = []
let series = []
let filmes = []
let urlAtual = null
let canalAtual = null

function atualizarHora() {
    const agora = new Date()
    const horas = agora.getHours().toString().padStart(2, '0')
    const minutos = agora.getMinutes().toString().padStart(2, '0')
    const segundos = agora.getSeconds().toString().padStart(2, '0')
    document.getElementById('hora').textContent = `${horas}:${minutos}:${segundos}`
}
    
setInterval(atualizarHora, 1000)
atualizarHora()

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
             <button onclick="buscarCanais()" tabindex="0">Buscar</button>`
    if (listaAtual.length === 0) {
        html += `<p>Nenhum resultado encontrado.</p>`
    } else {
        listaAtual.forEach(c => {
            const url = `${server}/live/${user}/${pass}/${c.stream_id}.m3u8`
            html += `<button onclick="abrirCanal('${url}', '${c.name}')" tabindex="0">${c.name}</button>`;
        })
    }
    lista.innerHTML = html;
    setTimeout(() => {
        box.style.display = 'none'
    }, 1000)
}

function mostrarCategoria() {
    const box = document.getElementById('box1')
    const lista = document.getElementById("lista")
    const video = document.getElementById('box_player')
    const divRemover = document.getElementById("container")
    if(divRemover) {
        divRemover.remove()
    }
    video.style.display = 'block'
    lista.style.display = 'flex'
    lista.innerHTML = ''
    let html = "<h3 class='canal'>Canais Ao Vivo:</h3>";
    html += `<input type="text" id="pesquisar" placeholder="buscar canais...">
             <button onclick="buscarCanais()" tabindex="0">Buscar</button>`
    categoriasCache.forEach((c, i) => {
        html += `<button onclick="carregarCanais('${c.category_id}')" tabindex="0">${c.category_name}</button>`;
    });
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
        html += `<button onclick="abrirCanal('${url}', '${c.name}')" tabindex="0">${c.name}</button>`;
    });
    lista.innerHTML = html;
    box.style.display = 'none'
}

function abrirCanal(url, canal) {
    let tempo = 0
    let contador = 0
    urlAtual = url
    canalAtual = canal
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

    let monitorId = setInterval(() => {
        if(contador < 5) {
          contador++
        } else if(contador === 5){
             if(video.currentTime === tempo) {
                        clearInterval(monitorId)
                        abrirCanal(urlAtual, canalAtual)
                    }
          }
          tempo = video.currentTime
    }, 10000)
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
    const video = document.getElementById('box_player')
    const divRemover = document.getElementById("container")
    if(divRemover) {
        divRemover.remove()
    }
    video.style.display = 'none'
    lista.style.display = 'flex'
    let html = "<h3 class='canal'>Séries:</h3>";
    html += `<input type="text" id="pesquisar" placeholder="buscar séries...">
             <button onclick="buscarSeries()" tabindex="0">Buscar</button>`
    seriesCache.forEach((c, i) => {
        html += `<button onclick="carregarListaSeries('${c.category_id}', '${c.category_name}')" tabindex="0">${c.category_name}</button>`;
    });
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
             <button onclick="buscarSeries()" tabindex="0">Buscar</button>`
    if (listaAtual.length === 0) {
        html += `<p>Nenhum resultado encontrado.</p>`
    } else {
        listaAtual.forEach(c => {
            html += `<button onclick="carregarEpisodiosSeries('${c.series_id}', '${c.name}', '${c.cover}')">
                        <img src="${c.cover}" alt="${c.name}">${c.name}
                     </button>
                    `
        })
    }
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
    const video = document.getElementById('box_player')
    const divRemover = document.getElementById("container")
    if(divRemover) {
        divRemover.remove()
    }
    video.style.display = 'block'
    lista.style.display = 'flex'
    serie = episodios_seriesCache
    lista.innerHTML = ''
    let html = `<h3 class='canal'>${serieNome}</h3>`;
    html += `<img src="${imagem}" alt="${serieNome}"><br>`
    for (const temporada in serie.episodes) {
        //console.log('Temporada: ', temporada)
        serie.episodes[temporada].forEach((ep) => {
            //console.log(ep.title)
            html += `<button onclick="reproduzirSeries('${ep.id}', '${ep.title}')" tabindex="0">${ep.title}</button>`;
        })
    }
    lista.innerHTML = html;
    box.style.display = 'none'
}

function mostrarListaSeries(nome) {
    const box = document.getElementById('box1')
    const lista = document.getElementById("lista")
    const video = document.getElementById('box_player')
    const boxPai = document.getElementById('box_pai')
    const boxCard = document.createElement("div")
    const boxTitulo = document.createElement("div")
    const card = document.createElement("div")
    const boxBotoes = document.createElement("div")
    video.style.display = 'none'
    boxCard.id = "container"
    card.classList.add("box_card")
    boxPai.appendChild(boxCard)
    boxCard.appendChild(boxTitulo)
    boxCard.appendChild(boxBotoes)
    boxBotoes.appendChild(card)
    let html = ''
    let html2 = `<h3 class='canal'>${nome}:</h3>`
    lista_seriesCache.forEach((c, i) => {
        html += `<button onclick="carregarEpisodiosSeries('${c.series_id}', '${c.name}', '${c.cover}')">
                     <img src="${c.cover}" alt="${c.name}">${c.name}
                 </button>
                `
    });
    lista.style.display = 'none'
    card.innerHTML = html;
    boxTitulo.innerHTML = html2
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
    const video = document.getElementById('box_player')
    const divRemover = document.getElementById("container")
    if(divRemover) {
         divRemover.remove()
    }
    video.style.display = 'none'
    lista.style.display = 'flex'
    let html = "<h3 class='canal'>Filmes:</h3>";
    html += `<input type="text" id="pesquisar" placeholder="buscar filmes...">
             <button onclick="buscarFilmes()" tabindex="0">Buscar</button>`
    filmesCache.forEach((c, i) => {
        html += `<button onclick="carregarListaFilmes('${c.category_id}', '${c.category_name}')" tabindex="0">${c.category_name}</button>`;
    });
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
    const video = document.getElementById('box_player')
    const boxPai = document.getElementById('box_pai')
    const boxCard = document.createElement("div")
    const boxTitulo = document.createElement("div")
    const card = document.createElement("div")
    const boxBotoes = document.createElement("div")
    video.style.display = 'none'
    boxCard.id = "container"
    card.classList.add("box_card")
    boxPai.appendChild(boxCard)
    boxCard.appendChild(boxTitulo)
    boxCard.appendChild(boxBotoes)
    boxBotoes.appendChild(card)
    let html = ''
    let html2 = `<h3 class='canal'>${nome}:</h3>`;
    lista_filmesCache.forEach((c, i) => {
        html += `<button onclick="carregarInfoFilmes('${c.stream_id}', '${c.stream_icon}', '${c.name}')">
                    <img src="${c.stream_icon}" alt="${c.name}">${c.name}
                 </button>
                `
    });
    lista.style.display = 'none'
    card.innerHTML = html;
    boxTitulo.innerHTML = html2
    box.style.display = 'none'
}

function carregarFilme(filme_id, imagem, filmeNome) {
    const divRemover = document.getElementById("container")
    if(divRemover) {
       divRemover.remove()
    }
    const box = document.getElementById('box1')
    const lista = document.getElementById("lista")
    const video = document.getElementById('box_player')
    lista.style.display = 'flex'
    lista.innerHTML = ''
    video.style.display = 'block'
    let html = `<h3 class='canal'>${filmeNome}</h3>`;
    html += `<img src="${imagem}" alt="${filmeNome}"><br>`
    html += `<button onclick="reproduzirFilmes('${filme_id}', '${filmeNome}')" tabindex="0">Assistir</button>`
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
             <button onclick="buscarFilmes()" tabindex="0">Buscar</button>`
    if (listaAtual.length === 0) {
        html += `<p>Nenhum resultado encontrado.</p>`
    } else {
        listaAtual.forEach(c => {
            html += `<button onclick="carregarInfoFilmes('${c.stream_id}', '${c.stream_icon}', '${c.name}')">
                        <img src="${c.stream_icon}" alt="${c.name}">${c.name}
                     </button>
                    `
        })
    }
    lista.innerHTML = html;
    setTimeout(() => {
        box.style.display = 'none'
    }, 1000)
}

carregarCategoria()
