const address = document.getElementById("serverAddress").value
const imageName =  document.getElementById("imageName").value

fetch("http://"+address+'/galleryData/GetImageDetails?'+$.param({imageName : imageName}))
            .then(response => {
                return response.json();
            })
            .then (data => {
                for(index =0; index<data.length; index++){
                    for(var key in data[index]){
                    document.getElementById("imageDescription").innerHTML += key+": "+data[index][key] + "<br>"
                    }
                    document.getElementById("imageDescription").innerHTML += "<br>"
                }
            });
