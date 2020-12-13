$(document).ready(function(){

    var interval = setInterval(update,1000);

    function update(){
        $.getJSON($SCRIPT_ROOT + '/ajax/',
            function(data){
                
                if(data.m1 == 1){
                    $('#m1').css('background-color', 'red');
                    $('#m1').text("ZAUZETO");
                }else{
                    $('#m1').css('background-color', '#00ff19'); 
                    $('#m1').text("SLOBODNO");
                }
                if(data.m2 == 1){
                    $('#m2').css('background-color', 'red');
                    $('#m2').text("ZAUZETO");
                }else{
                    $('#m2').css('background-color', '#00ff19'); 
                    $('#m2').text("SLOBODNO");
                }
                if(data.m3 == 1){
                    $('#m3').css('background-color', 'red');
                    $('#m3').text("ZAUZETO");
                }else{
                    $('#m3').css('background-color', '#00ff19'); 
                    $('#m3').text("SLOBODNO");
                }
                if(data.m4 == 1){
                    $('#m4').css('background-color', 'red');
                    $('#m4').text("ZAUZETO");
                    
                }else{
                    $('#m4').css('background-color', '#00ff19'); 
                    $('#m4').text("SLOBODNO");
                }
                
                $('#temp').text(data.temp_js + '°C')
                $('#hum').text(data.hum_js + '%')
                $('#pres').text(data.pressure_js + 'Pa')
                
                if(data.gas_js == 0){
                    $('#gas').text('Nema opasnosti')
                    $('#g').css('background-color', '#00ff19')
                    $('#gas').css('color', 'white')
                }
                if(data.gas_js == 1){
                    $('#gas').text('Povecan nivo stetnih gasova')
                    $('#g').css('background-color', 'yellow')
                    $('#gas').css('color', 'black')
                }
                if(data.gas_js == 2){
                    $('#gas').text('Opasanost, ne ulazite u garazu!')
                    $('#g').css('background-color', 'red')
                    $('#gas').css('color', 'white')
                }

            });
    };
    
    /*$("#button5").click(function(){
        $("input[type=text], textarea").val("");
    });*/

    //Ovo je stara tranzicija koja ne postoji na trenutnoj verziji aplikacije

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

});
