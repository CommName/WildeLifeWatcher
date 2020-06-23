const subDiv =  document.getElementById("subscribtion")
const address = document.getElementById("serverAddress").value

var ws = new WebSocket('ws://' + wsaddress+ '/ws');

const allAnimals = JSON.parse(document.getElementById("animalList").value);
const subedAnimlas = JSON.parse(document.getElementById("activeSubscribtions").value);


function subscribtion(animal) {
    console.log(animal.checked)
    if (animal.checked){
        ws.send("animal "+animal.value);
    }
    else {
        console.log("unsub")
        ws.send("unsub animal "+animal.value);
    }

}

function addAnimalCheckBox(animal) {
    var lab = document.createElement("LABEL");
    lab.for = animal;
    lab.innerHTML = animal;
    subDiv.appendChild(lab);

    var x = document.createElement("INPUT");
    x.setAttribute("type", "checkbox");
    var subscribed = subedAnimlas.includes(animal);
    x.value = animal;
    x.checked = subscribed;
    x.onclick = function() { subscribtion(x)};

    subDiv.appendChild(x);
    var br = document.createElement("BR");
    subDiv.appendChild(br);
}
$(document).ready(function() {


        window.onbeforeunload = function(e) {

            ws.close();

            if(!e) e = window.event;
            e.stopPropagation();
            e.preventDefault();
          };

        allAnimals.forEach(animal => addAnimalCheckBox(animal));
});