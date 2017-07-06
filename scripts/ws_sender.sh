#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

start() {
    $DIR/../node_modules/.bin/pm2 start $DIR/../ws_sender.js
}

stop() {
    $DIR/../node_modules/.bin/pm2 stop $DIR/../ws_sender.js
    $DIR/../node_modules/.bin/pm2 delete $DIR/../ws_sender.js
}

status() {
    $DIR/../node_modules/.bin/pm2 show ws_sender
}

# main
case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        stop
        start
        ;;
    status)
        status
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
esac

exit 0
