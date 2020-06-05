
address = document.getElementById("serverAddress").value



 $(document).ready(function() {
          var ws = new WebSocket(address);

          window.onbeforeunload = function(e) {

            ws.close(1000, "%(username)s left the room");

            if(!e) e = window.event;
            e.stopPropagation();
            e.preventDefault();
          };

          ws.onmessage = function (evt) {
            data = JSON.parse(evt.data)
            console.log(data)
            document.getElementById("sensorImage").src = "data:image/jpeg;base64,"+data["image"];
          };

          ws.onopen = function() {
             ws.send("sensor 40.0 40.0");
          };

          ws.onclose = function(evt) {
             ws.send("disconnect 40.0 40.0")
          };


        });