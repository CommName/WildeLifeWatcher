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
    var checkBoxDiv = document.createElement("DIV")
    checkBoxDiv.className = "ck-button";


    var x = document.createElement("INPUT");
    x.setAttribute("type", "checkbox");
    var subscribed = subedAnimlas.includes(animal);
    x.value = animal;
    x.checked = subscribed;
    x.onclick = function() { subscribtion(x)};

    checkBoxDiv.appendChild(x);

    var lab = document.createElement("SPAN");
    lab.for = animal;
    lab.innerHTML = animal;
    checkBoxDiv.appendChild(lab);
    
    subDiv.appendChild(checkBoxDiv);
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