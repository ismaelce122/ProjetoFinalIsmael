let texto = []
const box = document.getElementById('resultado')

const Scannear = (decodedText, decodedResult) => {
    if (!texto.includes(decodedText)) {
        texto = []
        document.getElementById("beep").play()
        let resultado = document.createElement('h2')
        texto.push(decodedText)
        resultado.textContent = decodedText
        box.appendChild(resultado)
    } else {
        alert('Erro ao ler Qr Code!!!')
    }
}

let html5QrCode = new Html5Qrcode("reader")
html5QrCode.start(
    { facingMode: "environment" }, // câmera traseira
    { fps: 10, qrbox: 250 },
    Scannear
)

const ReiniciarScanner = () => {
    texto = []
    alert('Scanner Reiniciado!!!')
}