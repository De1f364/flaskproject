// custom javascript

$( document ).ready(function() {
    let fieldNum = 0;
    let fieldNumApp = 0
        $("#add-address").click(function() {
          $('<div>').attr({
            class: 'form-group',
            id: 'form-group-' + fieldNum
          }).appendTo('.addr-form')
          $('<input>').attr({
            class: 'form-control',
            type: 'text',
            id: 'addresses-' + fieldNum,
            name: 'addresses-' + fieldNum,
          }).appendTo('#form-group-' + fieldNum);
          fieldNum++
        });
        
        $("#remove-address").click(function () {
          if (fieldNum > 0) {
            $("#form-group-" + (fieldNum - 1)).remove()
            fieldNum--
          }
        });

        $("#add-app").click(function() {
          $('<div>').attr({
            class: 'form-group',
            id: 'form-group-' + fieldNumApp
          }).appendTo('.app-form')
          $('<input>').attr({
            class: 'form-control',
            type: 'text',
            id: 'addresses-' + fieldNumApp,
            name: 'addresses-' + fieldNumApp,
          }).appendTo('#form-group-' + fieldNumApp);
          fieldNumApp++
        });

        $("#remove-app").click(function () {
          if (fieldNumApp > 0) {
            $("#form-group-" + (fieldNumApp - 1)).remove()
            fieldNumApp--
          }
        });

});
