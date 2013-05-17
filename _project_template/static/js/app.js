// Add some paths to require JS 
require.config( {
    paths: {
        moment: '//cdnjs.cloudflare.com/ajax/libs/moment.js/2.0.0/moment.min',
    },
} );

var TARBELL_QUOTES = [
    "And he calls his great organization a benefaction, and points to his church-going and charities as proof of his righteousness. This is supreme wrong-doing cloaked by religion. There is but one name for it -- hypocrisy.",
    "Perhaps our national ambition to standardize ourselves has behind it the notion that democracy means standardization. But standardization is the surest way to destroy the initiative, to benumb the creative impulse above all else essential to the vitality and growth of democratic ideals.",
    "There is no more effective medicine to apply to feverish public sentiment than figures.",
    "How defeated and restless the child that is not doing something in which it sees a purpose, a meaning! It is by its self-directed activity that the child, as years pass, finds its work, the thing it wants to do and for which it finally is willing to deny itself pleasure, ease, even sleep and comfort.",
    "Imagination is the only key to the future. Without it none exists -- with it all things are possible.",
    "The first and most imperative necessity in war is money, for money means everything else -- men, guns, ammunition."
];

require([ 'jquery', 'base/views/NavigationView' ],
function($, NavigationView) {
    // Demonstrate use of Backbone view
    var nav = new NavigationView({
        el: $('#header'),
        title: { label: document.title, url: '' },
    }).render();

    // Demonstrate use of simple jQuery code
    var get_quote = function() {
        return TARBELL_QUOTES[ Math.floor( Math.random() * TARBELL_QUOTES.length ) ];
    }

    $('#tarbell-quote').text('"' + get_quote() + '"');
});

