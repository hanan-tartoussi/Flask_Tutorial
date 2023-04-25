$(document).ready(function() {

    var socket = io.connect('http://127.0.0.1:5000');

    var socket_messages = io('http://127.0.0.1:5000/messages')

    $('#send').on('click', function() {
        var message = $('#message').val();

        socket_messages.emit('message from user', message);

    });

    socket_messages.on('from flask', function(msg) {
        alert(msg);
    });

    socket.on('server orginated', function(msg) {
        alert(msg);
    });

    var private_socket = io('http://127.0.0.1:5000/private')

    $('#send_username').on('click', function() {
        private_socket.emit('username', $('#username').val());
    });

    $('#send_private_message').on('click', function() {
        var recipient = $('#send_to_username').val();
        var message_to_send = $('#private_message').val();

        private_socket.emit('private_message', {'username' : recipient, 'message' : message_to_send});
    });

    private_socket.on('new_private_message', function(msg) {
        alert(msg);
    });

    $('#join_room').on('click', function() {
        var room = $('#room_to_join').val();

        private_socket.emit('join_room', room);
    });

    private_socket.on('room_message', function(msg) {
        alert(msg);
    });

    $('#leave_room').on('click', function() {
        var room = $('#room_to_join').val();

        private_socket.emit('leave_the_room', room);
    });


    /*

    socket.on('connect', function() {
    
        socket.send('I am now connected!');

        socket.emit('custom event', {'name' : 'Anthony'});

        socket.on('from flask', function(msg) {
            alert(msg['extension']);
        });

        socket.on('message', function(msg) {
            alert(msg);
        });
        
    });

    */

});