const formLogin = document.getElementById('formLogin');
const formCadastro = document.getElementById('formCadastro');
const leftButton = document.getElementById('leftButton');
const leftText = document.getElementById('leftText');
const leftTitle = document.getElementById('leftTitle');

function mostrarCadastro() {
    // Troca formulário
    formLogin.classList.remove('fade-in', 'show');
    formLogin.classList.add('fade-out');

    formLogin.addEventListener('animationend', () => {
        formLogin.style.display = 'none';
        formLogin.classList.remove('fade-out');

        formCadastro.style.display = 'block';
        formCadastro.classList.add('show', 'fade-in');
    }, { once: true });

    // Troca conteúdo da esquerda
    leftButton.classList.add('fade-button-out');
    leftText.classList.add('fade-button-out');
    leftTitle.classList.add('fade-button-out');

    leftButton.addEventListener('animationend', () => {
        leftButton.classList.remove('fade-button-out');
        leftText.classList.remove('fade-button-out');
        leftTitle.classList.remove('fade-button-out');

        leftButton.innerText = 'Voltar ao login';
        leftButton.setAttribute('onclick', 'voltarLogin()');
        leftText.innerText = 'Já tem uma conta?';
        leftTitle.innerText = '';

        leftButton.classList.add('fade-button-in');
        leftText.classList.add('fade-button-in');
        leftTitle.classList.add('fade-button-in');
    }, { once: true });
}

function voltarLogin() {
    // Troca formulário
    formCadastro.classList.remove('fade-in', 'show');
    formCadastro.classList.add('fade-out');

    formCadastro.addEventListener('animationend', () => {
        formCadastro.style.display = 'none';
        formCadastro.classList.remove('fade-out');

        formLogin.style.display = 'block';
        formLogin.classList.add('show', 'fade-in');
    }, { once: true });

    // Troca conteúdo da esquerda
    leftButton.classList.add('fade-button-out');
    leftText.classList.add('fade-button-out');
    leftTitle.classList.add('fade-button-out');

    leftButton.addEventListener('animationend', () => {
        leftButton.classList.remove('fade-button-out');
        leftText.classList.remove('fade-button-out');
        leftTitle.classList.remove('fade-button-out');

        leftButton.innerText = 'Cadastre-se';
        leftButton.setAttribute('onclick', 'mostrarCadastro()');
        leftText.innerText = 'Se não tem uma conta?';
        leftTitle.innerText = 'Seja Bem-Vindo a ISP Serviços!';

        leftButton.classList.add('fade-button-in');
        leftText.classList.add('fade-button-in');
        leftTitle.classList.add('fade-button-in');
    }, { once: true });
}

window.onload = () => {
    formLogin.style.display = 'block';
    formLogin.classList.add('show', 'fade-in');
};