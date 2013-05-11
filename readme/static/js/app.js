require.config( {
    paths: {
        moment: '//cdnjs.cloudflare.com/ajax/libs/moment.js/2.0.0/moment.min',
    },
} );

require([ 'jquery', 'base/views/NavigationView' ],
function($, NavigationView) {
    var nav = new NavigationView({
        el: $('#header'),
        title: { label: 'Tarbell Readme', url: '#top' },
    }).render();
});

