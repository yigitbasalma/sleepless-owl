$('.form-select').select2({
  theme: "bootstrap-5",
});

$('.datetime-pick').datetimepicker({
  format: 'DD/MM/YYYY HH:mm:ss',
  icons: {
    time: "fa-solid fa-clock",
    date: "fa-solid fa-calendar",
    up: "fa-solid fa-sort-up",
    down: "fa-solid fa-sort-down",
    next: "fa-solid fa-caret-right",
    previous: "fa-solid fa-caret-left",
    today: "fa-solid fa-calendar-day",
    clear: "fa-solid fa-trash",
    close: "fa-solid fa-xmark"
  }
});