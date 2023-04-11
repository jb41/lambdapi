var messages = [];
var editor = null;
var func = {};
var runtimes = [];
var codeHistory = [];
var currentCodeIndex = -1;

/*
 * ******** ******** ******** ******** ******** ******** ******** ********
 *
 * Code Editor
 * 
 */

require.config({ paths: { 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.31.1/min/vs' }});

function loadMonacoEditor() {
    return new Promise((resolve) => {
        require(['vs/editor/editor.main'], function () {
            const editor = monaco.editor.create(document.getElementById('code-editor'), {
                language: 'python',
                theme: 'vs-light',
                minimap: { enabled: false }
            });
            resolve(editor);
        });
    });
}

/*
 * ******** ******** ******** ******** ******** ******** ******** ********
 *
 * Function stuff
 * 
 */
function fetchHelper(url, options = {}) {
    return new Promise((resolve, reject) => {
        fetch(url, options)
        .then(response => {
            if (!response.ok) { throw new Error(`HTTP error! Status: ${response.status}`); }
            return response.json();
        })
        .then(data => {
            resolve(data);
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            reject(error);
        });
    });
}

function getFunctionId() {
    return (new URLSearchParams(window.location.search)).get('id');
}

function getFunction(functionId) {
    return fetchHelper('/api/functions/' + functionId);
}

function updateFunction(functionId, params) {
    return fetchHelper('/api/functions/' + functionId, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json', },
        body: JSON.stringify(params),
    });
}

function getRuntimes() {
    return fetchHelper('/api/runtimes/available');
}

/*
 * ******** ******** ******** ******** ******** ******** ******** ********
 *
 * Run stuff
 * 
 */
function runCode(endpoint_url, params) {
    showSpinner();
    fetch(endpoint_url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', },
        body: JSON.stringify(params),
    })
    .then(response => {
        hideSpinner();
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.indexOf('application/json') !== -1) {
            return response.json().then(showJsonResult);
        } else if (contentType && contentType.indexOf('image/') !== -1) {
            return response.blob().then(showImageResult);
        } else {
            return response.blob().then(blob => showDownloadResult(blob, contentType));
        }
    })
    .catch(error => { console.error('Error fetching data:', error); });
}

function paramsList() {
    const paramsList = document.getElementById('input-params').value.split('\n');

    if (paramsList.length > 0 && paramsList[0].length > 0) {
        return paramsList.reduce((params, value, index) => {
            params[index.toString()] = value;
            return params;
        }, {});
    } else {
        return {};
    }
}

function createResultElement(childElement) {
    const resultOutput = document.getElementById('result-output');
    resultOutput.innerHTML = '';
    resultOutput.appendChild(childElement);
}

function showJsonResult(result) {
    const codeElement = document.createElement('code');
    codeElement.innerText = JSON.stringify(result, null, 4);

    const preElement = document.createElement('pre');
    preElement.appendChild(codeElement);

    createResultElement(preElement);
}

function showImageResult(imageBlob) {
    const imageUrl = URL.createObjectURL(imageBlob);
    const img = document.createElement('img');
    img.src = imageUrl;

    createResultElement(img);
}

function showDownloadResult(fileBlob, contentType) {
    const downloadUrl = URL.createObjectURL(fileBlob);
    const downloadLink = document.createElement('a');
    downloadLink.href = downloadUrl;
    downloadLink.download = 'download.' + getFileExtension(contentType);
    downloadLink.innerText = 'Download file';
    downloadLink.classList.add('btn');
    downloadLink.classList.add('btn-primary');

    createResultElement(downloadLink);
}

function getFileExtension(contentType) {
    const ext = contentType.split('/').pop().split(';')[0];
    return ext === 'octet-stream' ? '' : ext;
}

/*
 * ******** ******** ******** ******** ******** ******** ******** ********
 *
 * UI Manipulation
 * 
 */
function getLanguageForRuntime(runtime) {
    const foundRuntime = runtimes.find(rt => rt.runtime === runtime);

    if (foundRuntime) {
        return foundRuntime.monaco_editor_id;
    } else {
        throw new Error(`Runtime ${runtime} not found`);
    }
}

function setFunctionValues() {
    document.getElementById('function-name').textContent = func.name;

    document.getElementById('function-runtime').value = func.runtime || 'python';
    const language = getLanguageForRuntime(func.runtime || 'python');
    monaco.editor.setModelLanguage(editor.getModel(), language);

    document.getElementById('function-endpoint-url').text = func.endpoint_url;
    document.getElementById('function-endpoint-url').href = func.endpoint_url;

    if (func.code) {
        editor.setValue(func.code);
        codeHistory.push(func.code);
        currentCodeIndex += 1;
    }
}

function setRuntimes() {
    const select = document.getElementById('function-runtime');
    runtimes.forEach(runtime => {
        const option = document.createElement('option');
        option.value = runtime.runtime;
        option.text = runtime.name;
        select.appendChild(option);
    });
}

