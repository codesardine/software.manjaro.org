$(function () {
  $("form").submit(function () {
    return false;
  });
});

$( ".logo" ).click(function() {
  $( "#sidebar" ).toggle();
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
    $(app).each(function () {
      $(this).show()
    })
  } else {
    $(app).hide()
    $(app).each(function () {
      if ($(this).find(".content").text().toLocaleLowerCase().includes(searchValue)) {
        $(this).show()
      }
    })
  }
}

$('#search').keyup(debounce(function () {
  //app.hide();
  let searchValue = $('#search').val().toLocaleLowerCase()
  matchApp(app, searchValue)
}, 1200));

$(document).ready(function () {
  app = $("main div .app");
  if ('loading' in HTMLImageElement.prototype) {
    const images = document.querySelectorAll("img.lazyload");
    images.forEach(img => {
      img.src = img.dataset.src;
    });
  } else {
    // Dynamically import the LazySizes library
    let script = document.createElement("script");
    script.async = true;
    script.src =
      "https://cdnjs.cloudflare.com/ajax/libs/lazysizes/4.1.8/lazysizes.min.js";
    document.body.appendChild(script);
  }
});