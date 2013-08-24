require([ 'jquery', 'js/views/NavigationView' ],
function($, NavigationView) {
  // Write javascript here!!
  // $('.myclass').click( ... );
  
  var nav = new NavigationView({
      el: $('#header'),
      title: { label: 'Tarbell', url: '#about' },
  }).render();
});
