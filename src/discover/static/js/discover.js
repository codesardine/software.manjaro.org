$(function() {
    $("form").submit(function() {
        return false;
    });
});

function debounce(fn, threshold) {
    var timeout;
    threshold = threshold || 600;
    return function debounced() {
        clearTimeout(timeout);
        var args = arguments;
        var _this = this;

        function delayed() {
            fn.apply(_this, args);
        }
        timeout = setTimeout(delayed, threshold);
    };
}

function matchApp(app, searchValue) {
    if (searchValue == "") {
        $(app).each(function() {
            $(this).show()
        })
    } else {
        $(app).hide()
        $(app).each(function() {
            if ($(this).find(".data-search").text().toLocaleLowerCase().includes(searchValue)) {
                let image = $(this).find("img").attr('data-src')
                $(this).find("img").attr('src', image);
                $(this).show()
                console.log($(this))
            }
        })
    }
}

$("#autocomplete-input").focus(function() {
    $(".search-container").addClass("active")
})

$("#autocomplete-input").focusout(function () {
    function is_open() {
        const active = $(".autocomplete-content").css("display")
        if (active == "none" && !$("#autocomplete-input").is(":focus")) {
            $(".search-container").removeClass("active")
        } else {
            setTimeout(is_open, 20);
        }
    }
    is_open()
})

$("#clear-search").click(function() {
    $("#autocomplete-input").val("")
    $(".app").show()
    lazyLoad()
})

$('#autocomplete-input').keyup(debounce(function() {
    $("body").addClass("wait");
    let searchValue = $('#autocomplete-input').val().toLocaleLowerCase()
    matchApp(app, searchValue)
    setTimeout(function() {
        $("body").removeClass("wait");
    }, 300);
}, 1200));

$(document).ready(function() {
    $('.sidenav').sidenav();
    $('.materialboxed').materialbox();
    let data = $('#search-items').attr("data-src")
    let search_data = JSON.parse(data);
    $('input.autocomplete').autocomplete({
        limit: 100,
        data: search_data,
        onAutocomplete: function (val) {
            var value = $('input.autocomplete').val();
            for (key in search_data) {
                if (value == key) {
                    if (location.pathname == "/snaps") {
                        var pkg_format = "snap"
                    } else if (location.pathname == "/flatpaks") {
                        var pkg_format = "flatpak"
                    } if (location.pathname == "/applications") {
                        var pkg_format = "package"
                    }
                    var link = window.open(`https://discover.manjaro.org/${pkg_format}/${key}`, '_blank');
                    link.location;
                }
            }
        },
    });
    var modals = document.querySelectorAll('.modal');
    var modalInstances = M.Modal.init(modals);
    var tooltips = document.querySelectorAll('.tooltipped');
    var tooltipInstances = M.Tooltip.init(tooltips);
    var carousel = document.querySelectorAll('.carousel');
    var carouselInstances = M.Carousel.init(
        carousel, {
        fullWidth: true,
        indicators: true
    }
    );
    app = $("#search-items .app");
    let lazyImages = [].slice.call(document.querySelectorAll("img.lazyload"));
    let active = false;

    lazyLoad = function() {
        if (active === false) {
            active = true;

            setTimeout(function() {
                lazyImages.forEach(function(lazyImage) {
                    if ((lazyImage.getBoundingClientRect().top <= window.innerHeight && lazyImage.getBoundingClientRect().bottom >= 0) && getComputedStyle(lazyImage).display !== "none") {
                        lazyImage.src = lazyImage.dataset.src;
                        //lazyImage.classList.remove("lazyload");

                        lazyImages = lazyImages.filter(function(image) {
                            return image !== lazyImage;
                        });

                        if (lazyImages.length === 0) {
                            document.removeEventListener("scroll", lazyLoad);
                            window.removeEventListener("resize", lazyLoad);
                            window.removeEventListener("orientationchange", lazyLoad);
                        }
                    }
                });
                active = false;
            }, 200);
        }
    };

    document.addEventListener("scroll", lazyLoad);
    window.addEventListener("resize", lazyLoad);
    window.addEventListener("orientationchange", lazyLoad);

    function forceImageLoad() {
        $(window).scrollTop($(window).scrollTop() + 1)
    }
    window.addEventListener('pageshow', forceImageLoad());
});