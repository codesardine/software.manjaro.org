$(function () {
  $("form").submit(function () {
    return false;
  });
});
$( "#search" ).focus();

$( ".search-icon .fa-search" ).click(function() {
  $( ".search-box" ).toggle();
  $( "#search" ).focus();
});

$(window).on('scroll', function () {
  if ($(document).scrollTop() >= 50) {
    $(".speech-bubble").hide();
  } else {
    $(".speech-bubble").show();
  }
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

$('.back-button').click(function(){
    window.history.back()
})

function matchApp(app, searchValue) {
  if (searchValue == "") {
    $(app).each(function () {
      $(this).show()
    })
  } else {
    $(app).hide()
    $(app).each(function () {
      if ($(this).find("div.content").text().toLocaleLowerCase().includes(searchValue)) {
        let image = $(this).find("img").attr('data-src')
        $(this).find("img").attr('src', image);
        $(this).show()
      }
    })
  }
}

$('#search').keyup(debounce(function () {
  $("body").addClass("wait");
  let searchValue = $('#search').val().toLocaleLowerCase()
  matchApp(app, searchValue)
  setTimeout(function(){   $("body").removeClass("wait");
}, 300);
}, 1200));

$( document ).ready(function() {
  app = $("#search-items .app");
  let lazyImages = [].slice.call(document.querySelectorAll("img.lazyload"));
  let active = false;

  const lazyLoad = function() {
    if (active === false) {
      active = true;

      setTimeout(function() {
        lazyImages.forEach(function(lazyImage) {
          if ((lazyImage.getBoundingClientRect().top <= window.innerHeight && lazyImage.getBoundingClientRect().bottom >= 0) && getComputedStyle(lazyImage).display !== "none") {
            lazyImage.src = lazyImage.dataset.src;
            lazyImage.classList.remove("lazyload");

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
      $(window).scrollTop($(window).scrollTop()+1)
  }
  window.addEventListener('pageshow', forceImageLoad());
  $("body").css("cursor", "default");
});
