/**
 * Runs when user click the 'Get data' button.
 * Sends a request to server and receives JSON data.
 */
// eslint-disable-next-line no-unused-vars
function execute() {
    clearHTMLElements("output-container");
    const url = "http://127.0.0.1:5000/";

    fetch(url)
        .then(response => {
            const responseStatus = response.status;
            const responseStatusWithText = responseStatus + " " + response.statusText;
            if (responseStatus !== 200) {                
                document.getElementById("error-messages").style.color = "red";
                document.getElementById("error-messages").innerHTML = responseStatusWithText;
                return;
            }
            response.json().then(data => {                
                jsonToUi(data, "monthly");
            });
        })
        .catch(error => {
            document.getElementById("error-messages").style.color = "red";
            document.getElementById("error-messages").innerHTML = error;
        });
}

/**
 * Prints the given data to UI as an HTML table.
 * @param {array} data Given data.
 * @param {string} granularity Granularity of data (monthly, weekly etc.).
 */
 function jsonToUi(data, granularity) {
    const selectElement = document.getElementById("output-electricity-consumption");
    const header = document.createElement("h3");    
    header.className = "output-header";
    header.innerHTML = capitalizeFirstLetter(granularity);
    const table = document.createElement("table");
    table.className = "output-table-" + granularity.toLowerCase();

    for (let i = 0; i < data.length; i++) {
        let line = data[i];
        let lines = line.split(",");
        const row = lines;
        table.insertRow(i);

        for (let j = 0; j < row.length; j++) {
            const cell = lines[j];
            const newCell = table.rows[table.rows.length - 1].insertCell(j);
            newCell.textContent = cell;
        }
    }

    selectElement.appendChild(header);
    selectElement.appendChild(table);
}

/**
 * Puts first letter of given word to upper case.
 * @param {string} word Given word.
 * @returns Given word with capitalized first letter.
 */
 function capitalizeFirstLetter(word) {
    word = word.toLowerCase();
    return word.charAt(0).toUpperCase() + word.slice(1);
}

/**
 * Clears HTML elements that have the given class.
 * @param {string} HTMLClass Given class.
 */
 function clearHTMLElements(HTMLClass) {
    const elements = document.getElementsByClassName(HTMLClass);

    for (let i = 0; i < elements.length; i++) {
        let element = elements[i];
        element.innerHTML = "";
    }
}