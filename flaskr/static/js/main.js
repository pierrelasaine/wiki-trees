function toggleEditor() {
    var editorContainer = document.getElementById('editor-container');
    if (editorContainer.style.display === 'none') {
        editorContainer.style.display = 'block';
        tinymce.init({
            height: 1000,
            selector: '#myTextarea',
            plugins: 'anchor autolink charmap codesample image link lists media searchreplace table visualblocks wordcount checklist mediaembed casechange export formatpainter pageembed linkchecker a11ychecker tinymcespellchecker permanentpen powerpaste advtable advcode editimage tableofcontents autocorrect',
            toolbar: 'export | undo redo | blocks fontfamily fontsize | bold italic underline strikethrough | link image media table | addcomment showcomments | spellcheckdialog a11ycheck | align lineheight | checklist numlist bullist indent outdent | emoticons charmap | removeformat',
            setup: function (editor) {
                // Save initial content
                var initialContent = editor.getContent();
            
                // Add event listener for beforeunload event
                window.addEventListener('beforeunload', handler, false);
                window.addEventListener('click', handler, false);

                function handler(event) {
                  // Check if content has been changed
                  if (initialContent !== editor.getContent()) {
                    // Display confirmation dialog
                    var confirmationMessage = 'You have unsaved changes. Do you want to save them?';
                    (event || window.event).returnValue = confirmationMessage;
                    return confirmationMessage;
                  }
                };

              }
        });
    } else {
        editorContainer.style.display = 'none';
        tinymce.remove();
    }
}

function toggleForm() {
    var uploadBox = document.getElementById('upload-box-box')
    var formContainer = document.getElementById('form-container');
    var toggleButton = document.getElementById('toggleButton');
    if (formContainer.style.display === 'block') {
        formContainer.style.display = 'none';
        uploadBox.style.marginTop = '40px';
        toggleButton.innerHTML = "<img src='/static/images/back.png'>";
        toggleButton.classList.add('upload-button-back')
    } 
    else {
        formContainer.style.display = 'block';
        uploadBox.style.marginTop = '200px'
        toggleButton.innerHTML = "Create New Page";
        toggleButton.classList.remove('upload-button-back')
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

function verifyLeaveFunction(){
    var editor = tinymce.get("myTextarea");

    // Check if content has been changed
    if (editor.isDirty()) {
        // Display confirmation dialog
        var confirmationMessage = 'You have unsaved changes. Are you sure you want to leave?';
        if (!confirm(confirmationMessage)) {
        // User chose to cancel, so prevent default action
        return false;
        }

    }

  // Proceed with default action (i.e., go back)
  return window.history.back();
}

function togglePage() {
    var formContainer = document.getElementById('page-data-container');
    var toggleButton = document.getElementById('toggleButton');
    if (formContainer.style.display === 'block') {
        formContainer.style.display = 'none';
        toggleButton.innerHTML = "<img src='/static/images/back.png'>";
        toggleButton.setAttribute("onclick", "verifyLeaveFunction()");
    } 
    else {
        formContainer.style.display = 'block';
        toggleButton.innerHTML = "<img src='/static/images/edit.png'>";
        toggleButton.removeAttribute("onclick");
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
    if (drawerOpen === 'true') {
        pageDrawer.style.display = 'block';
    } else {
        pageDrawer.style.display = 'none';
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
document.addEventListener('DOMContentLoaded', function() {
    var uniqueElement = document.querySelector('.unique-element');
    if (uniqueElement && uniqueElement.hasAttribute('data-default-drawer-open')) {
        var pageDrawer = document.getElementById('toggleDrawer');
        pageDrawer.style.display = 'block';
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

window.addEventListener("load", () => {
    const loader = document.querySelector(".loader")
    loader.classList.add("loader-hidden")

    loader.addEventListener("transitioned", () => {
        document.body.removeChild("loader");
    })
});