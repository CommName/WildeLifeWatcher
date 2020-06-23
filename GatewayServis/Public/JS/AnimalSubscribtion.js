const wsaddress = document.getElementById("serverAddress").value
var ws = new WebSocket('ws://' + wsaddress+ '/ws');


 $(document).ready(function() {

        console.log(document.cookie)
        window.onbeforeunload = function(e) {

            ws.close();

            if(!e) e = window.event;
            e.stopPropagation();
            e.preventDefault();
          };

        ws.onopen = function() {
            ws.send("subscribe animals")
        }

        ws.onmessage = function (evt) {
            data = JSON.parse(evt.data)

        if (data["Type"] != "New animal"){
            return;
        }

		window.createNotification({
			closeOnClick: false,
			displayCloseButton: true,
			positionClass: "nfc-top-right",
			showDuration: 3500,
			theme: "info",
			onclick: function(){ window.open("/ImageDescription?" + $.param({imageName: data["image"] }))}

		})({
			title: data["animal"],
			message: "New images of " + data["animal"]
		});



         };

  });