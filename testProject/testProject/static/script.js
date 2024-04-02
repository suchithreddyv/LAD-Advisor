var activeContainerId = null;
var prevNormalSrc = null;  // Variable to store the normal source of the previously active button

function changeColor(containerId, textClass, iconClass) {
    var iconContainer = document.getElementById(containerId);

    // Check if the button is currently active
    var isCurrentlyActive = iconContainer.classList.contains('active');

    // Deactivate the previously active button
    if (activeContainerId !== null && activeContainerId !== containerId) {
        removeActiveState(activeContainerId, textClass, iconClass, prevNormalSrc);
    }

    // Toggle the state of the current button if it's not currently active
    if (!isCurrentlyActive) {
        var isActive = iconContainer.classList.toggle('active');

        // Toggle between normal and active states using data attribute
        var icon = iconContainer.querySelector('.' + iconClass);
        var normalSrc = icon.getAttribute('src');
        var activeSrc = icon.getAttribute('data-active-src');
        
        // Update the image source based on the active state
        icon.src = isActive ? activeSrc : normalSrc;

        // Store the normal source of the currently active button
        if (isActive) {
            prevNormalSrc = normalSrc;
        }

        // Toggle the active class for text elements
        var textElements = iconContainer.getElementsByClassName(textClass);
        for (var i = 0; i < textElements.length; i++) {
            textElements[i].classList.toggle('active', isActive);
        }

        // Update the activeContainerId
        activeContainerId = isActive ? containerId : null;
    }
}

function removeActiveState(containerId, textClass, iconClass, normalSrc) {
    var iconContainer = document.getElementById(containerId);
    iconContainer.classList.remove('active');

    // Toggle between normal and active states using data attribute
    var icon = iconContainer.querySelector('.' + iconClass);
    
    // Set the image source to the stored normal source
    icon.src = normalSrc;

    // Remove the active class for text elements
    var textElements = iconContainer.getElementsByClassName(textClass);
    for (var i = 0; i < textElements.length; i++) {
        textElements[i].classList.remove('active');
    }
}

document.getElementById('backButton').addEventListener('click', function() {
    window.history.back(); 
});


// document.getElementById('loadadvising').addEventListener('click', function() {
//     // Replace 'yourUrl' with the URL of the HTML file you want to load
//     loadContent('screen_1/', 'content-container');
// });

// // Function to load content
// function loadContent(url, containerId) {
//     fetch(url)
//         .then(response => response.text())
//         .then(htmlContent => {
//             // Update the content of the specified container
//             document.getElementById(containerId).innerHTML = htmlContent;
//         })
//         .catch(error => console.error('Error fetching content:', error));
// }

// Function to filter student table rows
function filterStudentTable(searchQuery) {
    var rows = document.querySelectorAll('.studenttable tbody tr');
    rows.forEach(function(row) {
        var studentName = row.querySelector('td:first-child').textContent.toLowerCase();
        if (studentName.includes(searchQuery)) {
            row.style.display = 'table-row'; // Show the row
        } else {
            row.style.display = 'none'; // Hide the row
        }
    });
}

// Event listener for form submission
document.getElementById('searchForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission
    var searchQuery = document.getElementById('searchField').value.toLowerCase();
    filterStudentTable(searchQuery);
});

// Event listener for clear filter button
document.getElementById('clearFilterButton').addEventListener('click', function() {
    document.getElementById('searchField').value = ''; // Clear the search field
    filterStudentTable(''); // Reset the filter
});

function filterAssignments() {
    var selectedCategory = document.getElementById("category").value;
    var categories = document.querySelectorAll(".assignment-category");
    var table = document.getElementById("assignmentTable");
    var viewSelect = document.getElementById("view-select");

    categories.forEach(function(category) {
        if (category.id === selectedCategory) {
            category.style.display = "block";
        } else {
            category.style.display = "none";
        }
    });

    // Show the table if a category is selected
    if (selectedCategory !== "Select a Category") {
        table.style.display = "table";

        // Hide assignments not belonging to the selected category
        var assignmentItems = document.querySelectorAll(".assignment-item");
        assignmentItems.forEach(function(item) {
            if (item.dataset.category === selectedCategory) {
                item.style.display = "table-row";
            } else {
                item.style.display = "none";
            }
        });

        if (viewSelect.value === "graphical") {
            renderChart(selectedCategory);
        }

    } else {
        table.style.display = "none";
        viewSelect.value = "empty";
        toggleView();
    }
}

function toggleView() {
    var selectedView = document.getElementById("view-select").value;
    var tableView = document.getElementById("table-view");
    var graphicalView = document.getElementById("graphical-view");

    if (selectedView === "table") {
        tableView.style.display = "block";
        graphicalView.style.display = "none";
    } else if (selectedView === "graphical") {
        tableView.style.display = "none";
        graphicalView.style.display = "block";
        // Get the selected category
        var selectedCategory = document.getElementById("category").value;
        if (selectedCategory !== "Select a Category") {
            renderChart(selectedCategory);
        }
    }
    else{
        tableView.style.display = "none";
        graphicalView.style.display = "none";
    }
}

