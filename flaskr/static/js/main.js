/**
 * @fileoverview This script contains a collection of functions that provide various functionalities for a web
 * application. These functions are responsible for toggling the editor, forms, uploads, and drawers on the page,
 * managing unsaved changes, handling the drawer's state, and adjusting margins for wiki pages.
 */

/**
 * Toggle the editor's visibility and initialize or remove TinyMCE editor accordingly.
 */
function toggleEditor() {
    // Get the editor container element
    var editorContainer = document.getElementById('editor-container');

    // Check if editor container is not displayed
    if (editorContainer.style.display === 'none') {
        // If not displayed, display the container and initialize the TinyMCE editor
        editorContainer.style.display = 'block';
        tinymce.init({
            height: 1000,
            selector: '#myTextarea',
            plugins: 'anchor autolink charmap codesample image link lists media searchreplace table visualblocks wordcount',
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
        // If displayed, hide the container and remove the TinyMCE editor
        editorContainer.style.display = 'none';
        tinymce.remove();
    }
}

/**
 * Toggle the form's visibility and adjust the layout accordingly.
 */
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

/**
 * Toggle the visibility of the save button container.
 */
function toggleUpload() {
    var saveContainer = document.getElementById('save-button-container');

    if (saveContainer.style.display === 'none') {
        saveContainer.style.display = 'block';
    } else {
        saveContainer.style.display = 'none';
    }
}

/**
 * Verify if the user wants to leave the page with unsaved changes.
 * @return {boolean} to indicate whether to proceed with the default action.
 */
function verifyLeaveFunction() {
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

/**
 * Toggle the page data container's visibility and update the toggle button accordingly.
 */
function togglePage() {
    var formContainer = document.getElementById('page-data-container');
    var toggleButton = document.getElementById('toggleButton');

    if (formContainer.style.display === 'block') {
        formContainer.style.display = 'none';
        toggleButton.innerHTML = "<img src='/static/images/back.png'>";
        toggleButton.setAttribute("onclick", "verifyLeaveFunction()");
    } else {
        formContainer.style.display = 'block';
        toggleButton.innerHTML = "<img src='/static/images/edit.png'>";
        toggleButton.removeAttribute("onclick");
    }
}

/**
 * Toggle the visibility of the save button container.
 */
function toggleSave() {
    var saveContainer = document.getElementById('save-button-container');

    if (saveContainer.style.display === 'none') {
        saveContainer.style.display = 'block';
    } else {
        saveContainer.style.display = 'none';
    }
}

/**
 * Upload the content from the TinyMCE editor to the server by submitting the form.
 */
function uploadPageFromEditor() {
    var myContent = tinymce.get("myTextarea").getContent();

    document.getElementById("contentInput").value = myContent;
    document.forms[0].submit();
}

/**
 * Toggle the drawer's visibility and store its state in sessionStorage.
 */
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

/**
 * Toggle the margin of the wiki page element.
 */
function toggleWikiPageMargin() {
    var wikiPage = document.querySelector('.wiki-page');
    
    if (wikiPage.style.marginLeft === '0px') {
        wikiPage.style.marginLeft = '250px';
    } else {
        wikiPage.style.marginLeft = '0px';
    }
}

// Event listeners

/**
 * Set the drawer's display state based on the value stored in sessionStorage.
 */
document.addEventListener('DOMContentLoaded', function() {
    var drawerOpen = sessionStorage.getItem('drawerOpen');
    var pageDrawer = document.getElementById('toggleDrawer');

    if (drawerOpen === 'true') {
        pageDrawer.style.display = 'block';
    } else {
        pageDrawer.style.display = 'none';
    }
});

/**
 * Hide the drawer if the unique-element is not present or does not have the data-default-drawer-open attribute.
 */
document.addEventListener('DOMContentLoaded', function() {
    var uniqueElement = document.querySelector('.unique-element');

    if (!(uniqueElement && uniqueElement.hasAttribute('data-default-drawer-open'))) {
        var pageDrawer = document.getElementById('toggleDrawer');
        pageDrawer.style.display = 'none';
    }
});

/**
 * Show the drawer if the unique-element is present and has the data-default-drawer-open attribute.
 */
document.addEventListener('DOMContentLoaded', function() {
    var uniqueElement = document.querySelector('.unique-element');

    if (uniqueElement && uniqueElement.hasAttribute('data-default-drawer-open')) {
        var pageDrawer = document.getElementById('toggleDrawer');
        pageDrawer.style.display = 'block';
    }
});

/**
 * Toggle the drawer and wiki page margin when the window is resized, based on the unique-element and drawer state.
 */
window.addEventListener('resize', function() {
    var drawerOpen = sessionStorage.getItem('drawerOpen');
    var uniqueElement = document.querySelector('.unique-element');

    if (window.matchMedia('(max-width: 768px)').matches && (uniqueElement && uniqueElement.hasAttribute('data-default-drawer-open')) && (drawerOpen === 'true')) {
        toggleDrawer();
        toggleWikiPageMargin();
    }
});

/**
 * Hide the loader after the page has finished loading.
 */
window.addEventListener("load", () => {
    const loader = document.querySelector(".loader");
    loader.classList.add("loader-hidden");

    loader.addEventListener("transitionend", () => {
        document.body.removeChild(loader);
    });
});