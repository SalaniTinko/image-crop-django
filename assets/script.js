var canvas = $("#canvas"),
  context = canvas.get(0).getContext("2d"),
  $result = $("#result");

$("#fileInput").on("change", function () {
  if (this.files && this.files[0]) {
    if (this.files[0].type.match(/^image\//)) {
      $("#btnCrop").removeClass("hidden"); //Here classes are removed or added to display or hide them
      $(".cv").removeClass("hidden");
      $(".custom-file-upload").addClass("hidden");
      $("#submitBtn").addClass("hidden");
      var reader = new FileReader();
      reader.onload = function (evt) {
        var img = new Image();
        img.onload = function () {
          context.canvas.height = img.height;
          context.canvas.width = img.width;
          context.drawImage(img, 0, 0);
          var cropper = canvas.cropper({}); //Initialize the cropper
          $("#btnCrop").click(function () {
            var croppedImageDataURL = canvas
              .cropper("getCroppedCanvas")
              .toDataURL("image/png");
            $result.append($("<img>").attr("src", croppedImageDataURL));
            $result.append($("<input type='text' name='img_data' hidden>").attr("value", croppedImageDataURL));
            $result.append($('<div><input type="submit" value="Save Image" id="submitBtn"></div>'))

            $("#submitBtn").css("display","none");
            $(".paybtn").show();
          });
        };
        img.src = evt.target.result;
      };
      reader.readAsDataURL(this.files[0]);
    } else {
      alert("Invalid file type! Please select an image file.");
    }
  } else {
    alert("No file(s) selected.");document.getElementsByClassName("button2 redColor")[0].click();
  }
});

$("#btnCrop").click(function(){
  $(".cv").addClass("hidden");


})
