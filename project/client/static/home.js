$(document).ready(function () {
    $('#add').click(function (e) {
        $(#items).append('<div><button class="btn btn-success" type="delete" id="delete">Add address</button></div>')
    })
    $('#delete').click(function (e) {
        $(this).parent('div').remove();
        
    })
    
});