/**
 * @fileoverview This script contains a collection of functions that provide various functionalities for a web
 * application. These functions are responsible for toggling the editor, forms, uploads, and drawers on the page,
 * managing unsaved changes, handling the drawer's state, and adjusting margins for wiki pages.
 */

(function() {
    function toggleEditor() {
        /**
         * Toggle the editor's visibility and initialize or remove TinyMCE editor accordingly.
         */
        // Get the editor container element
        var editorContainer = document.getElementById("editor-container");

        // Check if editor container is not displayed
        if (editorContainer.style.display === "none") {
            // If not displayed, display the container and initialize the TinyMCE editor
            editorContainer.style.display = "block";
            tinymce.init({
                height: 1000,
                selector: "#myTextarea",
                plugins: "anchor autolink charmap codesample image link lists media searchreplace table visualblocks wordcount",
                toolbar: "export | undo redo | blocks fontfamily fontsize | bold italic underline strikethrough | link image media table | addcomment showcomments | spellcheckdialog a11ycheck | align lineheight | checklist numlist bullist indent outdent | emoticons charmap | removeformat",
                setup: function (editor) {
                    // Save initial content
                    var initialContent = editor.getContent();
                
                    // Add event listener for beforeunload event
                    window.addEventListener("beforeunload", handler, false);
                    window.addEventListener("click", handler, false);

                    function handler(event) {
                        // Check if content has been changed
                        if (initialContent !== editor.getContent()) {
                            // Display confirmation dialog
                            var confirmationMessage = "You have unsaved changes. Do you want to save them?";
                            (event || window.event).returnValue = confirmationMessage;
                            return confirmationMessage;
                        }
                    };
                }
            });
        } else {
            // If displayed, hide the container and remove the TinyMCE editor
            editorContainer.style.display = "none";
            tinymce.remove();
        }
    }

    function toggleForm() {
        /**
         * Toggle the form's visibility and adjust the layout accordingly.
         */
        var uploadBox = document.getElementById("upload-box-box")
        var formContainer = document.getElementById("form-container");
        var toggleButton = document.getElementById("toggleButton");

        if (formContainer.style.display === "block") {
            formContainer.style.display = "none";
            uploadBox.style.marginTop = "40px";
            toggleButton.innerHTML = '<img src="/static/images/back.png">';
            toggleButton.classList.add("upload-button-back")
        } 
        else {
            formContainer.style.display = "block";
            uploadBox.style.marginTop = "200px";
            toggleButton.innerHTML = "Create New Page";
            toggleButton.classList.remove("upload-button-back")
        }
    }

    function toggleSave() {
        /**
         * Toggle the visibility of the save button container.
         */
        var saveContainer = document.getElementById("save-button-container");

        if (saveContainer.style.display === "none") {
            saveContainer.style.display = "block";
        } else {
            saveContainer.style.display = "none";
        }
    }

    function verifyLeaveFunction() {
        /**
         * Verify if the user wants to leave the page with unsaved changes.
         * @return {boolean} to indicate whether to proceed with the default action.
         */
        var editor = tinymce.get("myTextarea");
        var pageSave = sessionStorage.getItem("pageSave")

        // Check if content has been changed
        if (editor.isDirty() && pageSave != "true") {
            // Display confirmation dialog
            var confirmationMessage = "You have unsaved changes. Are you sure you want to leave?";
            if (!confirm(confirmationMessage)) {
            // User chose to cancel, so prevent default action
            return false;
            }
        }
    // Proceed with default action (i.e., go back)
    return location.reload();
    }

    function togglePage() {
        /**
         * Toggle the page data container's visibility and update the toggle button accordingly.
         */
        var formContainer = document.getElementById("page-data-container");
        var toggleButton = document.getElementById("toggleButton");

        if (formContainer.style.display === "block") {
            formContainer.style.display = "none";
            toggleButton.innerHTML = '<img src="/static/images/back.png">';
            toggleButton.setAttribute("onclick", "verifyLeaveFunction()");
        } else {
            formContainer.style.display = "block";
            toggleButton.innerHTML = '<img src="/static/images/edit.png">';
            toggleButton.removeAttribute("onclick");
        }
    }

    function uploadPageFromEditor() {
        /**
         * Upload the content from the TinyMCE editor to the server by submitting the form.
         */
        sessionStorage.setItem("savePage", "true")
        var myContent = tinymce.get("myTextarea").getContent();

        document.getElementById("contentInput").value = myContent;
        document.forms[0].submit();
    }

    function toggleDrawer() {
        /**
         * Toggle the drawer's visibility and store its state in sessionStorage.
         */
        var pageDrawer = document.getElementById("pageDrawer");

        if (pageDrawer.style.display === "block") {
            pageDrawer.style.display = "none";
            sessionStorage.setItem("drawerOpen", "false");
        } else {
            pageDrawer.style.display = "block";
            sessionStorage.setItem("drawerOpen", "true");
        }
    }

    function toggleWikiPageMargin() {
        /**
         * Toggle the margin of the wiki page element.
         */
        if(document.querySelector(".wiki-page") != null) {
            var wikiPage = document.querySelector(".wiki-page");
            
            if (wikiPage.style.marginLeft === "0px") {
                wikiPage.style.marginLeft = "250px";
            } else {
                wikiPage.style.marginLeft = "0px";
            }
        }
    }

    // Event listeners

    document.addEventListener("DOMContentLoaded", function() {
        /**
         * Set the drawer's display state based on the unique-element attribute and sessionStorage value.
         */
        var uniqueElement = document.querySelector(".unique-element");
        var wikiPage = document.querySelector(".wiki-page");
        var pageDrawer = document.getElementById("pageDrawer");
        var drawerOpen = sessionStorage.getItem("drawerOpen");
    
        if (pageDrawer != null) {
            if (uniqueElement && uniqueElement.hasAttribute("data-default-drawer-open")) {
                if (drawerOpen === "true" || drawerOpen === null) {
                    pageDrawer.style.display = "block";
                    wikiPage.style.marginLeft = "250px";
                } else if (drawerOpen === "false") {
                    pageDrawer.style.display = "none";
                    wikiPage.style.marginLeft = "0px";
                }
            } else {
                pageDrawer.style.display = "none";
            }
        }
    });
    

    window.addEventListener("resize", function() {
        /**
         * Toggle the drawer and wiki page margin when the window is resized, based on the unique-element and drawer state.
         */
        var drawerOpen = sessionStorage.getItem("drawerOpen");
        var uniqueElement = document.querySelector(".unique-element");
    
        if (uniqueElement && uniqueElement.hasAttribute("data-default-drawer-open")) {
            if (window.matchMedia("(min-width: 1018px)").matches) {
                if (drawerOpen === "false") {
                    toggleDrawer();
                    toggleWikiPageMargin();
                }
            } else {
                if (drawerOpen === "true") {
                    toggleDrawer();
                    toggleWikiPageMargin();
                }
            }
        }
    });

    window.addEventListener("load", () => {
        /**
         * Hide the loader after the page has finished loading.
         */
        if(document.querySelector(".loader") != null) {
            const loader = document.querySelector(".loader");
            loader.classList.add("loader-hidden");

            loader.addEventListener("transitionend", () => {
                document.body.removeChild(loader);
            });
        }
    });
    window.toggleEditor = toggleEditor;
    window.toggleForm = toggleForm;
    window.toggleSave = toggleSave;
    window.verifyLeaveFunction = verifyLeaveFunction;
    window.togglePage = togglePage;
    window.uploadPageFromEditor = uploadPageFromEditor;
    window.toggleDrawer = toggleDrawer;
    window.toggleWikiPageMargin = toggleWikiPageMargin;
})();
