function capitalize(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

$('.copy-clipboard').on('click', function (e) {
    navigator.clipboard.writeText(this.innerHTML);

    Toastify({
      text: "Copied!",
      className: "info",
      style: {
        background: "white",
        border: "solid white 2px",
        "border-radius": "10px",
        "font-weight": "bold",
        color: "green"
      }
    }).showToast();
});

function request(method, action, data) {
    $.ajax({
        type: method,
        url: action,
        data: data,
        beforeSend: function () {
            $.blockUI({
                message: '<div class="spinner-border text-primary" role="status"></div>',
                css: {
                  backgroundColor: 'transparent',
                  border: '0'
                },
                overlayCSS: {
                  backgroundColor: '#fff',
                  opacity: 0.8
                }
            });
        },
        complete: function () {
             $.unblockUI();
        },
        success: function (data) {
            if (data.message) {
                if ( !action.startsWith('/auth/') ) {
                    Swal.fire({
                      icon: data.status,
                      title: capitalize(data.status),
                      text: data.message,
                      showConfirmButton: false,
                      timer: (data.status == 'error') ? 25000 : 2000
                    })
                }

                if (data.status == 'error') {
                    Swal.fire({
                      icon: data.status,
                      title: capitalize(data.status),
                      text: data.message,
                      showConfirmButton: false,
                      timer: (data.status == 'error') ? 25000 : 2000
                    })
                }

                setTimeout(function(){
                    if (data.refresh) {
                        location.reload(true);
                    } else if (data.redirect) {
                        window.location.replace(data.redirect);
                    }
                }, 2000);
            }
        }
    });
}

$('form').on('submit', function (e) {
    e.preventDefault();
    var form = $(this);
    var form_data = new FormData(this);
    $.ajax({
        type: form[0].method,
        url: form[0].action,
        data: form_data,
        contentType: false,
        processData: false,
        beforeSend: function () {
            $.blockUI({
                message: '<div class="spinner-border text-primary" role="status"></div>',
                css: {
                  backgroundColor: 'transparent',
                  border: '0'
                },
                overlayCSS: {
                  backgroundColor: '#fff',
                  opacity: 0.8
                }
            });
        },
        complete: function () {
             $.unblockUI();
        },
        statusCode: {
          401: function (data) {
            Swal.fire({
              icon: "error",
              title: "Unauthorized Action",
              text: "You have no privilege for this operation",
              showConfirmButton: false,
              timer: 25000
            })
          }
        },
        success: function (data) {
            if (data.message) {
                if ( !form[0].action.startsWith('/auth/') ) {
                    Swal.fire({
                      icon: data.status,
                      title: capitalize(data.status),
                      text: data.message,
                      showConfirmButton: false,
                      timer: (data.status == 'error') ? 25000 : 2000
                    })
                }

                if (data.status == 'error') {
                    Swal.fire({
                      icon: data.status,
                      title: capitalize(data.status),
                      text: data.message,
                      showConfirmButton: false,
                      timer: (data.status == 'error') ? 25000 : 2000
                    })
                }

                setTimeout(function(){
                    if (data.refresh) {
                        location.reload(true);
                    } else if (data.redirect) {
                        window.location.replace(data.redirect);
                    }
                }, 2000);
            }
        }
    });
});

function delete_object(method, url, data=null) {
    Swal.fire({
      title: 'Do you want to remove the object?',
      showCancelButton: true,
      confirmButtonText: `Remove`,
      confirmButtonColor: "#dc3545"
    }).then((result) => {
      if (result.isConfirmed) {
        $.ajax({
            type: method,
            url: url,
            data: data,
            beforeSend: function () {
                $.blockUI({
                    message: '<div class="spinner-border text-primary" role="status"></div>',
                    css: {
                      backgroundColor: 'transparent',
                      border: '0'
                    },
                    overlayCSS: {
                      backgroundColor: '#fff',
                      opacity: 0.8
                    }
                  });
            },
            complete: function () {
                 $.unblockUI();
            },
            statusCode: {
              401: function (data) {
                Swal.fire({
                  icon: "error",
                  title: "Unauthorized Action",
                  text: "You have no privilege for this operation",
                  showConfirmButton: false,
                  timer: 25000
                })
              }
            },
            success: function (data) {
                if (data.message) {
                    Swal.fire({
                      icon: data.status,
                      title: capitalize(data.status),
                      text: data.message,
                      showConfirmButton: false,
                      timer: (data.status == 'error') ? 25000 : 2000
                    })

                    setTimeout(function(){
                        if (data.refresh) {
                            location.reload(true);
                        } else if (data.redirect) {
                            window.location.replace(data.redirect);
                        }
                    }, 2000);
                }
            }
        });
      }
    })
}

function call_ajax(url, method) {
    $.ajax({
        type: method,
        url: url,
        beforeSend: function () {
            $.blockUI({
                message: '<div class="spinner-border text-primary" role="status"></div>',
                css: {
                  backgroundColor: 'transparent',
                  border: '0'
                },
                overlayCSS: {
                  backgroundColor: '#fff',
                  opacity: 0.8
                }
              });
        },
        complete: function () {
             $.unblockUI();
        },
        success: function (data) {
            if (data.message) {
                setTimeout(function(){
                    if (data.refresh) {
                        location.reload(true);
                    } else if (data.redirect) {
                        window.location.replace(data.redirect);
                    }
                }, 500);
            }
        }
    });
}

$("option").each(function(){
  if ($(this).val().toLowerCase() == "-1") {
    $(this).attr("disabled", "disabled");
  }
});

$(function () {
  $('[data-toggle="tooltip"]').tooltip();
})