function downloadData(clicked_id, next_page) {
    myhtml = $('html').html();
    $.ajax({
        type: "POST",
        url: "/save_page",
        data: {
            html: myhtml,
            pageID: clicked_id
        }, // made into a hash for retrieval
        success: function() {
            window.location.href = "/" + next_page
        }
    });
}


$(document).ready(function() {

    var selection_caller = 0;

    //This function is used select the image in the choose image areas
    $('.unselected').click(function() {
        $('.selected').removeClass('selected');
        $(this).addClass('selected');
    });
    //This function is used to pass the img_url of the selected image to the backend
    $('#save_selection').click(function() {

        switch (selection_caller) {
            case 1:
                $('#first_section').css('background-image', "url(".concat($('.selected').attr('src')));
                break;
            case 2:
                $('#second_section').css('background-image', "url(".concat($('.selected').attr('src')));
                break;
            case 3:
                $('#third_section').css('background-image', "url(".concat($('.selected').attr('src')));
                break;
            case 4:
                $('#fourth_section').attr("src", $('.selected').attr('src'));
                break;
            case 5:
                $('#fifth_section').attr("src", $('.selected').attr('src'));
                break;
            case 6:
                $('#sixth_section').attr("src", $('.selected').attr('src'));
                break
            case 7:
                $('#seventh_section').attr("src", $('.selected').attr('src'));
                break;
            case 8:
                $.getJSON('/set_favicon', {
                    favicon: $('.selected').attr('src')
                });



        }
        $.getJSON('/selectImage', {
            img_url: $('.selected').attr('src')
        });
    });

    $('#save_title').click(function() {
        document.title =  document.getElementById("title_input").value; 
    });

    function openModal(id,modalName) {
        selection_caller = id;
        $("#"+modalName).attr('class', 'modal fade show in');
        $("#"+modalName).attr('style', 'display:block');
        $("body").attr('class', 'modal-open')
        $("#"+modalName).modal();
    }


    $("#set_title").click(function(event) {
        if (event.target.id == "set_title") {
            openModal(1,"setTitleModal");
        }
    });

    $("#first_section").click(function(event) {
        if (event.target.id == "first_section") {
            openModal(1,"imageSelectionModal");
        }
    });

    $("#second_section").click(function(event) {
        if (event.target.id == "second_section") {
            openModal(2,"imageSelectionModal");


        }
    });
    $("#third_section").click(function(event) {
        if (event.target.id == "third_section") {
            openModal(3,"imageSelectionModal");
        }
    });
    $("#fourth_section").click(function(event) {
        if (event.target.id == "fourth_section") {
            openModal(4,"imageSelectionModal");
        }
    });
    $("#fifth_section").click(function(event) {
        if (event.target.id == "fifth_section") {
            openModal(5,"imageSelectionModal");
        }
    });
    $("#sixth_section").click(function(event) {
        if (event.target.id == "sixth_section") {
            openModal(6,"imageSelectionModal");
        }
    });
    $("#seventh_section").click(function(event) {
        if (event.target.id == "seventh_section") {
            openModal(7,"imageSelectionModal");
        }
    });

    $("#set_favicon").click(function(event) {
        if (event.target.id == "set_favicon") {
            openModal(8,"imageSelectionModal");
        }
    });




    $('body').on('click', '[navbar-editable]', function() {
        var $el = $(this);
        var $element = $(this).prop('nodeName');
        var paragraph = $(this).get(0);

        var $input = $('<input/>').val($el.text());
        $el.replaceWith($input);

        // First, let's verify that the paragraph has some attributes    
        if (paragraph.hasAttributes()) {
            var attrs = paragraph.attributes;
            var output = "<" + paragraph.nodeName + " ";

            for (var i = attrs.length - 1; i >= 0; i--) {
                if (attrs[i].name != "navbar-editable") {
                    output += attrs[i].name + "=\'" + attrs[i].value + "\' ";
                } else {
                    output += "navbar-editable ";
                }
            }
            output += ' >';
        }

        var save = function() {

            var $p = $(output).text($input.val());
            $input.replaceWith($p);
        };
        $input.one('blur', save).focus();

    });

    $('body').on('click', '[data-editable]', function() {

        var $el = $(this);
        var $element = $(this).prop('nodeName');
        var paragraph = $(this).get(0);


        var $input = $('<input/>').val($el.text());
        $el.replaceWith($input);

        // First, let's verify that the paragraph has some attributes    
        if (paragraph.hasAttributes()) {
            var attrs = paragraph.attributes;
            var output = "<" + paragraph.nodeName + " ";

            for (var i = attrs.length - 1; i >= 0; i--) {
                if (attrs[i].name != "data-editable") {
                    output += attrs[i].name + "=\'" + attrs[i].value + "\' ";
                } else {
                    output += "data-editable ";
                }
            }
            output += ' >';
        }


        var save = function() {

            var $p = $(output).text($input.val());
            $input.replaceWith($p);
        };

        /**
          We're defining the callback with `one`, because we know that
          the element will be gone just after that, and we don't want 
          any callbacks leftovers take memory. 
          Next time `p` turns into `input` this single callback 
          will be applied again.
        */
        $input.one('blur', save).focus();

    });

    /*$(".modal").modal("show");
     */
    $(".modal-header").on("mousedown", function(mousedownEvt) {
        var $draggable = $(this);
        var x = mousedownEvt.pageX - $draggable.offset().left,
            y = mousedownEvt.pageY - $draggable.offset().top;
        $("body").on("mousemove.draggable", function(mousemoveEvt) {
            $draggable.closest(".modal-dialog").offset({
                "left": mousemoveEvt.pageX - x,
                "top": mousemoveEvt.pageY - y
            });
        });
        $("body").one("mouseup", function() {
            $("body").off("mousemove.draggable");
        });
        $draggable.closest(".modal").one("bs.modal.hide", function() {
            $("body").off("mousemove.draggable");
        });
    });



});
