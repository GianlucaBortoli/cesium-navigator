const WebSocket = require('ws'),
    wsPort = 9999,
    wss = new WebSocket.Server({ port: wsPort });

const INTERVAL = process.argv[2] || 500; // in milliseconds

console.log(`WebSocket server listening on port ${wsPort}`);
console.log(`Interval: ${INTERVAL}`)

/*
* The main ws loop
*/
function main() {
    console.log("Starting main");

    wss.on('connection', function connection(ws) {
        ws.on('message', function incoming(message) {
            // extract initial position from 1st message sent by client
            let received = message.split(' '),
                x = Number(received[0]),
                y = Number(received[1]),
                rotation = Number(received[2]);
            console.log(`x: ${x}\ny: ${y}\nrotation: ${rotation}`);
            streamPosition(ws, [x, y, rotation]);
        });
    });
}

/*
* Fake position & rotation for the browser
* A message has the following form:
* "<lat> <long> <rotation>"
*/
function streamPosition(ws, pos) {
    const posToAdd = 0.000005,
        rotToAdd = 1;
    // send data every INTERVAL ms
    setInterval(() => {
        pos[0] += posToAdd;
        pos[1] += posToAdd * 2;
        pos[2] += rotToAdd;
        //console.log(pos);
        ws.send(`${pos[0]} ${pos[1]} ${pos[2]}`, err => {
            if (err) {
                console.log("Error", err);
                console.log("Exting");
                process.exit(1);
            }
        });
    }, INTERVAL);
}

function degToRad(degrees) {
    return degrees * Math.PI / 180;
}

// main
main();
