 $(document).ready(function() {
    $('select').material_select();
  })

function addListItem() {

    let element = document.getElementById("item-data");

    let total_forms = $("#id_form-TOTAL_FORMS").val();

    let item = `
      <div class="item-row" id="item-row${total_forms}">
        <div class="col s11">
            <div class="input-field col s5">
              <select id="id_form-${total_forms}-product" name="form-${total_forms}-product">             
	            </select>         
            </div>
            <div class="input-field col s2">
              <input class="quantity" id="id_form-${total_forms}-quantity" name="form-${total_forms}-quantity" placeholder="Cantidad" type="text" value="0">
            </div>
            <div class="input-field col s2">
              <input class="rate" id="id_form-${total_forms}-unit_price" name="form-${total_forms}-unit_price" placeholder="Precio" type="text" value="1">
            </div>
            <div class="amount-field col s3">
              <div class="amount" id="amt${total_forms}">$0</div>
            </div>
        </div>
        <div class="amount-field col s1 destroy">
          <a class="btn-floating waves-effect waves-light red" id="remove${total_forms}""><i class="material-icons">delete</i></a>
        </div>
      </div>
      `

    total_forms++
    $("#id_form-TOTAL_FORMS").val(total_forms);

    $.ajax({
      url: '/ajax/get_products/',
      type: 'GET',
      data:  {},
      dataType: 'json',
      success: function(data){
        let selectItem = $(`#id_form-${total_forms-1}-product`)
        selectItem.append(new Option("---------", "", false, false))
        for (let i=0; i < data['products'].length; i++){
          let p = data['products'][i][0]
          selectItem.append(new Option(p, p, false, false))
        }
        $('select').material_select()
      }
      })    

    $("#item-data").append(item);

    $('select').material_select()
    
    var close = document.getElementsByClassName("destroy");
    for (let i = 0; i < close.length; i++) {
      close[i].onclick = function() {
        if (total_forms >= 2) {
          total_forms--
          $("#id_form-TOTAL_FORMS").val(total_forms);
          $(this).parent().remove()
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
    $( "#data" ).on( "keyup", ".rate, .quantity", function( event ) {
        event.preventDefault();

        itemID = $(this).attr("id")
        let index = itemID.match(/\d+/)[0]
        let qtID = `#id_form-${index}-quantity`
        let rateID = `#id_form-${index}-unit_price`

        let quantity = parseFloat($(qtID).val())
        let rate = parseFloat($(rateID).val())
        let amount = quantity * rate
        amount = isNaN(amount) ? 0 : amount
        // console.log("quantity", quantity)
        // console.log("rate", rate)
        // console.log("amount", amount)
        $("#amt" + index).text(amount.toLocaleString('en-us',{style:'currency', currency:'USD'}))

        updateTotal()

    })

    // Attach a delegated event handler
    $( "#data" ).on( "keyup", ".taxes", function( event ) {
        updateTotal()      
    })    

})

function updateTotal() {
  let subtotal = 0
  $('.amount').each(function () {
    let counter = toFloat($(this).text())
    subtotal += counter
  })

  $("#subtotal").text(subtotal.toLocaleString('en-us',{style:'currency', currency:'USD'}))

  let total = 0
  let tax_val = parseFloat( $("#tax").val() ) / 100
  console.log(tax_val)
  tax_val = isNaN(tax_val) ? 0 : tax_val
  total = subtotal * (1 + tax_val)
  $("#total").text(total.toLocaleString('en-us',{style:'currency', currency:'USD'}))  
}

$('#id_client').change(function(){

  let client_id = $(this).val()
  $.ajax({
    url: '/ajax/get_city/',
    type: 'GET',
    data:  {'client': client_id},
    dataType: 'json',
    success: function(data){
      $('#city').text(data.city)
    }
  })
});