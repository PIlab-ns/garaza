$(document).ready(function(){

    var interval = setInterval(update,1000);

    function update(){
        $.getJSON($SCRIPT_ROOT + '/ajax/',
            function(data){
                
                if(data.m1 == 1){
                    $('#m1').css('background-color', 'red');
                    $('#m1').innerHTML = 'ZAUZETO';
                }else{
                    $('#m1').css('background-color', '#00ff19'); 
                    $('#m1').innerHTML = 'SLOBODNO';
                }
                if(data.m2 == 1){
                    $('#m2').css('background-color', 'red');
                    $('#m2').innerHTML = 'ZAUZETO';
                }else{
                    $('#m2').css('background-color', '#00ff19'); 
                    $('#m2').innerHTML = 'SLOBODNO';
                }
                if(data.m3 == 1){
                    $('#m3').css('background-color', 'red');
                    $('#m3').innerHTML = 'ZAUZETO';
                }else{
                    $('#m3').css('background-color', '#00ff19'); 
                    $('#m3').innerHTML = 'SLOBODNO';
                }
                if(data.m4 == 1){
                    $('#m4').css('background-color', 'red');
                    $('#m4').innerHTML = 'ZAUZETO';
                }else{
                    $('#m4').css('background-color', '#00ff19'); 
                    $('#m4').innerHTML = 'SLOBODNO';
                }

            });
    };

    /*
    Smenjivanje panela preko dugmica

    $('#btn1').on('click', function(){
        $('#sekcija2').slideUp(200);
        $('#sekcija3').slideUp(200, function(){
                $('#sekcija1').slideDown(200);
            });
        $('#btn1').addClass('active');
        $('#btn2').removeClass('active');
    });

    $('#btn2').on('click', function(){
        $('#sekcija1').slideUp(200, function(){
            $('#sekcija3').slideDown(200);
            $('#sekcija2').slideDown(200);
        });
        $('#btn2').addClass('active');
        $('#btn1').removeClass('active');
    });
    */

});