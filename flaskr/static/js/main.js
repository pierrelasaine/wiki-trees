function toggleEditor() {
    var editorContainer = document.getElementById('editor-container');
    if (editorContainer.style.display === 'none') {
        editorContainer.style.display = 'block';
        tinymce.init({
            selector: '#myTextarea',
            plugins: 'anchor autolink charmap codesample image link lists media searchreplace table visualblocks wordcount checklist mediaembed casechange export formatpainter pageembed linkchecker a11ychecker tinymcespellchecker permanentpen powerpaste advtable advcode editimage tableofcontents footnotes mergetags autocorrect typography inlinecss file_export',
            toolbar: 'export | undo redo | blocks fontfamily fontsize | bold italic underline strikethrough | link image media table mergetags | addcomment showcomments | spellcheckdialog a11ycheck typography | align lineheight | checklist numlist bullist indent outdent | emoticons charmap | removeformat',
        });
    } else {
        editorContainer.style.display = 'none';
        tinymce.remove();
    }
}
function toggleForm() {
var formContainer = document.getElementById('form-container');
var toggleButton = document.getElementById('toggleButton');
if (formContainer.style.display === 'block') {
    formContainer.style.display = 'none';
    toggleButton.innerHTML = "Back";
} else {
    formContainer.style.display = 'block';
    toggleButton.innerHTML = "Create New Page";
}
}
function toggleUpload() {
var saveContainer = document.getElementById('save-button-container');
if (saveContainer.style.display === 'none') {
    saveContainer.style.display = 'block';
} else {
    saveContainer.style.display = 'none';
}
}
function togglePage() {
    var formContainer = document.getElementById('page-data-container');
    var toggleButton = document.getElementById('toggleButton');
    if (formContainer.style.display === 'block') {
        formContainer.style.display = 'none';
        toggleButton.innerHTML = "Back";
    } else {
        formContainer.style.display = 'block';
        toggleButton.innerHTML = "Edit Page";
    }
}
function toggleSave() {
    var saveContainer = document.getElementById('save-button-container');
    if (saveContainer.style.display === 'none') {
        saveContainer.style.display = 'block';
    } else {
        saveContainer.style.display = 'none';
    }
}
function uploadPageFromEditor() {
    var myContent = tinymce.get("myTextarea").getContent();
    document.getElementById("contentInput").value = myContent;
    document.forms[0].submit();
}