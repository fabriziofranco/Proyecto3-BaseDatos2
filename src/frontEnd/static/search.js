$("#loading").hide();

function loading(){
    $("#loading").show();
}

$(function() {
    $('#flash').delay(500).fadeIn('normal', function() {
       $(this).delay(5000).fadeOut();
    });
 });