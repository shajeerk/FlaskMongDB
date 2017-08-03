var rangeSlider = function(){
  var slider = $('.range-slider'),
      range = $('.range-slider__range'),
      value = $('.range-slider__value');
    
  slider.each(function(){

    value.each(function(){
      var value = $(this).prev().attr('value');
      $(this).html(value);
    });

    range.on('input', function(){
      if(this.value >= 2048){
        $(this).next(value).html(this.value + "<br\>You will have 2 VCPUs allocated to your machine ");  
      } else {
        $(this).next(value).html(this.value + "<br\>You will have 1 VCPUs allocated to your machine ");  
      }
      
    });
  });
};

rangeSlider();

$(function() {
        $('#box li a').click(function() {
           $('#box li').removeClass();
           $($(this).attr('href')).addClass('active');
        });
     });
