/**
 * Test suite for the JavaScript functions used in the Tree Map application.
 *
 * This test suite covers the following functions:
 *  - myFunction(): Sets a timeout to call showPage() function after 3000 milliseconds.
 *  - showPage(): Hides the loader and shows the map container after the specified delay.
 *
 * Each function is tested using the Jasmine testing framework, with beforeEach and afterEach hooks
 * to set up and clean up the required DOM elements for each test case.
 *
 * Test Cases:
 *
 * 1. 'myFunction()':
 *     - Verify that a timeout is set to call 'showPage()' after 3000 milliseconds.
 *
 * 2. 'showPage()':
 *     - Verify that the loader is hidden and the map container is shown after the specified delay.
 */
describe("Tree Map Functions", function () {
    let loader, myDiv;

    beforeEach(function () {
        jasmine.clock().install();

        loader = document.createElement("div");
        myDiv = document.createElement("div");

        loader.id = "loader";
        myDiv.id = "myDiv";

        document.body.appendChild(loader);
        document.body.appendChild(myDiv);
    });

    afterEach(function () {
        try {
            document.body.removeChild(loader);
            document.body.removeChild(myDiv);
        } catch (error) {
            // Do nothing if the element is not found
        }
        jasmine.clock().uninstall();
    });

    describe("myFunction()", function () {
        it("sets a timeout to call showPage function after 3000 milliseconds", function () {
            myFunction();
            jasmine.clock().tick(3100); // Slightly more than 3000ms to give showPage() time to execute

            expect(loader.style.display).toEqual("none");
            expect(myDiv.style.display).toEqual("block");
        });
    });

    describe("showPage()", function () {
        it("hides the loader and shows the map container after the specified delay", function () {
            loader.style.display = "block";
            myDiv.style.display = "none";

            myFunction();
            jasmine.clock().tick(3100); // Slightly more than 3000ms to give showPage() time to execute

            showPage();
            expect(loader.style.display).toEqual("none");
            expect(myDiv.style.display).toEqual("block");
        });
    });
});
