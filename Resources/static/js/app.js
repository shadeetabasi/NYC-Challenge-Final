//function to reset the form inputs to blank
$(document).ready(function(){
    $(".button_reset").click(function(){
        $("#client")[0].reset()
    })
})

// Restricts input for the set of matched elements to the given inputFilter function.
(function($) {
    $.fn.inputFilter = function(inputFilter) {
      return this.on("input keydown keyup mousedown mouseup select contextmenu drop", function() {
        if (inputFilter(this.value)) {
          this.oldValue = this.value;
          this.oldSelectionStart = this.selectionStart;
          this.oldSelectionEnd = this.selectionEnd;
        } else if (this.hasOwnProperty("oldValue")) {
          this.value = this.oldValue;
          this.setSelectionRange(this.oldSelectionStart, this.oldSelectionEnd);
        } else {
          this.value = "";
        }
      });
    };
  }(jQuery));

  $(document).ready(function() {
    $("#myTextBox").inputFilter(function(value) {
      return /^\d*$/.test(value);    // Allow digits only, using a RegExp
    });
  });



























// $(document).ready(function(){
//     $(".button_reset").click(function($form){
//         $form.find('input:text, input:password, input:file, select, textarea').val('');
//         $form.find('input:radio, input:checkbox')
//         .removeAttr('checked').removeAttr('selected');
//     })
// })