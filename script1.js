// Function to display workbooks in a styled box
async function displayWorkbooks() {
    const container = document.getElementById("workbook-box");
    container.innerHTML = "Loading workbooks...";

    try {
        const workbooks = await fetchWorkbooks();
        container.innerHTML = ""; // Clear the loading message

        workbooks.forEach((workbook) => {
            // Create a container for the workbook
            const box = document.createElement("div");
            box.style.border = "1px solid #ddd";
            box.style.padding = "10px";
            box.style.margin = "10px";
            box.style.borderRadius = "5px";
            box.style.width = "100%"; // Full width
            box.style.height = "600px"; // Adjust height as needed

            // Embed workbook in an iframe
            box.innerHTML = `
                <h3>${workbook.name}</h3>
                <iframe 
                    src="https://portal.azure.com/#@/resource/${workbook.id}" 
                    style="width: 100%; height: 90%; border: none;"
                    title="Workbook: ${workbook.name}">
                </iframe>
            `;

            container.appendChild(box);
        });
    } catch (error) {
        container.innerHTML = `<p>Error fetching workbooks: ${error.message}</p>`;
        console.error(error);
    }
}
