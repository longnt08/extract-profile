document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("entityForm").addEventListener("submit", async function(e) {
        e.preventDefault();

        // get data from form
        const form = e.target;
        const url = form.url.value;
        let fields = Array.from(form.querySelectorAll('input[name="fields"]:checked')).map(input => input.value);
        if(fields.includes("all")) {
            fields = ["name", "email", "phone", "address", "age", "profession", "organization"];
        }

        if(!url || fields.length === 0) {
            alert("Please enter URL and at least one field.");
            return;
        } 

        // create query string
        const params = new URLSearchParams();
        params.append("url", url);
        fields.forEach(f => params.append("fields", f));
        const queryString = params.toString();

        // send request by Fetch API
        try {
            const response = await fetch(`http://127.0.0.1:8000/entityExtraction?${queryString}`, {
                method: "GET",
            });

            const res = await response.json();
            const resultData = JSON.parse(res);

            if(response.ok) {
                console.log(resultData);
                const resultToDisplay = document.getElementById("result");
                resultToDisplay.innerHTML = "";
                
                fields.forEach(field => {
                    console.log(field);
                    let fieldText = document.createElement('p');
                    fieldText.innerHTML = `${field}: ${resultData[field] ?? "(Không có dữ liệu)"}`;
                    resultToDisplay.appendChild(fieldText);
                });
            } else {
                alert(`Error: ${resultData.message}`);
            }
        } catch(error) {
            console.error("An error occurred:", error);
            alert("An error occurred. Check your code.");
        }

    });
});