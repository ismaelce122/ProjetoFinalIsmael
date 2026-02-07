let contador = 0
let html = ''

fetch('https://ismaelce122.pythonanywhere.com/api/pecas')
    .then(resposta => resposta.json())
    .then(listaPecas => {
        listaPecas.forEach((peca) => {
            html += `<option value="${peca.nome}-${peca.preco}">${peca.nome}</option>`
        })
    })
    .catch(err => console.error('Erro ao Buscar Dados: ', err))

const AddItem = () => {
    contador++
    const item = document.getElementById('itens_os')
    const box = document.createElement('div')
    box.id = 'item-' + contador
    box.classList.add('row')
    box.innerHTML = `
                    <div class="col-4">
                        <label class="form-label" for="peca">Peça:</label>
                        <select name="peca[]" class="opcoes form-select">
                            <option value="">-- selecione a peça --</option>
                            +${html}
                        </select>
                    </div>
                    <div class="col-4">
                        <label class="form-label" for="quantidade[]">Quantidade:</label>
                        <input class="form-control" type="number" name="quantidade[]">
                    </div>
                    <div class="col-4 d-flex align-items-end">
                        <button type="button" onclick="ExcluirItem('item-${contador}')" class="btn btn-danger">
                            <i class="fa fa-trash"></i>
                            Excluir Item
                        </button>
                    </div>
                    `
    item.appendChild(box)
}

const ExcluirItem = (id) => {
    const item = document.getElementById(id)
    item.remove(item)
}
