let chart;

$('#monitors').on('shown.bs.collapse', function () {
  var taskID = $('.show input.task-id').val();

  // Main chart
  $.ajax({
    type: 'GET',
    url: '/agents/metrics/for-charts/' + taskID,
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
      const ctx = document.getElementById('chart-' + taskID);
      chart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: data.data.labels,
          datasets: data.data.datasets
        },
        options: {
          scales: {
            y: {
              beginAtZero: true,
              max: data.data.max
            },
            x: {
              type: 'time',
              time: {
                displayFormats: {
                    quarter: 'MMM YYYY'
                }
              }
            }
          }
        }
      });
    }
  });

  // Widget chart
  $.ajax({
    type: 'GET',
    url: '/agents/metrics/for-widget/' + taskID,
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
      document.getElementById('current-response-time-' + taskID).innerHTML = data.data.avg_30_min + '/s';
      document.getElementById('day-response-time-' + taskID).innerHTML = data.data.avg_24_hour + '/s';
      document.getElementById('day-uptime-' + taskID).innerHTML = data.data.uptime_24_hours + '%';
      document.getElementById('month-uptime-' + taskID).innerHTML = data.data.uptime_30_day + '%';
    }
  });
});

$('#monitors').on('hidden.bs.collapse', function () {
  chart.destroy();
});

$('.form-select').select2({
    theme: "bootstrap-5",
});

function refreshData(period, title) {
  var taskID = $('.show input.task-id').val();

  // Main chart
  $.ajax({
    type: 'GET',
    url: '/agents/metrics/for-charts/' + taskID + '?period=' + period,
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
      document.getElementById('chart-title-' + taskID).innerHTML = title;
      chart.destroy();
      const ctx = document.getElementById('chart-' + taskID);
      chart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: data.data.labels,
          datasets: data.data.datasets
        },
        options: {
          scales: {
            y: {
              beginAtZero: true,
              max: data.data.max
            },
            x: {
              type: 'time',
              time: {
                displayFormats: {
                    quarter: 'MMM YYYY'
                }
              }
            }
          }
        }
      });
    }
  });

  // Widget chart
  $.ajax({
    type: 'GET',
    url: '/agents/metrics/for-widget/' + taskID,
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
      document.getElementById('current-response-time-' + taskID).innerHTML = data.data.avg_30_min + '/s';
      document.getElementById('day-response-time-' + taskID).innerHTML = data.data.avg_24_hour + '/s';
      document.getElementById('day-uptime-' + taskID).innerHTML = data.data.uptime_24_hours + '%';
      document.getElementById('month-uptime-' + taskID).innerHTML = data.data.uptime_30_day + '%';
    }
  });
}

var socket = io();
socket.on('connect', function() {
    socket.emit('Task States');
});

