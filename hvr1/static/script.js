document.getElementById("jee-form").addEventListener("submit", function (event) {
    event.preventDefault();  // Prevent form submission from reloading page

    let college = document.getElementById("college").value;
    let seatType = document.getElementById("seat_type").value;
    let quota = document.getElementById("quota").value;
    let gender = document.getElementById("gender").value;
    let categoryRank = document.getElementById("category_rank").value;
    let queryType = document.getElementById("query-type").value; // Extract query type
    
    let apiUrl = `/get_branches?type=${queryType}&college=${encodeURIComponent(college)}&seat_type=${encodeURIComponent(seatType)}&quota=${encodeURIComponent(quota)}&gender=${encodeURIComponent(gender)}&category_rank=${encodeURIComponent(categoryRank)}`;

    console.log("Calling API:", apiUrl);  // Debugging

    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            console.log("API Response:", data);  // Debugging
            let resultDiv = document.getElementById("branch-results");
            resultDiv.innerHTML = "";

            if (data.message) {
                resultDiv.innerHTML = `<p>${data.message}</p>`;
            } else {
                if (data.length === 0) {
                    console.log("API Response:");
                    resultDiv.innerHTML = "<p>No branches available for this rank.</p>";
                } else {
                    // If there are branches, loop through them and display
                    data.forEach(branch => {
                        let li = document.createElement("li");
                        li.textContent = branch.academic_program_name;
                        resultDiv.appendChild(li);
                    });
                }
            }
        })
        .catch(error => console.error("Error:", error));
});


// document.getElementById("jee-form").addEventListener("submit", function(event) {
//     event.preventDefault();

//     const college = document.getElementById("college").value;
//     const seatType = document.getElementById("seat_type").value;
//     const quota = document.getElementById("quota").value;
//     const gender = document.getElementById("gender").value;
//     const categoryRank = document.getElementById("category_rank").value;
//     const queryType = document.getElementById("query-type").value; // Extract query type

//     fetch(`/fetch_branches?type=${queryType}`, {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ college, seatType, quota, gender, categoryRank })
//     })
//     .then(response => response.json())
//     .then(data => {
//         const resultsList = document.getElementById("branch-results");
//         resultsList.innerHTML = ""; // Clear previous results

//         data.branches.forEach(branch => {
//             const li = document.createElement("li");
//             li.textContent = branch;
//             resultsList.appendChild(li);
//         });
//     })
//     .catch(error => console.error("Error:", error));
// });


const collegeInput = document.getElementById("college");
const suggestionsBox = document.getElementById("suggestions");

// Fetch college suggestions dynamically
collegeInput.addEventListener("input", function () {
    const inputText = this.value.trim();

    if (inputText.length === 0) {
        suggestionsBox.innerHTML = "";
        return;
    }

    fetch(`/getting_colleges?query=${encodeURIComponent(inputText)}`)
        .then(response => response.json())
        .then(data => {
            suggestionsBox.innerHTML = "";
            if (data.length === 0) {
                return;
            }

            data.forEach(college => {
                const suggestionItem = document.createElement("div");
                suggestionItem.textContent = college;
                suggestionItem.classList.add("suggestion-item");

                suggestionItem.addEventListener("click", function () {
                    collegeInput.value = college;
                    suggestionsBox.innerHTML = ""; // Hide suggestions
                });

                suggestionsBox.appendChild(suggestionItem);
            });
        })
        .catch(error => console.error("Error fetching college suggestions:", error));
});

// Hide suggestions when clicking outside
document.addEventListener("click", function (e) {
    if (!collegeInput.contains(e.target) && !suggestionsBox.contains(e.target)) {
        suggestionsBox.innerHTML = "";
    }
});

