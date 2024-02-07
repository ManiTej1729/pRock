
    document.addEventListener('DOMContentLoaded', function() {

    let dropArea = document.getElementById('drop-area');
    let confirmButton = document.getElementById('confirm-selection-button');
    confirmButton.addEventListener('click', function() {
        handleConfirmSelection(); // Removed the unnecessary parameter here
    });

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });

    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false);
    });

    dropArea.addEventListener('drop', handleDrop, false);
    
});
function handleMusic(files) {
        let musicFile = files[0]; // Assume only one file is selected
        console.log('Selected music file:', musicFile);
        // You can handle the selected music file here (e.g., store it in memory or display its name)
    }

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

function highlight(e) {
    dropArea.classList.add('highlight');
}

function unhighlight(e) {
    dropArea.classList.remove('highlight');
}

function handleDrop(e) {
    let dt = e.dataTransfer;
    let files = dt.files;

    handleFiles(files);
}

function handleFiles(files) {
    ([...files]).forEach(file => {
        uploadFile(file);
        previewFile(file);
        displayFileName(file);
        addCheckbox(file)
    });

}

function previewFile(file) {
    let reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onloadend = function() {
        let img = document.createElement('img');
        img.src = reader.result;
        document.getElementById('gallery').appendChild(img);
    };
}

function displayFileName(file) {
    let fileList = document.getElementById('file-list'); // Ensure this element exists in your HTML
    let listItem = document.createElement('li');
    listItem.textContent = file.name;
    fileList.appendChild(listItem);
}


  function uploadFile(file) {
    // Simulate an upload process
    const url = 'your-upload-endpoint'; // Placeholder URL
    const formData = new FormData();
    formData.append('file', file);
  
    // Simulate progress and success/error handling
    console.log(`Uploading ${file.name}...`);
    simulateUploadProgress(file);
  }
  
  function simulateUploadProgress(file) {
    let progress = 0;
    const interval = setInterval(() => {
      progress += 10;
      console.log(`${file.name}: ${progress}%`);
      if (progress >= 100) {
        clearInterval(interval);
        // Simulate a successful upload with a 10% chance of failure
        if (Math.random() < 0.1) {
          console.error(`${file.name} failed to upload.`);
          // Handle the error, e.g., show an error message to the user
        } else {
          console.log(`${file.name} uploaded successfully.`);
          // Handle the success, e.g., update the UI to reflect the upload status
        }
      }
    }, 200);
  }
  function addCheckbox(file) {
    let photoSelectionDiv = document.getElementById('photo-selection');
    if (!photoSelectionDiv) {
        photoSelectionDiv = document.createElement('div');
        photoSelectionDiv.id = 'photo-selection';
        document.getElementById('drop-area').appendChild(photoSelectionDiv);
    }

    let checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.value = file.name;
    checkbox.id = `checkbox-${file.name}`; // Use file name as the unique identifier

    let label = document.createElement('label');
    label.htmlFor = `checkbox-${file.name}`; // Match label to checkbox
    label.textContent = file.name;

    let br = document.createElement('br');

    photoSelectionDiv.appendChild(checkbox);
    photoSelectionDiv.appendChild(label);
    photoSelectionDiv.appendChild(br);
}

function handleConfirmSelection() {
    // Check if the 'Preview' button already exists
    let existingPreviewButton = document.getElementById('preview-button');
    if (!existingPreviewButton) {
        let previewButton = document.createElement('button');
        previewButton.id = 'preview-button'; // Assign an ID to the button for easy reference
        previewButton.textContent = 'Preview';
        previewButton.addEventListener('click', handlePreview);

        let breakLine = document.createElement('br'); // Create a line break
        let breakLine2 = document.createElement('br'); // Create a line break

        let buttonParent = document.getElementById('confirm-selection-button').parentNode;
        buttonParent.appendChild(breakLine); // Append the line break to the parent container
        buttonParent.appendChild(breakLine2); // Append the line break to the parent container
        buttonParent.appendChild(previewButton); // Append the 'Preview' button after the line break
    }
}


function handlePreview() {
    // Navigate to the preview page
    window.location.href = 'preview.html'; // Replace 'preview.html' with the URL of your preview page
}