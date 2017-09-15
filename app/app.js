/*
* WEB TRACING FRAMEWORK
*/
var options = {
    'wtf.trace.provider.webgl': true,
    'wtf.trace.provider.webgl.recordAtStartup': true,
    'wtf.trace.provider.webgl.replayable': true,
    'wtf.trace.provider.webgl.embedRemoteImages': false,
    'wtf.trace.provider.webworker': true,
    'wtf.trace.provider.webworker.inject': true
};
wtf.trace.prepare(options);

/*
* CESIUM APPLICATION
*/
// move map from keyboard
addKeyboardShortcuts();
// global options
const cameraHeight = 500,
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
        clockViewModel: undefined,
        // remove sky background
        skyBox: new Cesium.SkyBox({}),
        skyAtmosphere: new Cesium.SkyAtmosphere(),
        // blank terrain
        // terrainProvider: new Cesium.CesiumTerrainProvider({})
    },
    flyToOpts = {
        duration: 0.1
    };
let tile3d = null;
// initial point position & id
const initialPosition = [-74.00303453207016, 40.71505038395303, 10],
    pointId = "mypoint";
// reset view goes to initial position
const commandOpts = {};
commandOpts.defaultResetView = new Cesium.Cartographic.fromDegrees(
    initialPosition[0],
    initialPosition[1],
    cameraHeight
);
commandOpts.enableDistanceLegend = false;
// viewer
let viewer = new Cesium.Viewer('cesiumContainer', viewerOpts),
    scene = viewer.scene;
// extend view with camera & zoom controls
viewer.extend(Cesium.viewerCesiumNavigationMixin, commandOpts);
// geojson/topojson data source
/*let diamond = Cesium.GeoJsonDataSource.load('../data/diamond.topojson', {
    stroke: Cesium.Color.RED,
    fill: Cesium.Color.RED,
    strokeWidth: 2
});
viewer.dataSources.add(diamond);*/
// show fps counter
scene.debugShowFramesPerSecond = true;
// the person moving on the map
let person = {
        id: pointId,
        position : Cesium.Cartesian3.fromDegrees(initialPosition[0], initialPosition[1], 0),
        cylinder : {
            length : 15,
            topRadius : 10,
            bottomRadius : 10,
            material : 'images/man.jpg',
            fill: true
        }
};
// red dot moving on the map
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
// fake point not really rendered but used to move the camera
let fakePoint = {
        id: pointId,
        position : Cesium.Cartesian3.fromDegrees(
            initialPosition[0], initialPosition[1], 0
        )
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
        // start profiling
        wtf.trace.start();
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
            new Cesium.Cartesian3(rotation, -cameraHeight, cameraHeight)
        );
    };

    socket.onerror = error => {
        console.log('WebSocket connection error');
    };

    socket.onclose = error => {
        wtf.trace.snapshot('file://trace')
        wtf.trace.stop();
        console.log('WebSocket server connection closed');
    };
}

/*
* Kyboard shortcuts
*/
function addKeyboardShortcuts() {
    const zoomAmount = 15,
        rotateAmount = 5;
    document.addEventListener('keydown', e => {
        // 87 -> W
        // 65 -> A
        // 83 -> S
        // 68 -> D
        // 38 -> up
        // 37 -> left
        // 40 -> down
        // 39 -> right
        // 81 -> Q
        // 69 -> E
        // 107 -> + (add)
        // 109 -> - (sub)
        switch(e.keyCode) {
            case 87:
            case 38:
                viewer.camera.moveForward(rotateAmount);
                break;
            case 81:
                viewer.camera.moveUp(rotateAmount);
                break;
            case 69:
                viewer.camera.moveDown(rotateAmount);
                break;
            case 65:
            case 37:
                viewer.camera.moveLeft(rotateAmount);
                break;
            case 83:
            case 40:
                viewer.camera.moveBackward(rotateAmount);
                break;
            case 68:
            case 39:
                viewer.camera.moveRight(rotateAmount);
                break;
            case 107:
                viewer.camera.zoomIn(zoomAmount);
                break;
            case 109:
                viewer.camera.zoomOut(zoomAmount);
                break;
        }
    });
}

function handle3d(checkbox) {
    if (checkbox.checked) {
        add3dTiles();
    } else {
        removeAllTiles();
    }
}

function add3dTiles() {
    tile3d = new Cesium.Cesium3DTileset({
        url: 'https://beta.cesium.com/api/assets/1461?access_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJkYWJmM2MzNS02OWM5LTQ3OWItYjEyYS0xZmNlODM5ZDNkMTYiLCJpZCI6NDQsImFzc2V0cyI6WzE0NjFdLCJpYXQiOjE0OTkyNjQ3NDN9.vuR75SqPDKcggvUrG_vpx0Av02jdiAxnnB1fNf-9f7s'
    });
    viewer.scene.primitives.add(tile3d);
}

function removeAllTiles() {
    tile3d.destroy();
}