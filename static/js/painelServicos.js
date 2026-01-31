const botoes = document.querySelectorAll('.botao-menu')

botoes.forEach((botao) => {
    botao.addEventListener('touchstart', () => {
        botao.style.backgroundColor = '#0056b3'
        botao.style.transform = 'scale(0.9)'
        botao.style.boxShadow = '0 2px 4px rgba(0, 0, 0, 0.2)'
    })

    botao.addEventListener('touchend', () => {
        botao.style.backgroundColor = '#007bff'
        botao.style.transform = 'scale(1)'
        botao.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)'
    })
})