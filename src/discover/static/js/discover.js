function debounce(fn, threshold) {
    var timeout;
    threshold = threshold || 300;
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
    let data = document.querySelector("#search-items").dataset.src
    if (data.length != 0) {
        const pkgsBtn = document.querySelector("#pkg-visibility")
        if (document.querySelector("#search").value.length != 0) {
            pkgsBtn.classList.remove("hide")
        } else {
            pkgsBtn.classList.add("hide")
        }
    }
    setTimeout(function () {
        window.scrollTo(0, 0)
    }, 10);
}

function install(el) {
   let packages = {
       "snap": JSON.parse(localStorage["snap"]),
       "flatpak": JSON.parse(localStorage["flatpak"]),
       "package": JSON.parse(localStorage["package"]),
       "appimage": JSON.parse(localStorage["appimage"])
   }
   let buildUrl = [];
   for (let format in packages) {
       for (let p of packages[format]) {
        buildUrl.push(format + "=" + p)
       }
   }
   url = buildUrl.join("&")
   url = "web-pamac://" + url
   el.href = url
   let array = new Array()
   localStorage.setItem("snap", [JSON.stringify(array)])
   localStorage.setItem("flatpak", [JSON.stringify(array)])
   localStorage.setItem("package", [JSON.stringify(array)])
   localStorage.setItem("appimage", [JSON.stringify(array)])
   rebuildInstall()
}

function rebuildInstall() {
    let formats = ["package", "snap", "flatpak", "appimage"]
    let install = document.querySelector("#install-list")
    let total_items = install.querySelector("#items-count")
    let items_count = 0
    for (let format of formats) {
        let data = JSON.parse(localStorage.getItem(format))
        if (data.length != 0) {
            let container = `
            <span class="${format}">
                <h6>${format.replace(/^\w/, (first) => first.toUpperCase())}</h6>
                <form id="${format}" action="#"></form>
            </span>
            `
            items_count += data.length
            let drop_down = document.querySelector(".collapsible-body")
            let template_container = document.querySelector(`.${format}`)
            if (!template_container) {
                drop_down.insertAdjacentHTML('beforeend', container)
            }
            let pkg_format = install.querySelector(`#${format}`)
            pkg_format.innerHTML = ""
            for (pkg of data) {
                let template = `
                    <p>
                    <label>
                        <input class="install-checkbox" data-pkg="${pkg}" data-format="${format}" data-title="" type="checkbox" checked="checked" onclick="remove_install(this)" />
                        <span>${pkg}</span>
                    </label>
                    </p>
                    `
                pkg_format.insertAdjacentHTML('beforeend', template)
            }
        } else {
            let template_container = document.querySelector(`.${format}`)
            if (template_container) {
                template_container.remove()
            }
        }
        
    }
    total_items.textContent = items_count
    if (items_count != 0) {
        install.style.display = "block"
    } else {
        install.style.display = "none"
    }
}

function remove_install(el) {
    if (!el.checked) {
        let data = JSON.parse(localStorage[`${el.dataset.format}`])
        let newData = data.filter(function(f) { return f !== `${el.dataset.pkg}` })
        localStorage.setItem(el.dataset.format, JSON.stringify(newData))
        M.toast({html: `<span class="pink-text">${el.dataset.pkg}&nbsp</span> removed from install.`, displayLength: 1200})
        rebuildInstall()
    }
}

function addApp(el) {
    let pkg = el.dataset.pkg
    let data = JSON.parse(localStorage[`${el.dataset.format}`])
    if (!data.includes(pkg)) {
        data.push(`${pkg}`)
        localStorage.setItem(`${el.dataset.format}`, JSON.stringify(data))
        M.toast({html: `<span class="pink-text">${pkg}&nbsp</span> added to install.`, displayLength: 1200})
    } else {
        M.toast({html: `<span class="pink-text">${pkg}&nbsp</span> already in install list.`, displayLength: 1200})
    }

   rebuildInstall()
}

