# cesium-navigator
WebGL navigator using the Cesium framework

### Initial setup
Install NodeJS & NPM. After that, install the dependencies running
```{r, engine='bash', code_block_name}
npm install
```

### How to run it
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
