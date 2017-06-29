// global options
const cameraHeight = 100;
let viewerOpts = {
    infoBox: false,
    timeline: false,
    navigationHelpButton: false,
    geocoder: false,
    baseLayerPicker : false,
    homeButton: false,
    animation: false,
    navigationInstructionsInitiallyVisible: false,
    clockViewModel: undefined
};
let flyToOpts = {
    duration: 0.1
};
let viewer = new Cesium.Viewer('cesiumContainer', viewerOpts),
    scene = viewer.scene;
// set fps counter
scene.debugShowFramesPerSecond = true;
// the point moving on the map
let initialPosition = [-75.166493, 39.9060534, 0],
    pointId = "mypoint",
    point = {
        id: pointId,
        position : Cesium.Cartesian3.fromDegrees(
            initialPosition[0], initialPosition[1], initialPosition[2]
        ),
        point : {
            pixelSize : 5,
            color : Cesium.Color.RED,
            outlineColor : Cesium.Color.WHITE,
            outlineWidth : 2
    }
};
// initial camera positioning
viewer.camera.flyTo({
    destination : Cesium.Cartesian3.fromDegrees(
        initialPosition[0], initialPosition[1], cameraHeight
    )
});
// add point to map
viewer.entities.add(point);
viewer.flyTo(point, flyToOpts).then(() => {
    setTimeout(() => {
        // leave some time to 1st camera positioning
        // and start to move point according to data received
        // from websocket
        movePoint()
    }, 3000);
});

/*
* Moves the point on the map according to data received from the websocket
* Data has the following form: [lat, long, direction]
*/
function movePoint() {
    let port = 9999,
        socket = new WebSocket(`ws://localhost:${port}`);

    socket.onopen = function () {
        socket.send('client connected');
    };

    socket.onmessage = message => {
        let received = message.data.split(' '),
            x = received[0],
            y = received[1],
            rotation = received[2]
        let e = viewer.entities.getById(pointId);
        e.position = Cesium.Cartesian3.fromDegrees(x, y);
        viewer.camera.position = Cesium.Cartesian3.fromDegrees(x, y, cameraHeight);
        viewer.camera.rotateRight(rotation);
    };

    socket.onerror = error => {
        console.log('WebSocket connection error');
    };

    socket.onclose = error => {
        console.log('WebSocket server connection closed');  
    };
}