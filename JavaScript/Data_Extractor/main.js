const input = document.getElementById('rawText');
const extracted = document.getElementById('extracted');
input.addEventListener('input', checkInput);

/* 
    This function holds a list of regex patterns then checks the input 
    value against all of them until it finds a match or not
*/
function checkInput() {
    let val = input.value;

    // /g tells to find all occurrances rather than juse one
    const patterns = {
        email: /(?<=^|\s)(\w+@\w+(\.[a-z]{2,})+)(?=$|\s)/gi,
        zip: /(?<=^|\s)\d{5}(?=$|\s)/g,
        date: /(?<=^|\s)(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z?)(?=$|\s)/g,
        ip: /(?<=^|\s)(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9])(?=$|\s)/g,
        color: /(?<=^|\s)(#([a-f0-9]{3,4}|[a-f0-9]{6}|[a-f0-9]{8}))(?=$|\s)/gi,
        currency: /(?<=^|\s)(\$\d*\.?\d{0,2}?)(?=$|\s)/g,
        url: /(?<=^|\s)((https?|git2|s?ftp):\/\/)([a-z][a-z0-9]*\.)+[a-z0-9]{2,}(:[0-9]{1,4})?(\/\S*)?(?=$|\s)/gi,
        url1: /(?<=^|\s)(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9]):([0-9]{1,4})(\/\S*)?(?=$|\s)/g,
        phone: /(?<=^|\s)((\+\d{1,3})?\([0-9]{3}\) [0-9]{3}-[0-9]{4})(?=$|\s)/g
    };

    let output = "";
    let urlUsed = false;

    // for each pattern get all the matches
    for (const [key, regex] of Object.entries(patterns)) {
        const matches = val.match(regex) || [];
        // url and url1 are both urls so combine them into one group
        if (matches.length > 0) {
            if (key === "url") {
                urlUsed = true; 
            }
            if (key === "url1" && urlUsed) {
                output += ``;
            } else if (key === "url1" && !urlUsed) {
                output += `<p>url:</p>`;
            } else {
                output += `<p>${key}:</p>`;
            }
            for (const match of matches) {
                output += `<p style="margin-left:4%;">${match}<p>`;
            }
        }
    }
    
    extracted.innerHTML = output || "<em>None</em>";
}