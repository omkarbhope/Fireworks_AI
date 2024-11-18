document.addEventListener('DOMContentLoaded', function() {
    // Function to switch from the welcome screen to the user details form.
    function goToDetails() {
        document.getElementById('welcome').style.display = 'none';
        document.getElementById('user-details').style.display = 'block';
        console.log("Switched to user details form.");
    }

    // Event listener for the 'Continue' button.
    document.getElementById('continue-button').addEventListener('click', goToDetails);

    // Function to handle form submission.
    function handleFormSubmit(event) {
        event.preventDefault(); // Prevent default form submission.
        console.log("Form submission started.");
        
        simulateLoading(); // Start the loading simulation.

        // Hide user details form and show processing indicator.
        document.getElementById('user-details').style.display = 'none';
        document.getElementById('processing').style.display = 'block';
        console.log("Processing screen is now visible.");

        // Prepare FormData object from the form.
        const formData = new FormData(event.target);
        console.log("Form Data Prepared for Submission:", Array.from(formData.entries()));

        // Perform the POST request to the FastAPI backend.
        fetch('http://127.0.0.1:8000/verify_identity/', {
            method: 'POST',
            body: formData,
        })
        .then(response => {
            console.log("Response received.");
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
            return response.json(); // Convert the response to JSON.
        })
        .then(data => {
            console.log("Data Received from Server:", data);
            // Hide processing screen and display results section.
            document.getElementById('processing').style.display = 'none';
            document.getElementById('results').style.display = 'block';
            // Display the verification result.
            // document.getElementById('verification-result').textContent = JSON.stringify(data, null, 2);
            displayResults(data);
            console.log("Results should now be visible.");
        })
        .catch(error => {
            console.error('Error:', error);
            // Handle errors by hiding processing and results section, show error message.
            document.getElementById('processing').style.display = 'none';
            document.getElementById('results').style.display = 'none';
            alert('Failed to verify identity. See console for details.');
        });
    }

    function displayResults(data) {
        const resultContainer = document.getElementById('result-container'); // Change the target container ID
        resultContainer.innerHTML = ''; // Clear previous results
    
        const card = document.createElement('div');
        card.className = 'card mx-auto';
        card.style.maxWidth = '18rem';
    
        let cardHeaderClass = 'card-header';
        let cardHeaderText = 'Verification Details';
        let cardBodyText = `
            <strong>Document Type:</strong> ${data.document_type}<br>
            <strong>Document Number:</strong> ${data.document_number}<br>
            <strong>Name:</strong> ${data.name}<br>
            <strong>Sex:</strong> ${data.sex}<br>
            <strong>Date of Birth:</strong> ${data.dob}<br>
            <strong>Expiry Date:</strong> ${data.expiry_date}<br>
            <strong>Address:</strong> ${data.address}
        `;
    
        if (data.error === "Invalid dates: Verification failed") {
            cardHeaderClass += ' bg-danger text-white';
            cardHeaderText = 'Error';
            cardBodyText = `<br><strong>Error:</strong> ${data.error}`;
            console.log("Accessed the error function");
        } 
        else if (data.error === "Date parsing failed: Verification failed" || data.error === "Expired document: Verification failed") {
            cardHeaderClass += ' bg-danger text-white';
            cardHeaderText = 'Error';
            cardBodyText += `<br><strong>Error:</strong> ${data.error}`;
            console.log("Accessed the error function");
        }
        else {
            cardHeaderClass += ' bg-success text-white';
        }
    
        card.innerHTML = `
            <div class="${cardHeaderClass}">${cardHeaderText}</div>
            <div class="card-body">
                <p class="card-text">${cardBodyText}</p>
            </div>
        `;
    
        resultContainer.appendChild(card);  // Append the new card to the new container
        document.getElementById('results').style.display = 'block';
    }

    function simulateLoading() {
        const loaderContainer = document.querySelector('.loader-container');
        const loaderBar = document.querySelector('.loader-bar');
        let width = 0;
        loaderContainer.classList.remove('hidden');
        
        intervalId = setInterval(() => {
            if (width < 90) { // Increment width till 90% to leave room for final data processing
                width += 1;
                loaderBar.style.width = width + '%';
            }
        }, 200);
    }
    
    

    // Add event listener to the form for handling submissions.
    document.getElementById('verification-form').addEventListener('submit', handleFormSubmit);

    // Function to reset the UI and form to initial state.
    function resetForm() {
        console.log("Resetting form and UI.");
        document.getElementById('verification-form').reset();
        document.getElementById('results').style.display = 'none';
        document.getElementById('welcome').style.display = 'block';
    }

    // Add event listener to the 'Verify Another' button for resetting the form.
    document.getElementById('reset-button').addEventListener('click', resetForm);
});
