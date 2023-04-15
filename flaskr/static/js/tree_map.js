/**
 * @fileoverview This script provides functionality for displaying a tree distribution map on a web page.
 * It includes a loader and a function to show the map after a specified delay.
 */

/**
 * Global variable for the timeout.
 * @type {number}
 */
let myVar;

/**
 * Set a timeout to delay showing the map.
 */
function myFunction() {
  // Set the timeout to call the showPage function after 3000 milliseconds (3 seconds)
  myVar = setTimeout(showPage, 3000);
}

/**
 * Show the map and hide the loader after the specified delay.
 */
function showPage() {
  // Hide the loader element
  document.getElementById('loader').style.display = 'none';

  // Show the map container (myDiv) element
  document.getElementById('myDiv').style.display = 'block';
}