// Get the modal
var modal = document.getElementById('myModal');

var mbutton = document.getElementById('mbutton');

var mbutton = document.getElementById('rbutton');

// Get the image and insert it inside the modal - use its "alt" text as a caption
var img = document.getElementById('myImg');
var modalImg = document.getElementById("img01");
var captionText = document.getElementById("caption");
mbutton.onclick = function(){
    modal.style.display = "block";
    modalImg.src = img.src;
    captionText.innerHTML = this.alt;
};

var img2 = document.getElementById('myImg2');
rbutton.onclick = function(){
    modal.style.display = "block";
    modalImg.src = img2.src;
    captionText.innerHTML = this.alt;
};


// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
};