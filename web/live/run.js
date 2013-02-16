var io = require('socket.io').listen(8000);

io.sockets.on('connection', function (socket) {

    var channel = null;

    socket.on("connect", function (data) {
        channel = data.document_id;
        socket.join(channel);
        socket.broadcast.to(channel).send(data.username + " joined.");
    });

    socket.on("push", function (data) {
        socket.broadcast.to(channel).emit("pull", data);
    });

});