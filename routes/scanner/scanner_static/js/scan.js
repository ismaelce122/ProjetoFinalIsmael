let texto = []
let box = document.getElementById('resultado')

const Scannear = (decodedText, decodedResult) => {
    if (!texto.includes(decodedText)) {
        texto = []
        document.getElementById("beep").play()
        let resultado = document.createElement('h2')
        texto.push(decodedText)
        resultado.textContent = texto
        box.appendChild(resultado)
    }
}

let html5QrCode = new Html5Qrcode("reader")
html5QrCode.start(
    { facingMode: "environment" }, // câmera traseira
    { fps: 10, qrbox: 250 },
    Scannear
)