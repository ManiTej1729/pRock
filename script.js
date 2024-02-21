
document.addEventListener('DOMContentLoaded', function() {

  let dropArea = document.getElementById('drop-area');
  let confirmButton = document.getElementById('confirm-selection-button');
  confirmButton.addEventListener('click', function() {
      handleConfirmSelection();
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
      let musicFile = files[0]; 
      console.log('Selected music file:', musicFile);
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
  let fileList = document.getElementById('file-list');
  let listItem = document.createElement('li');
  listItem.textContent = file.name;
  fileList.appendChild(listItem);
}


function uploadFile(file) {
  const url = 'your-upload-endpoint';
  const formData = new FormData();
  formData.append('file', file);

  console.log(`Uploading ${file.name}...`);
  simulateUploadProgress(file);
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
  checkbox.id = `checkbox-${file.name}`;

  let label = document.createElement('label');
  label.htmlFor = `checkbox-${file.name}`;
  label.textContent = file.name;

  let br = document.createElement('br');

  photoSelectionDiv.appendChild(checkbox);
  photoSelectionDiv.appendChild(label);
  photoSelectionDiv.appendChild(br);
}

function handleConfirmSelection() {
  let existingPreviewButton = document.getElementById('preview-button');
  if (!existingPreviewButton) {
      let previewButton = document.createElement('button');
      previewButton.id = 'preview-button';
      previewButton.textContent = 'Preview';
      previewButton.addEventListener('click', handlePreview);

      let breakLine = document.createElement('br');
      let breakLine2 = document.createElement('br');

      let buttonParent = document.getElementById('confirm-selection-button').parentNode;
      buttonParent.appendChild(breakLine);
      buttonParent.appendChild(breakLine2);
      buttonParent.appendChild(previewButton);
  }
}


function handlePreview() {
  window.location.href = 'video.html';
}
