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
    var totalSpace = selectedOption.getAttribute("data-units");
    var code = selectedOption.getAttribute("data-code");
    // Get the fields
    var buyAmount = document.getElementById("form_buy_amount");
    var sellAmount = document.getElementById("form_sell_amount");
    var shipCode = document.getElementById("ship_data");
    var shipCode2 = document.getElementById("ship_data2");
    var totalOnBoard = document.getElementById("total_cargo").innerHTML;

    // Calculate the values
    // Total space - cargo on board = space left
    var spaceLeft = parseInt(totalSpace) - parseInt(totalOnBoard.replace(/,/g, ''));

    // Insert the values
    buyAmount.value = spaceLeft;  // Buy units
    buyAmount.max = spaceLeft;  // Set max on the form input
    sellAmount.value = totalOnBoard.replace(/,/g, '');  // Sell units
    sellAmount.max = totalOnBoard.replace(/,/g, '');  // Set max on the form input

    // Send the ship code in a hidden form input
    shipCode.value = code;
    shipCode2.value = code;
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