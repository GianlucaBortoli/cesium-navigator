// global options
const cameraHeight = 300,
    viewerOpts = {
        infoBox: false,
        timeline: false,
        navigationHelpButton: false,
        geocoder: false,
        baseLayerPicker : false,
        homeButton: false,
        fullscreenButton: false,
        animation: false,
        navigationInstructionsInitiallyVisible: false,
        clockViewModel: undefined
    },
    flyToOpts = {
        duration: 0.1
    };
const initialPosition = [-75.166493, 39.9060534, 10],
    pointId = "mypoint";
// viewer
let viewer = new Cesium.Viewer('cesiumContainer', viewerOpts),
    scene = viewer.scene;
// geojson/topojson data source
let diamond = Cesium.GeoJsonDataSource.load('../data/diamond.topojson', {
    stroke: Cesium.Color.RED,
    fill: Cesium.Color.RED,
    strokeWidth: 2
});
viewer.dataSources.add(diamond);
// set fps counter
scene.debugShowFramesPerSecond = true;
// the point moving on the map
let point = {
        id: pointId,
        position : Cesium.Cartesian3.fromDegrees(
            initialPosition[0], initialPosition[1], 0
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
// move viewer to point
viewer.flyTo(point, flyToOpts).then(() => {
    // leave some time to 1st camera positioning
    setTimeout(movePoint(), 3000);
});

/*
* Moves the point on the map according to data received from the websocket
* A message has the following form:
* "<lat> <long> <rotation>"
*/
function movePoint() {
    let port = 9999,
        socket = new WebSocket(`ws://localhost:${port}`);

    socket.onopen = function () {
        // send initial position to server
        socket.send(`${initialPosition[0]} ${initialPosition[1]} ${initialPosition[2]}`);
    };

    socket.onmessage = message => {
        let received = message.data.split(' '),
            x = received[0],
            y = received[1],
            rotation = received[2]
        let e = viewer.entities.getById(pointId);
        e.position = Cesium.Cartesian3.fromDegrees(x, y);
        // move camera towards point
        let center = Cesium.Cartesian3.fromDegrees(x, y);
        viewer.camera.lookAt(
            center,
            new Cesium.Cartesian3(rotation, -100, 100)
        );
    };

    socket.onerror = error => {
        console.log('WebSocket connection error');
    };

    socket.onclose = error => {
        console.log('WebSocket server connection closed');  
    };
}
