let initialPosition = [-75.166493, 39.9060534, 0];
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
}
let viewer = new Cesium.Viewer('cesiumContainer', viewerOpts);
let pointId = "mypoint";
let point = {
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

viewer.camera.flyTo({
    destination : Cesium.Cartesian3.fromDegrees(
        initialPosition[0], initialPosition[1], initialPosition[2] + 100
    )
});

viewer.entities.add(point);
viewer.flyTo(point, flyToOpts).then(() => {
    setTimeout(() => {
        movePoint()
    }, 3000);
});

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
        //viewer.flyTo(e, flyToOpts);
        viewer.zoomTo(e);
        viewer.camera.rotateRight(rotation);
    };

    socket.onerror = error => {
        console.log('WebSocket connection error');
    };

    socket.onclose = error => {
        console.log('WebSocket server connection closed');  
    };
}