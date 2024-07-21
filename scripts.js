var canvas = document.getElementById('canvasEl');
var context = canvas.getContext('2d');

// Рисуем прямоугольник
context.fillStyle = 'red';
context.fillRect(50, 50, 100, 100);

// Рисуем линию
context.beginPath();
context.moveTo(200, 200);
context.lineTo(300, 300);
context.stroke();

// Рисуем текст
context.font = '30px Arial';
context.fillText('Hello, Canvas!', 100, 200);

navigator.mediaDevices.getUserMedia({ video: true })
  .then(function(stream) {
    // Получение доступа к видеопотоку
    var videoElement = document.getElementById('videoEl');
    videoElement.srcObject = stream;
    videoElement.play();
  })
  .catch(function(err) {
    console.error('Ошибка при получении доступа к камере:', err);
  });