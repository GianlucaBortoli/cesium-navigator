# cesium-navigator
WebGL navigator using the Cesium framework

### Initial setup
Install NodeJS & NPM. After that, install the dependencies running
```{r, engine='bash', code_block_name}
npm install
```
Install the python2 requirements for the analysis scripts using `pip` running
```{r, engine='bash', code_block_name}
pip install -r requirements.txt
```
The python requirements are **not** necessary to run the navigator app.

### How to run it
First start the Cesium local development HTTP server
```{r, engine='bash', code_block_name}
node server.js
```

Then start the WebSocket server which simulates position & rotation
```{r, engine='bash', code_block_name}
node ws_sender.js [interval in ms; default is 500]
```

or using
```{r, engine='bash', code_block_name}
./scripts/ws_sender.sh
```

After that, go to `http://localhost:8080/app/navigator.html`

### Keyboard bindings
* _w/up arrow_: move camera forward
* _a/left arrow_: move camera left
* _s/down arrow_: move camera backward
* _d/right arrow_: move camera right
* _q_: move camera up
* _e_: move camera down
* _\+ (add)_: zoom in
* _\- (sub)_: zoom out
