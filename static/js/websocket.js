// Connect to the WebSocket server
var socket = io.connect('http://' + document.domain + ':' + location.port);

// Define a function to handle the 'update_progress' event
socket.on('update_progress', function(data) {
    // Update progress bars with data received from the server
    document.getElementById('progress-bar-1').value = data.progress_1;
    document.getElementById('progress-bar-2').value = data.progress_2;

    // Update notifications if needed
    updateNotifications(data.notifications_1, data.notifications_2);
});

// Function to update notifications
function updateNotifications(notifications_1, notifications_2) {
    // Update notifications in the UI
    // For example, you could update a list of notifications
}
