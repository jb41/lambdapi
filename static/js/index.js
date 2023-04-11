const apiUrl = '/api/functions';

const fetchFunctions = async () => (await fetch(apiUrl)).json();

const deleteFunction = async functionId => {
    if (!confirm("Are you sure you want to delete this function?")) return;
    try {
        const response = await fetch(`${apiUrl}/${functionId}`, { method: 'DELETE' });
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
        location.reload();
    } catch (error) {
        console.error('Error fetching data:', error);
    }
};

const createNewFunction = async () => {
    try {
        const response = await fetch(apiUrl, { method: 'POST' });
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
        const data = await response.json();
        window.location.href = `/function-details.html?id=${data.id}`;
    } catch (error) {
        console.error('Error fetching data:', error);
    }
};

const displayFunctions = functions => {
    const functionList = document.getElementById('function-list');
    functionList.innerHTML = '';

    functions.forEach(func => {
        const rowItem = document.createElement('tr');
        rowItem.innerHTML = `
            <td>${func.id}</td>
            <td><strong>${func.name}</strong></td>
            <td>${func.runtime}</td>
            <td>${func.created_at}</td>
            <td>
                <span>${func.endpoint_url}&nbsp;</span>
                <button class="btn btn-link" onclick="copyEndpointUrlToClipboard('${func.endpoint_url}')">
                    <i class="bi bi-clipboard2"></i>
                </button>
            </td>
            <td><a href="/function-details.html?id=${func.id}" class="btn btn-primary"><i class="bi bi-pen"></i>&nbsp;Edit</a></td>
            <td><button class="btn btn-danger" onclick="deleteFunction(${func.id})"><i class="bi bi-trash3"></i>&nbsp;Delete</button></td>
        `;
        functionList.appendChild(rowItem);
    });
};

const copyEndpointUrlToClipboard = async textToCopy => {
    try {
        await navigator.clipboard.writeText(textToCopy);
    } catch (err) {
        console.error('Failed to copy text: ', err);
    }
};

(async () => {
    try {
        const functions = await fetchFunctions();
        displayFunctions(functions);
    } catch (error) {
        console.error('Error fetching data:', error);
    }
})();
