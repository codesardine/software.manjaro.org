function debounce( fn, threshold ) {
  var timeout;
  threshold = threshold || 100;
  return function debounced() {
    clearTimeout( timeout );
    var args = arguments;
    var _this = this;
    function delayed() {
      fn.apply( _this, args );
    }
    timeout = setTimeout( delayed, threshold );
  };
}

function matchApp(elem, searchValue) {
    $(elem).hide()
    $(elem).each(function() {
        if ($(this).text().toLocaleLowerCase().includes(searchValue)) {
            $(this).show()
            }
    })
}

$('#search').keyup( debounce( function() {
  //app.hide();
  let searchValue = $('#search').val().toLocaleLowerCase()
  matchApp('.app', searchValue)
}, 200 ) );
