const address = document.getElementById("serverAddress").value
const imageDiv =  document.getElementById("ImageGallery")
var numberOfPicturseShown = 0
var pictureData = []


function addAnimalOption(animal) {
    var x = document.createElement("OPTION");
    x.setAttribute("value", animal);
    var t = document.createTextNode(animal);
    x.appendChild(t);
    document.getElementById("animalName").appendChild(x);
}
const allAnimals = JSON.parse(document.getElementById("animalList").value);
allAnimals.forEach(animal => addAnimalOption(animal));


const queuingStrategy = new ByteLengthQueuingStrategy({ highWaterMark: 1 });
var size = queuingStrategy.size(250);

let reader;

var url = "http://"+address+'/galleryData/GetImages';


if(document.getElementById("search").value == "dataSearch"){
    url = "http://"+address+'/galleryData/dataSearch?' + $.param({
    coordinateN: document.getElementById("N").value,
    coordinateE: document.getElementById("E").value,
    startTime: document.getElementById("sTime").value,
    endTime: document.getElementById("eTime").value,
    });
}

if(document.getElementById("search").value == "infomrationSearch"){
    url = "http://"+address+'/galleryData/informationSearch?' + $.param({
    animalName: document.getElementById("aName").value,
    feeding: document.getElementById("feeding").value,
    notfeeding: document.getElementById("notfeeding").value
    });
}



fetch(url).then(response => {
    const reader = response.body.getReader();
    $(window).scroll(async function() {
        if($(window).scrollTop() + $(window).height() > $(document).height()- 100) {
            await loadMoreImages()
        }
    });
    loadMoreImages()
   async function loadMoreImages(){

        while(pictureData.length < numberOfPicturseShown+10 ) {
        done = await pump()
         if(done)
            break;
        }

        for(index = numberOfPicturseShown; index < numberOfPicturseShown+10; index++){
            var newImageDiv = document.createElement("div")
            var link = document.createElement("a")
            var image = new Image()
            var imageName =  ""
            if (document.getElementById("search").value == "infomrationSearch"){
                imageName =  pictureData[index].imageName
            }
            else {
                imageName = pictureData[index].id
            }
            link.href ="/ImageDescription?" + $.param({imageName:imageName});
            image.src = '/images/'+ imageName
            newImageDiv.className  = "GalleryImage"
            link.appendChild(image)
            newImageDiv.appendChild(link)
            imageDiv.appendChild(newImageDiv)
        }
        numberOfPicturseShown += 10;

    };


    async function pump() {
    response =  await reader.read(1024);

      // When no more data needs to be consumed, close the stream
      if (response.done) {
        console.log("Done")
          return true;
      }
        // Enqueue the next data chunk into our target stream
      string = "["
      for (index =0 ; index<response.value.length; index++){
        string +=  String.fromCharCode(response.value[index])
      }
      string += "]"
      string = string.split("}{").join("} ,{ ");
      newImageData = JSON.parse(string)
      pictureData = pictureData.concat(newImageData)

      return false;

  }
  } );