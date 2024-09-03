document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('upload-form');
    const resultsDiv = document.getElementById('results');
    const errorDiv = document.getElementById('error-message');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(form);
        
        fetch('/analyze', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            displayResults(data);
        })
        .catch(error => {
            errorDiv.textContent = error.message;
            errorDiv.style.display = 'block';
            resultsDiv.style.display = 'none';
        });
    });

    function displayResults(data) {
        const matchingSkillsDiv = document.getElementById('matching-skills');
        const missingSkillsDiv = document.getElementById('missing-skills');
        const recommendationsDiv = document.getElementById('recommendations');

        matchingSkillsDiv.innerHTML = `<h3>Matching Skills:</h3><p>${data.matching_skills.join(', ') || 'None found'}</p>`;
        missingSkillsDiv.innerHTML = `<h3>Missing Skills:</h3><p>${data.missing_skills.join(', ') || 'None found'}</p>`;
        
        let recommendationsHtml = '<h3>Recommendations:</h3><ul>';
        data.recommendations.forEach(rec => {
            recommendationsHtml += `<li>${rec}</li>`;
        });
        recommendationsHtml += '</ul>';
        recommendationsDiv.innerHTML = recommendationsHtml;

        resultsDiv.style.display = 'block';
        errorDiv.style.display = 'none';
    }
});