$(function () {
    "use strict";
    function getCookie(name) {
        var cookieValue = null;
        var i = 0;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (i; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    }); 
    $("select").not('.filtered').not('.disabled').not('.material-ignore').material_select();
    $(".scrollspy").scrollSpy(), $(".tooltipped").tooltip({delay: 50}), $(".menu-sidebar-collapse").sideNav({
        menuWidth: 240,
        edge: "left",
        menuOut: !1
    });
    if ($(".leftside-navigation").length) {
        var f = $(".page-topbar").height(), g = window.innerHeight - f;
        $(".leftside-navigation").height(g).perfectScrollbar({suppressScrollX: !0});
    }
    ;
    var i = $("#flow-toggle");
    $("#card-alert .close").click(function () {
        $(this).closest("#card-alert").fadeOut("slow")
    });
    if (typeof tinymce !== 'undefined') {
        tinymce.init({selector: 'textarea'});
    }
    $(".module.aligned .change-data.field-password label").addClass("active");
    $('.related-widget-wrapper').siblings("label").addClass("active");
    $(".vLargeTextField").addClass("materialize-textarea").removeClass("vLargeTextField");
    $('input[type="checkbox"]').addClass('filled-in').siblings("label").addClass('filled-in-box');
    if ($('.formset-field').length) {
        $('.formset-field').formset({
            animateForms: true,
        });
    }
    $(document).ready(function () {
        if ($('.tooltip').length) {
            $('.tooltip').tooltipster();
        }
        $(document).on('change', '.related-widget-wrapper select', function () {
            updateRelatedObjectLinks(this);
            $(this).not('.filtered').not('.disabled').not('.material-ignore').material_select();
        });
    });

    $("#result_list  tbody td.field-delete ").click(function () {
        $("input:checkbox").prop('checked', false);
        // $("#result_list tbody td.field-delete").siblings('.action-checkbox').children('input').attr('checked', false);
        $(this).siblings('.action-checkbox').parent().addClass('selected')
        var checkbox = $(this).siblings('.action-checkbox').children('input');
        checkbox.prop('checked', true);
        if (checkbox.prop('checked')) {
            $("#changelist-form .actions select").val("delete_selected");
            $("#changelist-form").submit();
        }
    })
});
