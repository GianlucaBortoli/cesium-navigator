const WebSocket = require('ws'),
    wsPort = 9999,
    wss = new WebSocket.Server({ port: wsPort });

const INTERVAL = process.argv[2] || 500; // in milliseconds
const NUM_POSITION = process.argv[3] || 50; // the # of positions to be sent
const MOVE_POINT = process.argv[4] || true; // if the point has move or not

console.log(`WebSocket server listening on port ${wsPort}`);
console.log(`Interval: ${INTERVAL}`);
console.log(`Sending ${NUM_POSITION} position(s)`);
console.log(`Point moving: ${MOVE_POINT}`);

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
    let posToAdd = rotToAdd = 0;
    if (MOVE_POINT) {
        posToAdd = 0.000005;
        rotToAdd = 1;
    }

    let duePositions = NUM_POSITION;
    // send data every INTERVAL ms
    let streamInterval = setInterval(() => {
        pos[0] += posToAdd;
        pos[1] += posToAdd * 2;
        pos[2] += rotToAdd;

        ws.send(`${pos[0]} ${pos[1]} ${pos[2]}`, err => {
            duePositions--;
            if (err) {
                console.log("Error", err);
                console.log("Exting");
                process.exit(1);
            }
            // stop sending data when done
            if (duePositions === 0) {
                console.log('Stopped sending position');
                clearInterval(streamInterval);
                process.exit(0);
            }
        });
    }, INTERVAL);
}

// main
main();