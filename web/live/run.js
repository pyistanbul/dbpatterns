var io = require('socket.io').listen(8000),
     _ = require('underscore');

var get_clients = function (channel) {
    // Returns the stored data of the clients of provided channel
    return _.map(io.sockets.clients(channel), function (client) {
        return client.store.data;
    });
};

io.sockets.on('connection', function (socket) {

    var channel = null;

    socket.on("connect", function (data) {
        channel = data.document_id;
        socket.join(channel);
        socket.set("username", data.username);
        socket.emit("enter", {
            "clients": get_clients(channel)
        });
        socket.broadcast.to(channel).emit("join", data.username);
    });

    socket.on("push", function (data) {
        socket.broadcast.to(channel).emit("pull", data);
    });

    socket.on("message", function (data) {
        var message = {
            "body": data,
            "username": socket.store.data["username"]
        };
        socket.broadcast.to(channel).emit("message", message);
        socket.emit("message", message);
    });

    socket.on("disconnect", function () {
        socket.broadcast.to(channel).emit("leave", socket.store.data["username"]);
        socket.leave(channel);
    });

});