require([ 'jquery', 'base/views/NavigationView' ],
function($, NavigationView) {
    var nav = new NavigationView({
        el: $('#header'),
        title: { label: 'Tarbell Readme', url: '#header' },
    }).render();
});

