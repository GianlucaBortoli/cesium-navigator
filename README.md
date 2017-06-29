# cesium-navigator
WebGL navigator using the Cesium framework

### How to start
First start the Cesium local development HTTP server
```{r, engine='bash', code_block_name}
node server.js
```

Then start the WebSocket server which simulates position & rotation
```{r, engine='bash', code_block_name}
node ws_sender.js [interval in ms; default is 200]
```

After that, go to `http://localhost:8080/app/navigator.html`

### TODO
* setup local terrain server
