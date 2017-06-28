const WebSocket = require('ws'),
    wsPort = 9999,
    wss = new WebSocket.Server({ port: wsPort });

console.log(`WebSocket server listening at port ${wsPort}`)

wss.on('connection', function connection(ws) {
  ws.on('message', function incoming(message) {
    console.log("-->", message);
    streamPosition(ws);
  });
});

function streamPosition(ws) {
    let pos = [-75.166493, 39.9060534],
        toAdd = 0.000005,
        interval = 1000 // in milliseconds

    setInterval(() => {
        pos[0] = pos[0] + toAdd;
        pos[1] = pos[1] + toAdd;
        console.log(JSON.stringify(pos));
        ws.send(`${pos[0]} ${pos[1]}`);
    }, interval)
}