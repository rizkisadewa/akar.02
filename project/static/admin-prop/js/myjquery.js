(function($) {
	"use strict"
  //////////////////////////////////////
  //TIMEPICKER
  $('#timepicker1').timepicker({
    showMeridian: false
  });
  $('#timepicker2').timepicker({
    showMeridian: false
  });

  /////////////////////////////////////
  // DATEPICKER
  $('datepicker').datepicker({
    format: 'yyyy/mm/dd'
  });

})(jQuery);
