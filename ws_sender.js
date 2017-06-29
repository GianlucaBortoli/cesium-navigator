const WebSocket = require('ws'),
    wsPort = 9999,
    wss = new WebSocket.Server({ port: wsPort });

const INTERVAL = process.argv[2] || 200; // in milliseconds

console.log(`WebSocket server listening on port ${wsPort}`);
console.log(`Interval: ${INTERVAL}`)

wss.on('connection', function connection(ws) {
  ws.on('message', function incoming(message) {
    // extract initial position from 1st message sent by client
    let received = message.split(' '),
        x = Number(received[0]),
        y = Number(received[1]),
        rotation = Number(received[2]);
    console.log(`x: {x}\ny: ${y}\nrotation: ${rotation}`);
    streamPosition(ws, [x, y, rotation]);
  });
});

/*
* Fake position & rotation for the browser
* A message has the following form:
* "<lat> <long> <rotation>"
*/
function streamPosition(ws, pos) {
    const toAdd = 0.000005;
    // send data every INTERVAL cs
    setInterval(() => {
        pos[0] = pos[0] + toAdd;
        pos[1] = pos[1] + toAdd;
        console.log(JSON.stringify(pos));
        ws.send(`${pos[0]} ${pos[1]} ${pos[2]}`);
    }, INTERVAL)
}

function degToRad(degrees) {
    return degrees * Math.PI / 180;
}