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
            const response = await fetch(`http://127.0.0.1:8000/experts/search?${queryString}`, {
                method: "GET",
            });

            const res = await response.json();

            const textRes = document.createElement("h3");
            const resultToDisplay = document.getElementById("result");

            textRes.innerText = "Kết quả";
            resultToDisplay.innerHTML = "";
            resultToDisplay.appendChild(textRes);

                // them css
                resultToDisplay.setAttribute(
                    "style",
                    "background-color: white; width: 320px; height: 300px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); border-radius: 8px; padding: 10px 20px;"
                );

            if(response.ok) {
                console.log(res);

                fields.forEach(field => {
                    console.log(field);
                    let fieldText = document.createElement('p');
                    fieldText.innerHTML = `${field}: ${res[field] ?? "(Không có dữ liệu)"}`;
                    resultToDisplay.appendChild(fieldText);
                });
            } else {
                resultToDisplay.innerText = res.message;
            }

        } catch(error) {
            console.error("An error occurred:", error);
            alert("An error occurred. Check your code.");
        }

    });
});