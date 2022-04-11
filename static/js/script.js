$(document).ready(function(){
    $('.hamburger_btn').on("click", function(){
        $('.sidebar_navigation').show()
    })
    $('#close-btn-menu').on("click", function(){
        $('.sidebar_navigation').hide()
    })
})