
let profileEditForm = document.getElementById('profile-edit-form');
let profileSettingsForm = document.getElementById('profile-settings-form');
let profileChangePasswordForm = document.getElementById('profile-change-password-form');
let profileImageUploadForm = document.getElementById('profile-image-upload-form');

// alert div 
let alertDiv = document.querySelector('.alert-div');
let alertStatus = alertDiv.querySelector('.status');
let alertMessage = alertDiv.querySelector('.message');


profileEditForm.addEventListener('submit', (e) => {
  e.preventDefault();
 
  uploadFormData(profileEditForm, '/admin/profile/edit/', 'POST'); 


}); 

profileChangePasswordForm.addEventListener('submit', (e) => {
    e.preventDefault();
    uploadFormData(profileChangePasswordForm, '/admin/profile/change-password/', 'POST');
});  

profileImageUploadForm.addEventListener('submit', (e) => {
    e.preventDefault();
    let image = profileImageUploadForm.querySelector('input[type="file"]').files[0];
    let modal = document.querySelector('#profileImageModal');

    let loader = modal.querySelector('.profile-upload-loader');
    let alert = modal.querySelector('.alert');

    let dismissBtn = modal.querySelector('[data-bs-dismiss="modal"]');
    if (image) { 
        loader.removeAttribute('hidden');
        // hidding the  profile image upload form
        profileImageUploadForm.style.display = 'none';

         uploadFormData(profileImageUploadForm, '/admin/profile/change-image/', 'POST', callback);
    }
    function callback(status, response){
        if (status == 200) {
            if (response.status == 'success') {
              //  add a hidden attribute to the loader div
              loader.setAttribute('hidden', true);
              //  show success message  inside alert div
              alert.classList.remove('d-none');
              alert.classList.remove('alert-danger')
              alert.classList.add('alert-success');
              alert.innerHTML = response.message;
                setTimeout(() => {
                     dismissBtn.click();
                     window.location.reload();
                }, 1500);
            }else{
                loader.setAttribute('hidden', true);
                alert.classList.remove('d-none');
                alert.classList.add('alert-danger');
                alert.innerHTML = response.message; 
                profileImageUploadForm.style.display = 'block';

            }
        }else{
            loader.setAttribute('hidden', true);
            alert.classList.remove('d-none');
            alert.classList.add('alert-danger');
            alert.innerHTML = response.message;

            // window.location.reload();
        }
    }

});







function uploadFormData(form, url, method ,  callback=null) {
    let formData = new FormData(form);
    let xhr = new XMLHttpRequest(); 
    // xhr.timeout = 8000; // 8 seconds timeout to prevent hanging requests
    xhr.open(method, url);
    if (callback != null){
        xhr.onload = () =>{
          var response;
          if (xhr.status == 200){
             response = JSON.parse(xhr.response);

          }else{
            response = {status: 'error', message: 'Something went wrong please try again later'};
          }
          callback(xhr.status , response); 
        }
        xhr.onerror = () => {
          callback(xhr.status , {status: 'error', message: 'connection failure please try again later'});
        }
        xhr.ontimeout = () => {
          callback(xhr.status , {status: 'error', message: 'Connection timed out please try again later'});
        }
    }
    else {
          scrollTo(0, 0); 
          LOADER.classList.add('active');
          xhr.onload = () => {
            alertDiv.classList.remove('d-none');
            if (xhr.status == 200) {
              let response = JSON.parse(xhr.response); 
              if (response.status == 'success') {
                  alertDiv.classList.remove('alert-danger')
                  alertDiv.classList.add('alert-success');
                  alertStatus.innerHTML = 'Success';
                  alertMessage.innerHTML = response.message; 

                  LOADER.classList.remove('active');

                  // REFRESING THE PAGE TO REFLECT CHANGES
                  setTimeout(() => {
                    window.location.reload();
                  }, 4500);

              }else{
                  alertDiv.classList.add('alert-danger');
                  alertStatus.innerHTML = response.status;
                  alertMessage.innerHTML = response.message;
              }
              setTimeout(() => {
              // hide alert div
                //  alertDiv.style.display = 'none';
                LOADER.classList.remove('active');
              }, 3000);
            }else{
              alertDiv.classList.add('alert-danger');
              alertStatus.innerHTML = 'Error '+xhr.status;
              alertMessage.innerHTML = 'Something went wrong please try again  later ';
            }
          }
          // if xhr fails to load
          xhr.onerror = () => {
            alertDiv.classList.remove('d-none');
            alertDiv.classList.add('alert-danger');
            alertStatus.innerHTML = 'Error '+xhr.status;
            alertMessage.innerHTML = 'Connection failure please try again  later';
            setTimeout(() => {
                LOADER.classList.remove('active');
              }, 3000);
          }
          // if xhr loads for so  long
          xhr.ontimeout = () => {
            alertDiv.classList.remove('d-none');
            alertDiv.classList.add('alert-danger');
            alertStatus.innerHTML = 'Error ';
            alertMessage.innerHTML = 'Connection timed out please try again';
            setTimeout(() => {
              // hide alert div
                //  alertDiv.style.display = 'none';
                LOADER.classList.remove('active');
              }, 3000);
          }
    }
    xhr.send(formData);
  }