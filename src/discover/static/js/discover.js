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

function matchApp(searchValue) {
    let package = document.querySelectorAll("main #search-items .app")
    if (searchValue == "") {
        package.forEach(function(el) {
            el.style.display = "block"
        })
    } else {
        package.forEach(function (el) {
            el.style.display = "none"
            if (el.querySelector(".data-search").textContent.toLocaleLowerCase().includes(searchValue)) {
                el.style.display = "block"
                lazyLoad()
            }
        })
    }
    setTimeout(function () {
        window.scrollTo(0, 0)
    }, 10);
}

document.querySelector("#autocomplete-input").addEventListener('focus', function() {
    document.querySelector(".search-container").classList.add("active")
})

document.querySelector("#autocomplete-input").addEventListener("focusout", function () {
    function is_open() {
        let search = document.querySelector(".search-container")
        let results = document.querySelector(".autocomplete-content").style.display
        const active = search.classList.contains("active")
        if (!search.hasFocus && results != "block") {
            document.querySelector(".search-container").classList.remove("active")
        } else {
            setTimeout(is_open, 20);
        }
    }
    is_open()
})

document.querySelector("#clear-search").addEventListener('click', function() {
    document.querySelector("#autocomplete-input").value = ""
    let app = document.querySelectorAll(".app")
    app.forEach(function (el) {
        el.style.display = "block"
    });
    lazyLoad()
})

if (document.querySelector("#btn-up")) {
    document.querySelector("#btn-up").addEventListener('click', function () {
        window.scroll(0, 0)
    })
}

document.querySelector('#autocomplete-input').addEventListener('keyup', debounce(function () {
    let searchValue = this.value.toLocaleLowerCase()
    matchApp(searchValue)
}, 1200));

window.addEventListener('DOMContentLoaded', function() {
    let sidenav = document.querySelector('.sidenav');
    let sidenavInstances = M.Sidenav.init(sidenav);
    let modals = document.querySelectorAll('.modal');
    let modalInstances = M.Modal.init(modals);
    let tooltips = document.querySelectorAll('.tooltipped');
    let tooltipInstances = M.Tooltip.init(tooltips);
    let materialboxed = document.querySelectorAll('.materialboxed');
    let materialboxedInstances = M.Materialbox.init(materialboxed);
    let carousel = document.querySelectorAll('.carousel');
    let carouselInstances = M.Carousel.init(
        carousel, {
        fullWidth: true,
        indicators: true
    }
    );
    let searchData = document.querySelector('#search-items')
    let autocomplete = document.querySelector('.autocomplete');
    let options = {
        limit: 100,
        data: JSON.parse(searchData.dataset.src),
        onAutocomplete: function (val) {
            let value = document.querySelector('input.autocomplete').value
            for (key in data) {
                if (value == key) {
                    if (location.pathname == "/snaps") {
                        var pkg_format = "snap"
                    } else if (location.pathname == "/flatpaks") {
                        var pkg_format = "flatpak"
                    } if (location.pathname == "/applications") {
                        var pkg_format = "package"
                    }
                    let link = window.open(`https://discover.manjaro.org/${pkg_format}/${key}`, '_blank');
                    link.location;
                }
            }
        },
    }
    let autocompleteInstances = M.Autocomplete.init(autocomplete, options);
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
    window.addEventListener('pageshow', lazyLoad);
})