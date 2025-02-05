document.addEventListener("DOMContentLoaded", function(){
	const manualRadio = document.getElementById("manual");
	const fileRadio = document.getElementById("file");
	const manualInputDev = document.getElementById("manualInput");
	const fileInputDev = document.getElementById("fileInput");
	const categorySelect = document.getElementById("category");
	const otherDescriptionLabel = document.getElementById("otherDescriptionLabel");
	const otherDescription = document.getElementById("otherdescription");
	const newCategoryHidden = document.getElementById("newCategoryHidden");
            const expenseForm = document.getElementById("expenseForm");

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
			newCategoryHidden.value = "";
		}
	}

	categorySelect.addEventListener("change", changeCategories);
	changeCategories();


	// function to add to category selection
	function addCategory() {
		if(categorySelect.value === "others") {
			const newCategory = otherDescription.value.trim();
			if (newCategory !== "") {
				const option = document.createElement("option");
				option.value = newCategory.toLowerCase();
				option.textContent = newCategory;
				categorySelect.appendChild(option);
				categorySelect.value = newCategory.toLowerCase();
				newCategoryHidden.value = newCategory;
				otherDescription.value = "";
			}
		}
	}

	// Trigger adding the category when the user presses "Enter" or leaves the input field
	otherDescription.addEventListener("keypress", function(event) {
		if (event.key === "Enter") {
			event.preventDefault(); // Prevent form submission
			addCategory();
		}
	});
	otherDescription.addEventListener("blur", addCategory);

	// Ensure new category is saved before form submission
	expenseForm.addEventListener("submit", function () {
		if (categorySelect.value === "others") {
			newCategoryHidden.value = otherDescription.value.trim();
		}
	});


});

