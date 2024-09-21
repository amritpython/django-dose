    const allInputs = document.querySelectorAll('input[type="checkbox"], input[type="radio"]');
        allInputs.forEach(input => {
            input.addEventListener('change',function(){
                if(this.checked){
                    document.getElementById('field-req-alert').style.display = 'none';
                };
            });
    });

    // Select the checkbox with class "none"
    const noneCheckbox = document.querySelector('input[type="checkbox"].none');

    // Add event listener to the "none" checkbox
    if (noneCheckbox) {
        noneCheckbox.addEventListener('change', function() {
            // Select all other checkboxes
            const otherCheckboxes = document.querySelectorAll('input[type="checkbox"]:not(.none)');
            
            // If "none" checkbox is checked, uncheck all others
            if (this.checked) {
                otherCheckboxes.forEach(checkbox => {
                    checkbox.checked = false;
                });
            }
        });
    }

    const otherCheckboxes = document.querySelectorAll('input[type="checkbox"]:not(.none)');


    otherCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            if (this.checked && noneCheckbox) {
                noneCheckbox.checked = false;
            };
        });
    });


    document.getElementById('nextBtn').addEventListener('click',function(){
        var show = false;
        var selected = false;
        const allInputs = document.querySelectorAll('input[type="checkbox"], input[type="radio"]');
        allInputs.forEach(input => {
            if (input.checked){selected=true};
        });
        if (!selected){
            document.getElementById('field-req-alert').style.display = 'flex';
            window.scrollTo(0, 0);
            return;
        };



        const modalCheckboxes = document.querySelectorAll('input[type="checkbox"].modal-input');
        modalCheckboxes.forEach(mcb => {
            if(mcb.checked && mcb.getAttribute('data-bs-target') !== ''){
                document.getElementById('show-modal-div').setAttribute('data-bs-toggle','modal');
                document.getElementById('show-modal-div').setAttribute('data-bs-target',mcb.getAttribute('data-bs-target'));
                document.getElementById('show-modal-div').click();
                show = true;
            };
        });
        const modalCheckboxes2 = document.querySelectorAll('input[type="radio"].modal-input');
        modalCheckboxes2.forEach(mcb => {
            if(mcb.checked && mcb.getAttribute('data-bs-target') !== ''){
                document.getElementById('show-modal-div').setAttribute('data-bs-toggle','modal');
                document.getElementById('show-modal-div').setAttribute('data-bs-target',mcb.getAttribute('data-bs-target'));
                document.getElementById('show-modal-div').click();
                show = true;
            };
        });
        if (!show){document.getElementsByTagName('form')[0].submit();};
    });

    // Function to set First Character Capital of each label which has no children element 
    const labels = document.querySelectorAll('label');
    labels.forEach(label => {
        if(label.children.length === 0 ){
            label.innerText = label.innerText.trimStart();
            label.innerText = label.innerText.charAt(0).toUpperCase() + label.innerText.slice(1).toLowerCase();
        };
    });

    function addToCart(){

    };



