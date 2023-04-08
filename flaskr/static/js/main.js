function toggleEditor() {
    var editorContainer = document.getElementById('editor-container');
    if (editorContainer.style.display === 'none') {
        editorContainer.style.display = 'block';
        tinymce.init({
            height: 1000,
            selector: '#myTextarea',
            plugins: 'anchor autolink charmap codesample image link lists media searchreplace table visualblocks wordcount checklist mediaembed casechange export formatpainter pageembed linkchecker a11ychecker tinymcespellchecker permanentpen powerpaste advtable advcode editimage tableofcontents autocorrect',
            toolbar: 'export | undo redo | blocks fontfamily fontsize | bold italic underline strikethrough | link image media table | addcomment showcomments | spellcheckdialog a11ycheck | align lineheight | checklist numlist bullist indent outdent | emoticons charmap | removeformat',
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
function toggleDrawer() {
    var pageDrawer = document.getElementById('toggleDrawer');
    if (pageDrawer.style.display === 'block') {
        pageDrawer.style.display = 'none';
        sessionStorage.setItem('drawerOpen', 'false');
    } else {
        pageDrawer.style.display = 'block';
        sessionStorage.setItem('drawerOpen', 'true');
    }
}
document.addEventListener('DOMContentLoaded', function() {
    var drawerOpen = sessionStorage.getItem('drawerOpen');
    var pageDrawer = document.getElementById('toggleDrawer');
    var wikiPage = document.querySelector('.wiki-page');
    if (drawerOpen === 'true') {
        pageDrawer.style.display = 'block';
    } else {
        pageDrawer.style.display = 'none';
        wikiPage.style.marginLeft = '0px';
    }
});
function toggleWikiPageMargin() {
    var wikiPage = document.querySelector('.wiki-page');
    if (wikiPage.style.marginLeft === '0px') {
        wikiPage.style.marginLeft = '250px';
    } else {
        wikiPage.style.marginLeft = '0px';
    }
}
document.addEventListener('DOMContentLoaded', function() {
    var uniqueElement = document.querySelector('.unique-element');
    if (!(uniqueElement && uniqueElement.hasAttribute('data-default-drawer-open'))) {
        var pageDrawer = document.getElementById('toggleDrawer');
        pageDrawer.style.display = 'none';
    }
});
window.addEventListener('resize', function() {
    var drawerOpen = sessionStorage.getItem('drawerOpen');
    var uniqueElement = document.querySelector('.unique-element');
    if (window.matchMedia('(max-width: 768px)').matches && (uniqueElement && uniqueElement.hasAttribute('data-default-drawer-open')) && (drawerOpen === 'true')) {
        toggleDrawer();
        toggleWikiPageMargin();
    }
  });
