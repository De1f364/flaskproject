$(document).ready(function () {
    var fieldNum = 0;
        $("#add").click(function() {
        var newInput = $("<textarea></textarea></br>")
            .attr("addresses", "addresses-" + fieldNum)
        $("#addresses").append(newInput);
        fieldNum++;
        });
    
});