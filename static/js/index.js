/************************轮播图begin***************************/
$(function () {
    $(window).on('resize', () => {
        //1.窗口的宽度
        let clientW = $(window).width();
        //2.设置临界点
        let isShowBigImage = clientW >= 900;
        //3.获取所有item
        let $allItems = $('#index_carousel .carousel-item')
        //4.遍历
        $allItems.each((index, item) => {
            //4.1取出图片路径
            let src = isShowBigImage ? $(item).data('lg-img') : $(item).data('sm-img');
            let imgUrl = `url(${src})`;
            //4.2设置背景
            $(item).css({
                backgroundImage: imgUrl
            });
            //4.3创建img标签
            if (!isShowBigImage) {//小屏幕
                let imgEle = `<img src="${src}">`;
                $(item).empty().append(imgEle);
            } else {//大屏幕
                $(item).empty();
            }
        });
    });
    $(window).trigger('resize');
});
/************************轮播图end***************************/



/************************友情链接begin***************************/


/************************友情链接end***************************/



/************************轮播图begin***************************/
/************************轮播图begin***************************/
/************************轮播图begin***************************/
/************************轮播图begin***************************/
/************************轮播图begin***************************/

