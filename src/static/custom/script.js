function openImageModal(imageUrl) {
  var modal = document.getElementById("imageModal");
  var modalImage = document.getElementById("modalImage");
  modalImage.src = imageUrl;
  modal.style.display = "block";

  // Zoom in effect
  modalImage.addEventListener("click", function () {
    modalImage.classList.toggle("zoomed");
  });
}

// Close the modal when the user clicks on the close button
var closeButton = document.getElementById("closeBtn");
closeButton.onclick = function () {
  var modal = document.getElementById("imageModal");
  var modalImage = document.getElementById("modalImage");
  modalImage.classList.remove("zoomed");
  modal.style.display = "none";
};

