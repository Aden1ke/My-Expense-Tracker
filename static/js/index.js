document.addEventListener("DOMContentLoaded", function(){
	const manualRadio = document.getElementById("manual");
	const fileRadio = document.getElementById("file");
	const manualInputDev = document.getElementById("manualInput");
	const fileInputDev = document.getElementById("fileInput");
	const categorySelect = document.getElementById("category");
	const otherDescriptionLabel = document.getElementById("otherDescriptionLabel");
	const otherDescription = document.getElementById("otherdescription"); // Corrected

	function toggleInput(){
		if(manualRadio.checked) {
			manualInputDev.classList.remove("hide_div");
			fileInputDev.classList.add("hide_div");
		} else if(fileRadio.checked) {
			fileInputDev.classList.remove("hide_div");
			manualInputDev.classList.add("hide_div");
		}
	}

	manualRadio.addEventListener("change", toggleInput);
	fileRadio.addEventListener("change", toggleInput);
	toggleInput();

	function changeCategories() {
		if(categorySelect.value === "others") {
			otherDescriptionLabel.classList.remove("hide_div"); // Show label
			otherDescription.classList.remove("hide_div"); // Show input
		} else {
			otherDescriptionLabel.classList.add("hide_div"); // Hide label
			otherDescription.classList.add("hide_div"); // Hide input
		}
	}

	categorySelect.addEventListener("change", changeCategories);
	changeCategories();


	// Function to show/hide 'Amount' field
	function addAmountToCategories() {
		let categoryFound = false;
		for (let i = 0; i < categorySelect.options.length; i++) {
			if (categorySelect.value === categorySelect.options[i].value) {
				categoryFound = true;
				break;
			}
		}
		if (categoryFound) {
			amountLabel.classList.remove("hide_div");
			amount.classList.remove("hide_div");
		} else {
			amountLabel.classList.add("hide_div");
			amount.classList.add("hide_div");
		}
	}

	categorySelect.addEventListener("change", addAmountToCategories);
	addAmountToCategories();

});

