document.addEventListener('DOMContentLoaded', function (e) {
  (function () {
    const formNewUser = document.querySelector('#newUserForm');

    // Form validation for Change password
    if (formNewUser) {
      const fv = FormValidation.formValidation(formNewUser, {
        fields: {
          first_name: {
            validators: {
              notEmpty: {
                message: 'Please enter your first name'
              },
              stringLength: {
                min: 3,
                max: 64,
                message: 'First name length must be between 3 and 64 characters'
              }
            }
          },
          last_name: {
            validators: {
              notEmpty: {
                message: 'Please enter your last name'
              },
              stringLength: {
                min: 3,
                max: 64,
                message: 'Last name length must be between 3 and 64 characters'
              }
            }
          },
          email: {
            validators: {
              notEmpty: {
                message: 'Please enter your business email'
              },
              emailAddress: {
                message: 'Please enter valid email address'
              }
            }
          },
          password: {
            validators: {
              notEmpty: {
                message: 'Please enter password'
              },
              stringLength: {
                min: 8,
                max: 64,
                message: 'Password length must be between 8 and 64 characters'
              }
            }
          },
          confirm_password: {
            validators: {
              notEmpty: {
                message: 'Confirm Password is required'
              },
              identical: {
                compare: function () {
                  return formNewUser.querySelector('[name="password"]').value;
                },
                message: 'The password and its confirm are not the same'
              }
            }
          }
        },
        plugins: {
          trigger: new FormValidation.plugins.Trigger(),
          bootstrap5: new FormValidation.plugins.Bootstrap5({
            eleValidClass: '',
            rowSelector: function(field, ele) {
                switch (field) {
                    case 'email':
                        return '.col-12';

                    default:
                        return '.col-6';
                }
            }
          }),
          submitButton: new FormValidation.plugins.SubmitButton(),
          // Submit the form when all fields are valid
          // defaultSubmit: new FormValidation.plugins.DefaultSubmit(),
          autoFocus: new FormValidation.plugins.AutoFocus()
        },
        init: instance => {
          instance.on('plugins.message.placed', function (e) {
            if (e.element.parentElement.classList.contains('input-group')) {
              e.element.parentElement.insertAdjacentElement('afterend', e.messageElement);
            }
          });
        }
      }).on('core.form.valid', function() {
        // Send the form data to back-end
        // You need to grab the form data and create an Ajax request to send them

        request(formNewUser.method, formNewUser.action, $('#' + formNewUser.id).serialize())
      });
    }
  })();
});