function remove404Images(el) {
    let colToRemove = el.parentElement.parentElement
    let row = colToRemove.parentElement
    let colToEnlarge = row.querySelector(".col")
    if (colToEnlarge.classList.contains("s8")) {
        colToEnlarge.classList.remove("s8")
        colToEnlarge.classList.add("s12")        
    }
    colToRemove.remove()
}

function pulse() {
    this.classList.remove("pulse")
}

window.addEventListener('DOMContentLoaded', function() {
    if (document.querySelector("#btn-up")) {
        document.querySelector("#btn-up").addEventListener('click', function () {
            window.scroll(0, 0)
        })
    }
    
    let content = document.querySelector("main")
    let sidenav = document.querySelector(".sidenav")
    document.querySelector(".toggle-arrow").addEventListener('click', function () {
        if (sidenav.classList.contains("open")) {
            sidenav.classList.remove("open")
            content.classList.remove("nav-open")
        } else {
            sidenav.classList.add("open")
            content.classList.add("nav-open")    }
    })
    document.querySelector("main").addEventListener("click", function() {
        collapsibleInstance.close()
        sidenav.classList.remove("open")
        content.classList.remove("nav-open")
    })
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
    });

    var collapsible = document.querySelector('.collapsible');
    var collapsibleInstance = M.Collapsible.init(collapsible, {
    accordion: false
    });

    collapsible.querySelector("#install-btn").addEventListener("click", pulse)
    collapsible.querySelector("#install-btn").addEventListener("touchstart", pulse)
    document.querySelector(".toggle-arrow").addEventListener("click", pulse)
    document.querySelector(".toggle-arrow").addEventListener("touchstart", pulse)

    if (document.body.classList.contains("search")) {
        document.querySelector('#search').addEventListener('keyup', debounce(function () {
            let searchValue = this.value.toLocaleLowerCase()
            matchApp(searchValue)
        }, 1200))

        document.querySelector("#clear-search").addEventListener('click', function() {
            document.querySelector("#search").value = ""
            let app = document.querySelectorAll(".app")
            app.forEach(function (el) {
                el.style.display = "block"
            });
            lazyLoad()
        })
        let searchData = document.querySelector('#search-items')
        let autocomplete = document.querySelector('.autocomplete');
        function parseData() {
            let data = searchData.dataset.src
            if (!data) {
                data = "{}"
            } 
            return JSON.parse(data)
        }
        let options = {
            limit: 100,
            data: parseData(),
            onAutocomplete: function (val) {
                let value = document.querySelector('input.autocomplete').value
                for (key in options.data) {
                    if (value == key) {
                        if (location.pathname == "/snaps") {
                            var format = "snap"
                        } else if (location.pathname == "/flatpaks") {
                            var format = "flatpak"
                        } else if (location.pathname == "/applications") {
                            var format = "package"
                        } else if (location.pathname == "/appimage") {
                            var format = "appimage"
                        }
                        let link = window.open(`/${format}/${key}`, "_blank");
                        link.location;
                    }
                }
            },
        }
        let autocompleteInstances = M.Autocomplete.init(autocomplete, options);
        let btn = document.querySelector(".autocomplete-content")
        btn.classList.add("hide")
        document.querySelector("#pkg-visibility").addEventListener("click", function() {
            if (this.textContent == "visibility") {
                this.textContent = "visibility_off"
                btn.classList.add("hide")
            } else {
                this.textContent = "visibility"
                btn.classList.remove("hide")
            }
        })
    }
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
    document.addEventListener("click", function(event) {
        console.log(document.querySelector("#search").value)
        const pkgsBtn = document.querySelector("#pkg-visibility")
        let data = document.querySelector("#search-items").dataset.src

        if (event.target.id != "search" || document.querySelector("#search").value.length === 0) {
            pkgsBtn.classList.add("hide")
        } else if (event.target.id == "search" && data.length != 0){
            pkgsBtn.classList.remove("hide")
        }
    })
    
    let pkg_formats = ["snap", "flatpak", "package", "appimage"]
    for (let format of pkg_formats) {
        if (localStorage.getItem(format) === null) {
            let array = new Array()
            localStorage.setItem(format, JSON.stringify(array))
        } else {
            rebuildInstall()
        }
    }
})