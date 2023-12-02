function formatProvider(provider) {
  if (!provider.id) {
    return provider.text;
  }
  console.log(provider);
  var baseUrl = "/static/images/providers";
  var $provider = $(
    '<span><img height="30" width="30" src="' + baseUrl + '/' + provider.element.dataset.img.toLowerCase() + '.png" class="img-flag" /> ' + provider.text + '</span>'
  );
  return $provider;
};

$('.form-select').select2({
    theme: "bootstrap-5",
    templateResult: formatProvider
});

$('.form-select-without-img').select2({
    theme: "bootstrap-5"
});

function update_provider(providerID, name, config) {
  document.getElementById('edit-provider-header').innerHTML = name;
  document.getElementById('name-1').value = name;
  document.getElementById('config-1').innerHTML = config;
  document.getElementById('editProviderForm').action = '/notification/provider/' + providerID + '/update';
  $('#updateProvider').modal('show');
}

function update_rule(ruleID, name, config, tasks) {
  document.getElementById('edit-rule-header').innerHTML = name;
  document.getElementById('name-2').value = name;
  $('#tasks-2').val(JSON.parse(tasks)).change();
  document.getElementById('config-2').innerHTML = config;
  document.getElementById('editRuleForm').action = '/notification/rule/' + ruleID + '/update';
  $('#updateRule').modal('show');
}