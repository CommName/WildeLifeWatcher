
const address = document.getElementById("serverAddress").value


var ws = new WebSocket('ws://' + address+ '/ws');

function addSensor(sensor) {
  var scrollbar = document.getElementById("sensorSelector");
  var option = document.createElement("option");
  option.text = sensor.Name;
  option.value = sensor.Name;
  scrollbar.add(option);
}

function setSensorInfo(sensors){
  var sensorName = document.getElementById("sensorSelector").value
  for (index = 0; index < sensors.length; index++ ){
    if (sensors[index].Name = sensorName){
      document.getElementById("sensorInfo").innerHTML = "Sensor name: " + sensorName + "<br /> N: " + sensors[index].N + "<br /> E: " + sensors[index].E
    }
  }
  console.log("change")
  ws.send("sensor "+sensorName)
}



 $(document).ready(function() {

        fetch("http://"+address+'/sensors')
            .then(response => {
                return response.json();
            })
            .then (data => {
                if (Array.isArray(data) && data.length){
                    Sensors = data;
                    data.forEach(addSensor);
                    document.getElementById("sensorSelector").onchange = function(){setSensorInfo(data); };
                }
                else {
                    document.getElementById("sensorSelector").disabled = true;
                }

            });
        });



        window.onbeforeunload = function(e) {

            ws.close();

            if(!e) e = window.event;
            e.stopPropagation();
            e.preventDefault();
          };

        ws.onmessage = function (evt) {
            data = JSON.parse(evt.data)
            document.getElementById("sensorImage").src = "data:image/jpeg;base64,"+data["image"];
          };


