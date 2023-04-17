/**
 * Test suite for the JavaScript functions used in the Wiki application.
 *
 * This test suite covers the following functions:
 *  - toggleEditor(): Toggles the visibility of the TinyMCE editor and initializes/destroys it accordingly.
 *  - toggleForm(): Toggles the visibility of the form container and adjusts the layout.
 *  - toggleSave(): Toggles the visibility of the save button container.
 *  - togglePage(): Toggles the visibility of the page data container and updates the toggle button.
 *  - toggleDrawer(): Toggles the visibility of the drawer and stores its state in sessionStorage.
 *  - toggleWikiPageMargin(): Toggles the margin of the wiki page element.
 *  - uploadPageFromEditor(): Uploads the content from the TinyMCE editor to the server by submitting the form.
 *
 * Each function is tested using the Jasmine testing framework, with beforeEach and afterEach hooks
 * to set up and clean up the required DOM elements for each test case.
 *
 * Test Cases:
 *
 * 1. 'toggleEditor()':
 *     - Verify that the editor's visibility is toggled ON and the TinyMCE editor is initialized.
 *     - Verify that the editor's visibility is toggled OFF and the TinyMCE editor is destroyed.
 *
 * 2. 'toggleForm()':
 *     - Verify that the form's visibility is toggled OFF and the layout is adjusted accordingly.
 *     - Verify that the form's visibility is toggled ON and the layout is adjusted accordingly.
 *
 * 3. 'toggleSave()':
 *     - Verify that the save button container's visibility is toggled ON.
 *     - Verify that the save button container's visibility is toggled OFF.
 *
 * 4. 'togglePage()':
 *     - Verify that the page data container's visibility is toggled OFF and the toggle button is updated.
 *     - Verify that the page data container's visibility is toggled ON and the toggle button is updated.
 *
 * 5. 'toggleDrawer()':
 *     - Verify that the drawer's visibility is toggled OFF and its state is stored in sessionStorage.
 *     - Verify that the drawer's visibility is toggled ON and its state is stored in sessionStorage.
 *
 * 6. 'toggleWikiPageMargin()':
 *     - Verify that the margin of the wiki page element is toggled RIGHT.
 *     - Verify that the margin of the wiki page element is toggled LEFT.
 *
 * 7. 'uploadPageFromEditor()':
 *     - Verify that the content from the TinyMCE editor is uploaded to the server by submitting the form.
 */
