const emailInput = document.getElementById('resident-email');
const cnicInput = document.getElementById('self-cnic-number');
const ownercnicInput = document.getElementById('owner-cnic-number');
const flatnumberInput = document.getElementById('flat-number');
const cnicerrorMessage = document.getElementById('cnic-error-message');
const ownercnicerrorMessage = document.getElementById('owner-cnic-error-message');
const flatnumbererrorMessage = document.getElementById('flat-number-error-message');
const emailInputerrorMessage = document.getElementById('email-error-message');

cnicInput.addEventListener('input', async () => {
  const response = await fetch(`/check_cnic/${cnicInput.value}`);
  const result = await response.json();
  if (result.error) {
    cnicerrorMessage.textContent = result.error;
  } else {
    cnicerrorMessage.textContent = '';
  }
});

emailInput.addEventListener('input', async () => {
    const response = await fetch(`/check_email/${emailInput.value}`);
    const result = await response.json();
    if (result.error) {
      emailInputerrorMessage.textContent = result.error;
    } else {
        emailInputerrorMessage.textContent = '';
    }
  });

ownercnicInput.addEventListener('input', async () => {
    const response = await fetch(`/owner_check_cnic/${ownercnicInput.value}`);
    const result = await response.json();
    if (result.error) {
        ownercnicerrorMessage.textContent = result.error;
    } else {
        ownercnicerrorMessage.textContent = '';
    }
  });
  
  flatnumberInput.addEventListener('input', async () => {
    const response = await fetch(`/check_flat_number/${flatnumberInput.value}`);
    const result = await response.json();
    if (result.error) {
        flatnumbererrorMessage.textContent = result.error;
    } else {
        flatnumbererrorMessage.textContent = '';
    }
  });
  
  flatnumberInput.addEventListener('input', async (event) => {
    const flatNumber = event.target.value;
    const ownerCnic = ownercnicInput.value;
    const response = await fetch('/check_flat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            flat_number: flatNumber,
            owner_cnic_number: ownerCnic
        })
    });
    const data = await response.json();
    const errorMessage = document.getElementById('flat-error-message');
    
    if (data.success) {
        errorMessage.innerText = '';
    } else {
        errorMessage.innerText = 'Incorrect Match: owner cnic and flat number';
    }
});

flatnumberInput.addEventListener('input', async (event) => {
    const flatNumber = event.target.value;
    const ownerCnic = ownercnicInput.value;
    const response = await fetch('/check_max_residents', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            flat_number: flatNumber,
            owner_cnic_number: ownerCnic
        })
    });
    const data = await response.json();
    const errorMessage = document.getElementById('resident-error-message');
    
    if (data.success) {
        errorMessage.innerText = '';
    } else {
        errorMessage.innerText = data.message;
    }
});

