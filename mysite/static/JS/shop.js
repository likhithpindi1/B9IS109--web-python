var to_open_basket = document.querySelector(".back_black");
var to_close = document.querySelector(".to_close_basket");
var to_close_it = document.querySelector(".back_black");
var to_open_cart = document.querySelector(".onclick_button");

to_close.addEventListener("click", close_basket);
to_close_it.addEventListener("click", close_basket);

function open_basket(id) {
  to_open_basket.classList.remove("to_hide");
  to_open_cart.classList.remove("to_hide");

  var item_img = $(".item-" + id + " .item_image").attr("src");
  var item_name = $(".item-" + id + " .item_name_" + id).text();
  var item_price = $(".item-" + id + " .item_price_" + id).text();

  $(".img_of_item").attr("src", item_img);
  $(".name_of_item").text(item_name);
  $(".bucket_rate").text(item_price);
  $('#quantity').val(1);
  $('#stock_id').val(id);
  $(".bucket_final_rate").text(item_price);
}

function close_basket() {
  to_open_basket.classList.add("to_hide");
  to_open_cart.classList.add("to_hide");
}

const inputBox = document.getElementById("quantity");

inputBox.addEventListener("input", function() {
  // This function gets called when the value in the input box changes
  rate = $(".bucket_rate").text();
  quantity = inputBox.value;

  let product = rate * quantity

  $(".bucket_final_rate").text(product.toFixed(2));
});
