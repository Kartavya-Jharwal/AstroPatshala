// ======== LOCAL STORAGE LOGIC ========
const lsInput = document.getElementById('ls-input');
const lsOutput = document.getElementById('ls-output');
const lsSaveBtn = document.getElementById('ls-save');

// Load existing data
const existingData = localStorage.getItem('demoData');
if (existingData) {
    lsOutput.textContent = existingData;
    lsInput.value = existingData;
}

lsSaveBtn.addEventListener('click', () => {
    const val = lsInput.value;
    localStorage.setItem('demoData', val);
    lsOutput.textContent = val;
});


// ======== OPFS (Origin Private File System) LOGIC ========
const opfsInput = document.getElementById('opfs-input');
const opfsOutput = document.getElementById('opfs-output');
const opfsSaveBtn = document.getElementById('opfs-save');
const opfsReadBtn = document.getElementById('opfs-read');

const FILE_NAME = 'startup_data.txt';

async function saveToOPFS(content) {
    try {
        const root = await navigator.storage.getDirectory();
        // Create or get the file
        const fileHandle = await root.getFileHandle(FILE_NAME, { create: true });
        // Create a writable stream to the file
        const writable = await fileHandle.createWritable();
        // Write the contents
        await writable.write(content);
        // Close the file
        await writable.close();
        
        alert('File successfully saved to OPFS!');
    } catch (error) {
        console.error("Error saving to OPFS:", error);
        alert('Failed to save to OPFS. See console for details.');
    }
}

async function readFromOPFS() {
    try {
        const root = await navigator.storage.getDirectory();
        // Get the file
        const fileHandle = await root.getFileHandle(FILE_NAME);
        const file = await fileHandle.getFile();
        const content = await file.text();
        
        opfsOutput.textContent = content || '(Empty File)';
    } catch (error) {
        if (error.name === 'NotFoundError') {
            opfsOutput.textContent = 'File not found. Save something first!';
        } else {
            console.error("Error reading from OPFS:", error);
            opfsOutput.textContent = 'Error reading file.';
        }
    }
}

opfsSaveBtn.addEventListener('click', () => {
    saveToOPFS(opfsInput.value);
});

opfsReadBtn.addEventListener('click', () => {
    readFromOPFS();
});