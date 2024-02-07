
  document.addEventListener('DOMContentLoaded', function() {
    let dropArea = document.getElementById('drop-area');

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

    });
}


function previewFile(file) {
    let reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onloadend = function() {
        let img = document.createElement('img');
        img.src = reader.result;
        img.style.width = '100px'; // Directly set the width
        img.style.height = 'auto'; // Keep the aspect ratio
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
    
  
  