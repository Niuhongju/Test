$(function () {

    //将全部类型页面展示出来
    $("#all_types").click(function () {

        console.log('点到了');

    $("#all_types_container").show();

    var $span_all_type=$("#all_types").find('span').find('span');

    $span_all_type.removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up')

    //同时将综合排序页面收起来
    $("#sort_rule_container").hide();

    var $span_sort_rule=$("#sort_rule").find('span').find('span');

    $span_sort_rule.removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down')

    })

    //将全部类型页面点下去
    $("#all_types_container").click(function () {

    $("#all_types_container").hide();

    var $span=$("#all_types").find('span').find('span');

    $span.removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down')

    })


    //将综合排序内容点出来
    $("#sort_rule").click(function () {

        console.log('点到了');

    $("#sort_rule_container").show();

    var $span_sort_rule=$("#sort_rule").find('span').find('span');

    $span_sort_rule.removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up')

    //同时将全部分类收起来
    $("#all_types_container").hide();

    var $span_all_type=$("#all_types").find('span').find('span');

    $span_all_type.removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down')

    })

    //将展示的内容隐藏起来
    $("#sort_rule_container").click(function () {

    $("#sort_rule_container").hide();

    var $span=$("#sort_rule").find('span').find('span');

    $span.removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down')

    })


//    添加和减少商品的点击事件

    $(".subShopping").click(function () {

        console.log('sub')

        var $sub=$(this);

        var goodsid=$sub.attr('goodsid');

        $.get('/axf/subtocart/',{'goodsid':goodsid},function (data) {

            if(data['status']==302){

                window.open('/axf/login',target=('_self'));

            }
            else if(data['status']==200){

                console.log(data);

                if($sub.next('span').html()=='0'){
                    console.log('行得通1')
                    $sub.next('span').html('0');
                }
                else if($sub.next('span').html()>0){
                    console.log('行得通2')
                    var c_good_num=parseInt($sub.next('span').html())-1;

                    $sub.next('span').html(c_good_num);
                }
            }
        })
    });

    $(".addShopping").click(function () {

        console.log('add');

        var $add=$(this);

        var goodsid=$add.attr('goodsid');

        $.getJSON('/axf/addtocart/',{'goodsid':goodsid},function (data) {

            if(data['status']==302){
                window.open('/axf/login',target=('_self'));
            }
            else if(data['status']==200){

                    console.log(data);
                    // var htm=$add.next('span')
                    var c_good_num=parseInt($add.prev('span').html())+1;
                    console.log(c_good_num)

                    $add.prev('span').html(c_good_num);

            }
        })
    })



})


