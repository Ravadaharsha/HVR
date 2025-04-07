document.getElementById("category-form").addEventListener("submit", function (event) {
    event.preventDefault();

    const category = document.getElementById("category").value;
    const seat_type = document.getElementById("seat_type").value;
    const quota = document.getElementById("quota").value;
    const gender = document.getElementById("gender").value;
    const category_rank = document.getElementById("category_rank").value;
    let queryType = document.getElementById("query-type").value; // Extract query type
    
    fetch(`/get_suggested_colleges?type=${queryType}&category=${category}&seat_type=${seat_type}&quota=${quota}&gender=${gender}&category_rank=${category_rank}`)
        .then(response => response.json())
        .then(data => {
            const resultsList = document.getElementById("college-results");
            resultsList.innerHTML = "";

            if (data.message) {
                resultsList.innerHTML = `<li>${data.message}</li>`;
            } else {
                data.forEach(college => {
                    const listItem = document.createElement("li");
                    listItem.innerHTML = `
                        <strong>College:</strong> ${college.college_name} <br>
                        <strong>Branch:</strong> ${college.academic_program_name} <br>
                        <strong>Closing Rank:</strong> ${college.closing_rank}<br>
                        <strong>Seat_type:</strong> ${college.seat_type}
                        <hr>
                    `;
                    resultsList.appendChild(listItem);
                });
            }
        })
        .catch(error => console.error("Error:", error));
});
