$("#card-alert .close").click(function () {
    $(this).closest("#card-alert").fadeOut("slow")
});
if ($(".leftside-navigation").length) {
    var f = $(".page-topbar").height()
        , g = window.innerHeight - f;
    $(".leftside-navigation").height(g).perfectScrollbar({
        suppressScrollX: !0
    });
}
$(document).ready(function () {
     $('select').not('.filtered').not('.disabled').not('.material-ignore').material_select();
   

});
$(document).ready(function () {
    $(".module.aligned .change-data.field-password label").addClass("active");
    $('.related-widget-wrapper').siblings("label").addClass("active");
    $(".vLargeTextField").addClass("materialize-textarea").removeClass("vLargeTextField");
    $('input[type="checkbox"]').addClass('filled-in').siblings("label").addClass('filled-in-box');
    $(".sidebar-collapse").sideNav({edge: "left"}), $(".menu-sidebar-collapse").sideNav({
        menuWidth: 240,
        edge: "left",
        menuOut: !1
    });
    if ($('.formset-field').length) {
        $('.formset-field').formset({
            animateForms: true,
        });
    }
    if ($('.tooltip').length) {
        $('.tooltip').tooltipster();
    }
        
    
});