socket.on('summaries', function(rsp) {
    var taskStatuses = {unknown: "btn-secondary", up: "btn-success", down: "btn-danger", partial: "btn-warning"};
    var certStatuses = {unknown: "btn-secondary", valid: "btn-success", expired: "btn-danger"};
    $.each( rsp, function( index, value ) {
      // Set task status
      var taskStatusObject = document.getElementById('task-status-' + value.id);
      $(taskStatusObject).removeClass(function (index, className) {
        return (className.match(/(^|\s)btn-\S+/g) || []).join(' ');
      });
      $(taskStatusObject).addClass(taskStatuses[value.status]);
      $(taskStatusObject).text(value.status);

      // Set ssl-cert status
      if ( value.cert_valid_until != "" ) {
        var certStatusObject = document.getElementById('cert-status-' + value.id);
        $(certStatusObject).removeClass(function (index, className) {
          return (className.match(/(^|\s)btn-\S+/g) || []).join(' ');
        });
        $(certStatusObject).addClass(certStatuses[value.cert_valid]);
        $(certStatusObject).attr('data-original-title', 'Cert valid until ' + value.cert_valid_until);
        $(certStatusObject).text(value.cert_valid);
      }

      // Set agent success ratio
      var agentSuccessRatioObject = document.getElementById('agent-success-ratio-' + value.id);
      agentSuccessRatioObject.style.cssText = "position: relative; top: -40%; float: right;background: radial-gradient(closest-side, white 79%, transparent 80% 100%), conic-gradient(green " + value.task_state_percent + "%, red 0);"
      if ( value.task_state_percent != 100 ) {
        $(agentSuccessRatioObject).attr('data-original-title', 'Some of agents are failing.');
      } else {
        $(agentSuccessRatioObject).attr('data-original-title', 'All agents up & running.');
      }

      // Set maintenance status
      var maintenanceStatusObject = document.getElementById('maintenance-status-' + value.id);
      if ( value.in_maintenance ) {
        $(maintenanceStatusObject).attr('data-original-title', 'Task in maintenance from ' + value.maintenance_since + ' to ' + value.maintenance_until + '.');
        $(maintenanceStatusObject).removeAttr('hidden');
      } else {
        $(maintenanceStatusObject).attr('hidden', '');
      }
    });
});

function edit_http_task(taskID) {
  $.ajax({
    type: 'GET',
    url: '/tasks/' + taskID,
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
      document.getElementById('edit-http-task-header').innerHTML = data.task.name;
      document.getElementById('name-1').value = data.task.name;
      document.getElementById('username-1').value = data.task.username;
      document.getElementById('password-1').value = data.task.password;
      document.getElementById('return_codes-1').value = data.task.return_codes;
      document.getElementById('period-1').value = data.task.period;
      document.getElementById('url-1').value = data.task.url;
      document.getElementById('headers-1').value = data.task.headers;
      document.getElementById('data-1').value = data.task.data;
      document.getElementById('editHttpTaskForm').action = '/tasks/http/' + taskID + '/update';
      $('#agents-1').val(data.agents).change();
      $('#editHttpTask').modal('show');
    }
  });
}

function edit_tcp_task(taskID) {
  $.ajax({
    type: 'GET',
    url: '/tasks/' + taskID,
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
      document.getElementById('edit-tcp-task-header').innerHTML = data.task.name;
      document.getElementById('name-3').value = data.task.name;
      document.getElementById('period-3').value = data.task.period;
      document.getElementById('ip_address-3').value = data.task.ip_address;
      document.getElementById('port-3').value = data.task.port;
      document.getElementById('editTCPTaskForm').action = '/tasks/tcp/' + taskID + '/update';
      $('#agents-3').val(data.agents).change();
      $('#editTCPTask').modal('show')
    }
  });
}

function task_logs(taskID) {
  $.ajax({
    type: 'GET',
    url: '/tasks/' + taskID + '/logs',
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
      document.getElementById('task-logs-header').innerHTML = data.name;
      var logsTable = document.getElementById('task-logs-table').getElementsByTagName('tbody')[0];
      while( logsTable.hasChildNodes() ) {
         logsTable.removeChild(logsTable.firstChild);
      }
      if ( data.logs.length > 0 ){
        $.each( data.logs, function( l_index, l_value ) {
          var row = logsTable.insertRow(0);
          var agentNameCell = row.insertCell(0);
          var createdAtCell = row.insertCell(1);
          var taskLogCell = row.insertCell(2);

          agentNameCell.innerHTML = l_value.agent;
          createdAtCell.innerHTML = l_value.created_at;
          taskLogCell.innerHTML = l_value.log;
        });
      } else {
        var row = logsTable.insertRow(0);
        var noLogFoundCell = row.insertCell(0);

        noLogFoundCell.innerHTML = 'No logs found';
        noLogFoundCell.colSpan = 3;
        noLogFoundCell.style.textAlign = 'center';
      }
      $('#taskLogs').modal('show')
    }
  });
}