"use strict";
const aSliderLabel = document.querySelector("#slider-label")
const slider = document.querySelector("#slider")
aSliderLabel.textContent = slider.value

slider.addEventListener("input", (event) => {
	aSliderLabel.textContent = event.target.value
})