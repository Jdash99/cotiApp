
function addListItem() {

    var element = document.getElementById("item-data");
    var numberOfChildren = element.children.length
    var i = numberOfChildren + 1

    var item = `
            <div class="row item-row" id="item-row${i}">
                <div class="input-field col s5">
                  <input type="text" placeholder="Description" id="descr${i}">
                </div>
                <div class="input-field col s2">
                  <input class="quantity" type="text" placeholder="1" id="qt${i}" value="0">
                </div>
                <div class="input-field col s2">
                  <input class="rate" type="text" placeholder="0" id="rate${i}" value="1">
                </div>
                <div class="amount-field col s2">
                  <div class="amount" id="amt${i}">$0</div>
                </div>
                <div class="amount-field col s1">
                  <a class="btn-floating waves-effect waves-light red" id="remove${i}"><i class="material-icons destroy">delete</i></a>
                </div>                
            </div>
          `              

    $("#item-data").append(item);
    
    var close = document.getElementsByClassName("destroy");
    var l;
    for (l = 0; l < close.length; l++) {
      close[l].onclick = function() {
        if (i >= 2) {
          i--
          $(this).parent().parent().parent().remove()
          updateTotal() 
        }

      }
    }    
}

function toFloat(str) {
    return parseFloat(str.replace(/,/g , "").slice(1));
}

$(function(){
    $("#add").on('click', addListItem);

    // Attach a delegated event handler
    $( "#data" ).on( "keyup", ".rate, .quantity, .taxes", function( event ) {
        event.preventDefault();
        var index = $(this).attr("id").slice(-1);
        var quantity = parseFloat($("#qt" + index).val());
        var rate = parseFloat($("#rate" + index).val());
        var amount = quantity * rate;
        amount = isNaN(amount) ? 0 : amount;
        $("#amt" + index).text(amount.toLocaleString('en-us',{style:'currency', currency:'USD'}));

        updateTotal()      

    });

});

function updateTotal() {
  var subtotal = 0;
  $('.amount').each(function () {
      var counter = toFloat($(this).text());
      subtotal += counter;
  });

  $("#subtotal").text(subtotal.toLocaleString('en-us',{style:'currency', currency:'USD'}));

  var total = 0;
  var tax_val = parseFloat( $("#tax").val() ) / 100;
  tax_val = isNaN(tax_val) ? 0 : tax_val;
  total = subtotal * (1 + tax_val);
  $("#total").text(total.toLocaleString('en-us',{style:'currency', currency:'USD'}));  
}