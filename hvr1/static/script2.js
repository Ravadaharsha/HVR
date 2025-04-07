const branchInput = document.getElementById("branch");
const branchSuggestionsBox = document.getElementById("branch-suggestions");

branchInput.addEventListener("input", function () {
    const inputText = this.value.trim();

    if (inputText.length === 0) {
        branchSuggestionsBox.innerHTML = "";
        return;
    }

    fetch(`/getting_branches?query=${encodeURIComponent(inputText)}`)
        .then(response => response.json())
        .then(data => {
            branchSuggestionsBox.innerHTML = "";
            if (data.length === 0) {
                return;
            }

            data.forEach(branch => {
                const suggestionItem = document.createElement("div");
                suggestionItem.textContent = branch;
                suggestionItem.classList.add("suggestion-item");

                suggestionItem.addEventListener("click", function () {
                    branchInput.value = branch;
                    branchSuggestionsBox.innerHTML = ""; // Hide suggestions
                });

                branchSuggestionsBox.appendChild(suggestionItem);
            });
        })
        .catch(error => console.error("Error fetching branch suggestions:", error));
});

// Hide suggestions when clicking outside
document.addEventListener("click", function (e) {
    if (!branchInput.contains(e.target) && !branchSuggestionsBox.contains(e.target)) {
        branchSuggestionsBox.innerHTML = "";
    }
});

document.getElementById("branch-form").addEventListener("submit", function (event) {
    event.preventDefault();

    const branch = document.getElementById("branch").value;
    const seatType = document.getElementById("seat_type").value;
    const quota = document.getElementById("quota").value;
    const gender = document.getElementById("gender").value;
    const categoryRank = document.getElementById("category_rank").value;
    let queryType = document.getElementById("query-type").value; // Extract query type

    fetch(`/get_colleges_by_branch?type=${queryType}&branch=${encodeURIComponent(branch)}&seat_type=${seatType}&quota=${quota}&gender=${gender}&category_rank=${categoryRank}`)
        .then(response => response.json())
        .then(data => {
            const resultsContainer = document.getElementById("college-results");
            resultsContainer.innerHTML = "";

            if (data.message) {
                resultsContainer.innerHTML = `<li>${data.message}</li>`;
                return;
            }
            
            data.forEach(college => {
                const listItem = document.createElement("li");
                listItem.textContent = college.college_name;
                resultsContainer.appendChild(listItem);
            });
        })
        .catch(error => console.error("Error fetching college data:", error));
});
