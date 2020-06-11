const address = document.getElementById("serverAddress").value
const imageDiv =  document.getElementById("ImageGallery")
var numberOfPicturseShown = 0
var pictureData = []


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
            var image = new Image()
            console.log( pictureData[index])
            image.src = '/images/'+ pictureData[index].id
            newImageDiv.className  = "GalleryImage"
            newImageDiv.appendChild(image)
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
      console.log(string)
      newImageData = JSON.parse(string)
      pictureData = pictureData.concat(newImageData)

      return false;

  }
  } );