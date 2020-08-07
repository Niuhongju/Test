$(function () {
    initTopSwiper();
    initSwiperMenu();

})

function initTopSwiper() {
        var swiper=new Swiper("#topSwiper",{
        loop:true,
        autoplay:2000,
        pagination:'.swiper-pagination'
    })
}

function initSwiperMenu() {
        var swiper=new Swiper("#swiperMenu",{
        slidesPerView:3,
        autoplay: 2000,
        // pagination:'.swiper-pagination'
    })
}