/*
 * ******** ******** ******** ******** ******** ******** ******** ********
 *
 * Save & Run
 * 
 */
async function saveAndRun() {
    await updateFunction(func.id, {
        name: document.getElementById('function-name').textContent,
        code: editor.getValue(),
        runtime: document.getElementById('function-runtime').value,
    });
    if (editor.getValue() !== codeHistory[currentCodeIndex]) {
        codeHistory.push(editor.getValue());
        currentCodeIndex += 1;
        changePrevNextHistoryButtonDisabledState();
    }
    runCode(func.endpoint_url, paramsList());
}

/*
 * ******** ******** ******** ******** ******** ******** ******** ********
 *
 * Completion
 * 
 */
function createCurrentMessageForCompletion() {
    const code = editor.getValue();
    const llmPrompt = document.getElementById('llm-prompt').value;
    
    const newMessage = "current code:\n```" + code + "```\n\n" + llmPrompt;
    return { "role": "user", "content": newMessage };
}

function updateCodeInEditor(code) {
    if (code.length > 0) {
        editor.setValue(code);
    }
    if (code !== codeHistory[currentCodeIndex]) {
        codeHistory.push(code);
        currentCodeIndex += 1;
        changePrevNextHistoryButtonDisabledState();
    }
}

function updateTextOutput(text) {
    document.getElementById('output').innerHTML = "<p>" + text + "</p>";
}

function requestCompletions() {
    showSpinner();
    const selectedRuntime = document.getElementById('function-runtime').value;
    fetch('/api/completions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', },
        body: JSON.stringify({
            messages: messages,
            language: getLanguageForRuntime(selectedRuntime)
        })
    })
    .then(response => {
        hideSpinner();
        if (!response.ok) { throw new Error(`HTTP error! Status: ${response.status}`); }
        return response.json();
    })
    .then(data => {
        messages.push(data.message);
        updateCodeInEditor(data.code);
        updateTextOutput(data.text);
    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });
}

function getCompletion() {
    messages.push(createCurrentMessageForCompletion());
    document.getElementById('llm-prompt').value = '';
    requestCompletions();
}

/*
 * ******** ******** ******** ******** ******** ******** ******** ********
 *
 * Code history
 * 
 */
function changePrevNextHistoryButtonDisabledState() {
    const prevButton = document.getElementById('prev-code-in-history');
    const nextButton = document.getElementById('next-code-in-history');
    
    prevButton.disabled = currentCodeIndex <= 0;
    nextButton.disabled = currentCodeIndex >= codeHistory.length - 1;
}

function navigateCodeHistory(direction) {
    const newIndex = currentCodeIndex + direction;

    if (newIndex >= 0 && newIndex < codeHistory.length) {
        currentCodeIndex = newIndex;
        editor.setValue(codeHistory[currentCodeIndex]);
        changePrevNextHistoryButtonDisabledState();
    }
}

/*
 * ******** ******** ******** ******** ******** ******** ******** ********
 *
 * Helpers
 * 
 */
const debounce = (func, wait) => {
    let timeout;
    return (...args) => {
        clearTimeout(timeout);
        timeout = setTimeout(() => func(...args), wait);
    };
};

const showSpinner = () => document.getElementById('spinner').style.display = 'flex';

const hideSpinner = () => document.getElementById('spinner').style.display = 'none';

const autoResizeTextarea = textarea => {
    textarea.style.height = 'auto';
    textarea.style.height = `${textarea.scrollHeight}px`;
};

const copyEndpointUrlToClipboard = async () => {
    const textToCopy = document.getElementById('function-endpoint-url').text;
    try {
        await navigator.clipboard.writeText(textToCopy);
    } catch (err) {
        console.error('Failed to copy text:', err);
    }
};

/*
 * ******** ******** ******** ******** ******** ******** ******** ********
 *
 * Init
 * 
 */
async function init() {
    try {
        editor = await loadMonacoEditor();
        runtimes = await getRuntimes();
        setRuntimes(runtimes);
        console.log(runtimes);
        func = await getFunction(getFunctionId());
        setFunctionValues(func);
    } catch (error) {
        console.error('Error:', error);
    }
}


init();

document.getElementById('function-name').addEventListener('input', debounce((event) => {
    updateFunction(func.id, { name: event.target.textContent });
}, 1000));

document.getElementById('function-runtime').addEventListener('change', (event) => {
    const selectedRuntime = event.target.value;
    const language = getLanguageForRuntime(selectedRuntime);
    monaco.editor.setModelLanguage(editor.getModel(), language);
    updateFunction(func.id, { runtime: selectedRuntime });
});

document.getElementById('llm-prompt').addEventListener('input', (event) => {
    autoResizeTextarea(event.target);
});

document.getElementById('llm-prompt').focus();
