document.getElementById('reset_profit').addEventListener('click', function (event) {
    document.getElementById('reset_profit').submit();
});

function errorClear() {
    document.getElementById("clear_errors").submit();
}

function setFields() {
    // Get the selection box
    var selectBox = document.getElementById("in_commodity");
    // Get the selected option
    var selectedOption = selectBox.options[selectBox.selectedIndex];
    // Get the attribute value
    var buyValue = selectedOption.getAttribute("data-buy");
    var sellValue = selectedOption.getAttribute("data-sell");
    var commodityValue = selectedOption.getAttribute("value");
    // Get the fields
    var buyPrice = document.getElementById("form_buy_price");
    var sellPrice = document.getElementById("form_sell_price");
    var formBuyCommodity = document.getElementById("form_buy_commodity");
    var formSellCommodity = document.getElementById("form_sell_commodity");
    // Insert the values
    buyPrice.value = buyValue;
    sellPrice.value = sellValue;
    formBuyCommodity.value = commodityValue;
    formSellCommodity.value = commodityValue;
}

function setUnits() {
    // Get the selection box
    var selectBox = document.getElementById("in_ship");
    // Get the selected option
    var selectedOption = selectBox.options[selectBox.selectedIndex];
    // Get the attribute value
    var units = selectedOption.getAttribute("data-units");
    // Get the fields
    var buyAmount = document.getElementById("form_buy_amount");
    var sellAmount = document.getElementById("form_sell_amount");
    // Insert the values
    buyAmount.value = units;
    sellAmount.value = units;
    buyAmount.max = units;
    sellAmount.max = units;
}

function setSelect(commodity, amount) {
    // Get the fields
    var selectBox = document.getElementById("in_commodity");
    var buyAmount = document.getElementById("form_buy_amount");
    var sellAmount = document.getElementById("form_sell_amount");
    // Change the selected commodity and insert the unit amounts
    selectBox.value = commodity;
    buyAmount.value = amount;
    sellAmount.value = amount;
    // Set the price and hidden fields
    setFields();
}

setFields();
setUnits()