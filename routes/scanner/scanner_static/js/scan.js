let texto = ''
let box = document.getElementById('resultado')

const Scannear = (decodedText, decodedResult) => {
    document.getElementById("beep").play()
    let resultado = document.createElement('h2')
    texto = decodedText
    resultado.textContent = texto
    box.appendChild(resultado)
    texto = ''
}

let html5QrCode = new Html5Qrcode("reader")
html5QrCode.start(
    { facingMode: "environment" }, // câmera traseira
    { fps: 10, qrbox: 250 },
    Scannear
)