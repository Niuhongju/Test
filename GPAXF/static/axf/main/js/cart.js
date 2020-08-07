$(function () {

    //改变商品选中状态,全选状态
    $(".confirm").click(function () {

        console.log('改变选中状态');

        var $confirm=$(this);

        var $li=$confirm.parents('li');

        var cartid=$li.attr('cartid');

        $.getJSON('/axf/changecartstate/',{'cartid':cartid},function (data) {

            console.log(data);

            if(data['c_is_select']){

                $confirm.find('span').find('span').html('√')

                }else{

                $confirm.find('span').find('span').html('');

            }

            if(data['is_all_select']){

                $(".all_select span span").html('√')
            }else{

                $(".all_select span span").html('')

            }

            $("#total_price").html(data['total_price'])

        })

    })
    //改变商品数量
    $(".subShopping").click(function () {

        console.log('sub');

        var $sub=$(this);

        var goodsid=$sub.attr('goodsid');

        $.getJSON('/axf/subtocart/',{'goodsid':goodsid},function (data) {

            console.log(data);

            //能进到购物车，说明就已经登录了，所以不用判断状态码了
            $sub.next('span').html(data['c_good_num']);

            $("#total_price").html(data['total_price']);

            console.log(data['total_price']);

            if(data['c_good_num']==0){

                var $li=$sub.parents('li');

                $li.remove();
            }
        })

    })
    $(".addShopping").click(function () {

        console.log('add');

        var $add=$(this);

        var goodsid=$add.attr('goodsid');

        $.getJSON('/axf/addtocart/',{'goodsid':goodsid},function (data) {

            console.log(data);


            //能进到购物车，说明就已经登录了，所以不用判断状态码了
            $add.prev('span').html(data['c_good_num'])

            $("#total_price").html(data['total_price'])

        })

    })
//    全选点击
    $(".all_select").click(function () {


        var $all_select=$(this);

        var un_select_list=[];

        var select_list=[];

        $(".confirm").each(function () {

            var $confirm=$(this);

            var cartid=$confirm.parents('li').attr('cartid')

            if($confirm.find('span').find('span').html().trim()){

                select_list.push(cartid)
            }else{

                un_select_list.push(cartid)
            }
        })

        if(un_select_list.length>0){

            $.getJSON('/axf/allselect',{'cart_list':un_select_list.join('#')},function (data) {

                console.log(data);

                $("#total_price").html(data['total_price'])

                if(data['status']===200){

                    $(".confirm").find('span').find('span').html('√');

                    $all_select.find('span').find('span').html('√');
                }

            })
        }else if(select_list.length>0){

            $.getJSON('/axf/allselect/',{'cart_list':select_list.join('#')},function (data) {

                console.log(data);

                $("#total_price").html(data['total_price'])

                if(data['status']==200){

                    $(".confirm").find('span').find('span').html('');

                    $all_select.find('span').find('span').html('');


                }

            })
        }
    })

    //下单生成
    $("#make_order").click(function () {


        var un_select_list=[];

        var select_list=[];

        $(".confirm").each(function () {

            var $confirm=$(this);

            var cartid=$confirm.parents('li').attr('cartid');

            if($confirm.find('span').find('span').html().trim()){

                select_list.push(cartid)
            }else{

                un_select_list.push(cartid)
            }
        })
        if(select_list.length===0){
            return
        }else{

            $.getJSON('/axf/makeorder/',function (data) {

                console.log(data)
                if(data['status']===200){
                    window.open('/axf/orderdetail/?orderid='+data['order_id'],target='_self');
                }
            })
        }


    })
})