describe("Toggle Functions", function() {
    describe("toggleEditor()", function() {
        let editorContainer, myTextarea;

        beforeEach(function() {
            editorContainer = document.createElement("div");
            myTextarea = document.createElement("textarea");

            editorContainer.id = "editor-container";
            myTextarea.id = "myTextarea";

            document.body.appendChild(editorContainer);
            document.body.appendChild(myTextarea);
        });

        afterEach(function() {
            document.body.removeChild(editorContainer);
            document.body.removeChild(myTextarea);
        });

        it("toggle the editor's visibility ON and initializes TinyMCE editor accordingly", function() {
            editorContainer.style.display = "none"

            toggleEditor();

            expect(tinymce).toBeTruthy;
            expect(editorContainer.style.display).toEqual("block");
            tinymce.remove();
        });

        it("toggle the editor's visibility OFF and initializes TinyMCE editor accordingly", function() {
            editorContainer.style.display = "block"
            tinymce.init({
                selector: "#myTextarea",
                setup: function(editor) {
                    editor.on("init", function() {
                        // Set initial content for the TinyMCE editor
                        editor.setContent("<p>Testing Editor</p>");
                    });
                },
            });

            toggleEditor();

            expect(editorContainer.style.display).toEqual("none");
            expect(tinymce).toBeFalsy;
        });
    });

    describe("toggleForm()", function() {
        let uploadBox, formContainer, toggleButton;

        beforeEach(function() {
            uploadBox = document.createElement("div");
            formContainer = document.createElement("div");
            toggleButton = document.createElement("button");

            uploadBox.id = "upload-box-box";
            formContainer.id = "form-container";
            toggleButton.id = "toggleButton";

            document.body.appendChild(uploadBox);
            document.body.appendChild(formContainer);
            document.body.appendChild(toggleButton);
        });

        afterEach(function() {
            document.body.removeChild(uploadBox);
            document.body.removeChild(formContainer);
            document.body.removeChild(toggleButton);
        });

        it("toggles the form's visibility OFF and adjusts the layout accordingly", function () {
            uploadBox.style.marginTop = "200px";
            formContainer.style.display = "block";
            toggleButton.innerHTML = "Create New Page";

            toggleForm();

            expect(uploadBox.style.marginTop).toEqual("40px");
            expect(formContainer.style.display).toEqual("none");
            expect(toggleButton.innerHTML).toEqual('<img src="/static/images/back.png">');
            expect(toggleButton.classList.contains("upload-button-back")).toBeTruthy();
        });

        it("toggles the form's visibility ON and adjusts the layout accordingly", function () {
            uploadBox.style.marginTop = "40px";
            formContainer.style.display = "none";
            toggleButton.innerHTML = '<img src="/static/images/back.png">';
            toggleButton.classList.add("upload-button-back");

            toggleForm();

            expect(uploadBox.style.marginTop).toEqual("200px");
            expect(formContainer.style.display).toEqual("block");
            expect(toggleButton.innerHTML).toEqual("Create New Page");
            expect(toggleButton.classList.contains("upload-button-back")).toBeFalsy();
        });
    });

    describe("toggleSave()", function() {
        let saveContainer

        beforeEach(function() {
            saveContainer = document.createElement("div");

            saveContainer.id = "save-button-container";

            document.body.appendChild(saveContainer);
        });

        afterEach(function() {
            document.body.removeChild(saveContainer);
        });

        it("toggles the visibility of the save button container ON", function() {
            saveContainer.style.display = "none";

            toggleSave();

            expect(saveContainer.style.display).toEqual("block");
        });

        it("toggles the visibility of the save button container ON", function() {
            saveContainer.style.display = "block";

            toggleSave();

            expect(saveContainer.style.display).toEqual("none");
        });
    });

    describe("togglePage()", function() {
        let formContainer, toggleButton;

        beforeEach(function() {
            formContainer = document.createElement("div");
            toggleButton = document.createElement("button");

            formContainer.id = "page-data-container";
            toggleButton.id = "toggleButton";

            document.body.appendChild(formContainer);
            document.body.appendChild(toggleButton);
        });

        afterEach(function() {
            document.body.removeChild(formContainer);
            document.body.removeChild(toggleButton);
        });
        
        it("toggles the page data container's visibility OFF and updates the toggle button accordingly", function() {
            formContainer.style.display = "block";
            toggleButton.innerHTML = '<img src="/static/images/edit.png">';

            togglePage();

            expect(formContainer.style.display).toEqual("none");
            expect(toggleButton.innerHTML).toEqual('<img src="/static/images/back.png">');
            expect(toggleButton.getAttribute("onclick")).toEqual("verifyLeaveFunction()");
        });

        it("toggles the page data container's visibility ON and updates the toggle button accordingly", function() {
            formContainer.style.display = "none";
            toggleButton.innerHTML = '<img src="/static/images/back.png">';

            togglePage();

            expect(formContainer.style.display).toEqual("block");
            expect(toggleButton.innerHTML).toEqual('<img src="/static/images/edit.png">');
            expect(toggleButton.getAttribute("onclick")).toEqual(null);
        });
    });

    describe("toggleDrawer()", function() {
        let pageDrawer;

        beforeEach(function() {
            pageDrawer = document.createElement("div");

            pageDrawer.id = "pageDrawer";

            document.body.appendChild(pageDrawer);
        });

        afterEach(function() {
            document.body.removeChild(pageDrawer);
        });

        it("toggles the drawer's visibility OFF and stores its state in sessionStorage.", function() {
            pageDrawer.style.display = "block";
            sessionStorage.setItem("drawerOpen", "true");

            toggleDrawer();

            expect(pageDrawer.style.display).toEqual("none");
            expect(sessionStorage.getItem("drawerOpen")).toEqual("false");
        });

        it("toggles the drawer's visibility ON and stores its state in sessionStorage.", function() {
            pageDrawer.style.display = "none";
            sessionStorage.setItem("drawerOpen", "false");

            toggleDrawer();

            expect(pageDrawer.style.display).toEqual("block");
            expect(sessionStorage.getItem("drawerOpen")).toEqual("true");
        });
    });

    describe("toggleWikiPageMargin()", function() {
        let wikiPage;

        beforeEach(function() {
            wikiPage = document.createElement("div");
            wikiPage.classList.add("wiki-page");

            document.body.appendChild(wikiPage);
        });

        afterEach(function() {
            document.body.removeChild(wikiPage);
        });

        it("toggles the margin of the wiki page element RIGHT", function() {
            wikiPage.style.marginLeft = "0px";

            toggleWikiPageMargin();

            expect(wikiPage.style.marginLeft).toEqual("250px");
        });

        it("toggles the margin of the wiki page element LEFT", function() {
            wikiPage.style.marginLeft = "250px";

            toggleWikiPageMargin();

            expect(wikiPage.style.marginLeft).toEqual("0px");
        });
    });
});

describe("Upload Function - uploadPageFromEditor()", function() {
    let myTextarea, contentInput, form;

    beforeEach(function() {
        myTextarea = document.createElement("textarea");
        contentInput = document.createElement("input");
        form = document.createElement("form");

        myTextarea.id = "myTextarea";
        contentInput.id = "contentInput";

        document.body.appendChild(myTextarea);
        document.body.appendChild(contentInput);
        document.body.appendChild(form);
    
        // Initialize the TinyMCE editor
        tinymce.init({
            selector: "#myTextarea",
            setup: function(editor) {
                editor.on("init", function() {
                    // Set initial content for the TinyMCE editor
                    editor.setContent("<p>Testing Editor. Please be patient.</p>");
                });
            },
        });
    });

    afterEach(function() {
        tinymce.remove();
        document.body.removeChild(myTextarea);
        document.body.removeChild(contentInput);
        document.body.removeChild(form);
    });

    it("uploads the content from the TinyMCE editor to the server by submitting the form", function(done) {
        setTimeout(function() {
            spyOn(form, "submit");

            uploadPageFromEditor();

            expect(contentInput.value).toEqual("<p>Testing Editor. Please be patient.</p>");
            expect(form.submit).toHaveBeenCalled();

            done();
        }, 1000);
    });
});

