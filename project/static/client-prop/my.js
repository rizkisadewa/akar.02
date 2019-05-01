/*
  CLIENT INDEX
*/

// smooth link scoller

(function() {
	scrollTo();
})();

function scrollTo() {
	const links = document.querySelectorAll('.scroll');
	links.forEach(each => (each.onclick = scrollAnchors));
}

function scrollAnchors(e, respond = null) {
	const distanceToTop = el => Math.floor(el.getBoundingClientRect().top);
	e.preventDefault();
	var targetID = (respond) ? respond.getAttribute('href') : this.getAttribute('href');
	const targetAnchor = document.querySelector(targetID);
	if (!targetAnchor) return;
	const originalTop = distanceToTop(targetAnchor);
	window.scrollBy({ top: originalTop, left: 0, behavior: 'smooth' });
	const checkIfDone = setInterval(function() {
		const atBottom = window.innerHeight + window.pageYOffset >= document.body.offsetHeight - 2;
		if (distanceToTop(targetAnchor) === 0 || atBottom) {
			targetAnchor.tabIndex = '-1';
			targetAnchor.focus();
			window.history.pushState('', '', targetID);
			clearInterval(checkIfDone);
		}
	}, 100);
}


// on load on the top scroll
window.addEventListener('load', function() {
    console.log('All assets are loaded')
		scrollTo({
			top: 0,
			left: 0,
		});
})

/*
  /CLIENT INDEX
*/


/*
  SERVICE DETAILS
*/

// Image Slider

let sliderImages = document.querySelectorAll('.slide'),
    arrowLeft = document.querySelector('#arrow-left'),
    arrowRight = document.querySelector('#arrow-right'),
    current = 0;


// Clear all images
function reset(){
  for(let i=0; i<sliderImages.length; i++){
    sliderImages[i].style.display = 'none';
  }
}

// Initialize the slider
function startSlide(){
  reset();
  sliderImages[0].style.display = 'block';
}


// Show the prev
function slideLeft(){
  reset();
  sliderImages[current - 1].style.display = 'block';
  current--;
}

// Show the next
function slideRight(){
  reset();
  sliderImages[current + 1].style.display = 'block';
  current++;
}

// Left arrow click
arrowLeft.addEventListener('click', function(){
  if(current === 0){
    current = sliderImages.length; // then will be set up the number of equal to sliderImages.length
  }
  slideLeft();
});

// Right arrow click
arrowRight.addEventListener('click', function(){
  if(current === sliderImages.length - 1){
    current = -1; // then will be set up to zero after slideRight()
  }
  slideRight();
});

startSlide(); // execute

/*
  SERVICE DETAILS
*/
