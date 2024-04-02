document.getElementById('loadCumAnalysis').addEventListener('click', function() {
    // Replace 'yourUrl' with the URL of the HTML file you want to load
    loadContent('screen_2/', 'content-container');
});

function loadContent(url, containerId) {
    fetch(url)
        .then(response => response.text())
        .then(htmlContent => {
            // Update the content of the specified container
            document.getElementById(containerId).innerHTML = htmlContent;
        })
        .catch(error => console.error('Error fetching content:', error));
}