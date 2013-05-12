require.config( {
    paths: {
        moment: '//cdnjs.cloudflare.com/ajax/libs/moment.js/2.0.0/moment.min',
        highlight: '//cdnjs.cloudflare.com/ajax/libs/highlight.js/7.3/highlight.min',
    },
} );

require([ 'jquery', 'base/views/NavigationView', 'highlight' ],
function($, NavigationView, hljs) {
    var nav = new NavigationView({
        el: $('#header'),
        title: { label: 'Tarbell', url: '#about' },
    }).render();

    $('.doc-section pre code').each(function() {
        hljs.highlightBlock(this);
    });
});

