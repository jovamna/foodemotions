function checkAcceptCookies() {
    if (localStorage.acceptCookies == 'true') {
    } else {
        $('#div-cookies').show();
    }
}
function acceptCookies() {
    localStorage.acceptCookies = 'true';
    $('#div-cookies').hide();
}
$(document).ready(function () {
    checkAcceptCookies();
});



<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>


<!--COOKIE----------------------------->
    <script src="{% static 'appfood/js/cookies.js' %}"></script>