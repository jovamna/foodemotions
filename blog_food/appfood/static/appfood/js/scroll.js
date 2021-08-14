function apareceScroll() {
    var html = document.getElementsByTagName("html")[0];
    var elementoAparece = document.getElementsByClassName("aparece");

    document.addEventListener("wheel", function () {
        var topVent = html.scrollTop;
        for (i = 0; i < elementoAparece.lenght; i++) {
            var topelemenAparece = elementoAperece[i].offsetTop;
            if (topVent > topelemenAparece - 400) {
                elementoAparece[i].style.opacity = 1;
            }  //fin if
        }  //fin for
    })   //fin addEventlistener
}   //fin apareceScroll

apareceScroll();



//fadeIn
$("#fadeIn").click(function () {
    $("#div1").fadeIn();
    $("#div2").fadeIn("slow");
    $("#div3").fadeIn(3000);
});
//fadeOut
$("#fadeOut").click(function () {
    $("#div1").fadeOut();
    $("#div2").fadeOut("slow");
    $("#div3").fadeOut(3000);
});
//fadeToggle
$("#fadeToggle").click(function () {
    $("#div1").fadeToggle();
    $("#div2").fadeToggle("slow");
    $("#div3").fadeToggle(3000);
});
//fadeTo
$("#fadeTo").click(function () {
    $("#div1").fadeTo("slow", 0.15);
    $("#div2").fadeTo("slow", 0.5);
    $("#div3").fadeTo("slow", 0.8);
});