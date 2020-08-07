$(function () {

    $(".order_detail").click(function () {

        var $order_detail=$(this);

        var orderid=$order_detail.attr('orderid');

        window.open('/axf/orderdetail/?orderid='+orderid,target='_self');

    })
})