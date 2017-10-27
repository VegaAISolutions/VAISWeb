// Get the modal
var modal = document.getElementById('myModal');
var img1 = document.getElementById('myImg1');
var img2 = document.getElementById('myImg2');


// Get the image and insert it inside the modal - use its "alt" text as a caption
var mbutton = document.getElementById('mbutton');
var modalImg = document.getElementById("img01");
var captionText = document.getElementById("caption");
mbutton.onclick = function(){
    modal.style.display = "block";
    modalImg.src = img1.src;
    captionText.innerHTML = this.alt;
}

var rbutton = document.getElementById('rbutton');
rbutton.onclick = function(){
    modal.style.display = "block";
    modalImg.src = img2.src;
    captionText.innerHTML = this.alt;
}

var thumb1 = document.getElementsByClassName('thumb1');
thumb2.onclick = function(){
    modal.style.display = "block";
    modalImg.src = img1.src;
    captionText.innerHTML = this.alt;
}

var thumb2 = document.getElementsByClassName('thumb2');
thumb2.onclick = function(){
    modal.style.display = "block";
    modalImg.src = img2.src;
    captionText.innerHTML = this.alt;
}

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}