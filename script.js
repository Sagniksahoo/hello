import * as msal from "@azure/msal-browser";

// MSAL Configuration
const msalConfig = {
    auth: {
        clientId: "YOUR_CLIENT_ID", // Replace with your Azure AD App's client ID
        authority: "https://login.microsoftonline.com/YOUR_TENANT_ID", // Replace with your tenant ID
        redirectUri: window.location.origin // Your website URL
    }
};

// Initialize MSAL instance
const msalInstance = new msal.PublicClientApplication(msalConfig);

// Function to get an access token
async function getAccessToken() {
    const request = {
        scopes: ["https://management.azure.com/.default"], // Azure Management API scope
    };

    try {
        const response = await msalInstance.acquireTokenSilent(request);
        return response.accessToken;
    } catch (error) {
        console.log("Silent token acquisition failed. Trying popup...");
        const response = await msalInstance.acquireTokenPopup(request);
        return response.accessToken;
    }
}

// Function to fetch workbooks
async function fetchWorkbooks() {
    const token = await getAccessToken();
    const response = await fetch(
        "https://management.azure.com/providers/Microsoft.ResourceGraph/resources?api-version=2021-03-01",
        {
            method: "POST",
            headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                subscriptions: ["YOUR_SUBSCRIPTION_ID"], // Replace with your Azure subscription ID
                query: "Resources | where type == 'microsoft.insights/workbooks'"
            })
        }
    );

    if (!response.ok) {
        console.error("Failed to fetch workbooks:", await response.text());
        return [];
    }

    const data = await response.json();
    return data.data;
}

// Function to display workbooks in a styled box
async function displayWorkbooks() {
    const container = document.getElementById("workbook-box");
    container.innerHTML = "Loading workbooks...";

    try {
        const workbooks = await fetchWorkbooks();
        container.innerHTML = ""; // Clear the loading message

        workbooks.forEach((workbook) => {
            const box = document.createElement("div");
            box.style.border = "1px solid #ddd";
            box.style.padding = "10px";
            box.style.margin = "10px";
            box.style.borderRadius = "5px";

            box.innerHTML = `
                <h3>${workbook.name}</h3>
                <p>Location: ${workbook.location}</p>
                <a href="https://portal.azure.com/#@/resource/${workbook.id}" target="_blank">View in Azure</a>
            `;
            container.appendChild(box);
        });
    } catch (error) {
        container.innerHTML = `<p>Error fetching workbooks: ${error.message}</p>`;
        console.error(error);
    }
}

// Call displayWorkbooks on page load
displayWorkbooks();
