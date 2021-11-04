document.getElementById('button').addEventListener("click", function() {
	document.querySelector('.bg-modal').style.display = "flex";
});

document.querySelector('.close').addEventListener("click", function() {
	document.querySelector('.bg-modal').style.display = "none";
});
document.getElementById('button1').addEventListener("click", function() {
	document.querySelector('.bg-modal1').style.display = "flex";
});
document.getElementById('button2').addEventListener("click", function() {
	document.querySelector('.bg-modal2').style.display = "flex";
});

document.querySelector('.close1').addEventListener("click", function() {
	document.querySelector('.bg-modal1').style.display = "none";
});
document.querySelector('.close2').addEventListener("click", function() {
	document.querySelector('.bg-modal2').style.display = "none";
});


