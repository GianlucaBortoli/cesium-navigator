let initialPosition = [-75.166493, 39.9060534];
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
let point = {
    id: "mypoint",
    position : Cesium.Cartesian3.fromDegrees(initialPosition[0], initialPosition[1]),
    point : {
        pixelSize : 5,
        color : Cesium.Color.RED,
        outlineColor : Cesium.Color.WHITE,
        outlineWidth : 2
    }
};
viewer.entities.add(point)
viewer.flyTo(point, flyToOpts).then(() => {
    setTimeout(() => {
        movePoint()
    }, 3000);
});

function movePoint() {
    let socket = new WebSocket("ws://localhost:9999")
    socket.onopen = function () {
        socket.send('client connected');
    };

    socket.onmessage = message => {
        let position = message.data.split(' '),
            x = position[0],
            y = position[1]
        let e = viewer.entities.getById("mypoint");
        e.position = Cesium.Cartesian3.fromDegrees(position[0], position[1])
        viewer.flyTo(e, flyToOpts);
    };

    socket.onerror = error => {
        console.log('WebSocket connection error');
    };

    socket.onclose = error => {
        console.log('WebSocket server connection closed');  
    };
}