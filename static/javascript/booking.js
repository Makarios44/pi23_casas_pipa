var booking = document.getElementById("booking");
var roomDescription = document.getElementById("roomDescription");

// Define a imagem de fundo fixa inicial
booking.style.backgroundImage = "url('{% static 'img/quarto.jpg' %}')";

// Adiciona um evento de clique à seleção do quarto
document.getElementById("roomOptions").onclick = function() {
    // Atualiza a descrição do quarto se necessário
    // Você pode adicionar mais lógica aqui se necessário

    // Evita alterar a imagem de fundo
    return false;
};
