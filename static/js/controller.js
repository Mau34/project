 document.addEventListener('DOMContentLoaded', function () {
    const socket = io.connect('http://' + document.domain + ':' + location.port);

    socket.on('temp', (data) => {
        console.log("Hay temp");
        document.getElementById('temperature').innerHTML = 'Temperature: ' + data;
    });

    socket.on('speed', (data) => {
        console.log("Hay speed");
        document.getElementById('motorSpeed').innerHTML = 'Motor Speed: ' + data;
    });

    socket.on('disconect', (data) => {
        console.log("No data");
        document.getElementById('temperature').innerHTML = "msg: " + data;
    });

    const left = document.getElementById('left');
    const rigth = document.getElementById('rigth');

    // Manejar el evento submit del formulario
    left.addEventListener('click', function (e) {
        // Enviar el evento 'action' con el valor del número al servidor a través de Socket.io
        socket.emit('left', { value: 0});
    });

    rigth.addEventListener('click', function (e) {
        // Enviar el evento 'action' con el valor del número al servidor a través de Socket.io
        socket.emit('right', {value : 1});
    });
});