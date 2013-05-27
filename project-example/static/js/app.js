// Example project application. If this file is a little complicated, it's because
// we're trying to demonstrate a basic app pattern using RequireJS.

// Further configure RequireJS
require.config( {
    // Library paths
    paths: {
        moment: '//cdnjs.cloudflare.com/ajax/libs/moment.js/2.0.0/moment.min',
        spin: '//cdnjs.cloudflare.com/ajax/libs/spin.js/1.2.7/spin.min',
    },
    // Shim for non-AMD compatible Javascript libraries
    shim: {
        spin: {
            exports: 'Spinner'
        },
    }
} );

// Quotes for generator
var TARBELL_QUOTES = [
    "And he calls his great organization a benefaction, and points to his church-going and charities as proof of his righteousness. This is supreme wrong-doing cloaked by religion. There is but one name for it -- hypocrisy.",
    "Perhaps our national ambition to standardize ourselves has behind it the notion that democracy means standardization. But standardization is the surest way to destroy the initiative, to benumb the creative impulse above all else essential to the vitality and growth of democratic ideals.",
    "There is no more effective medicine to apply to feverish public sentiment than figures.",
    "How defeated and restless the child that is not doing something in which it sees a purpose, a meaning! It is by its self-directed activity that the child, as years pass, finds its work, the thing it wants to do and for which it finally is willing to deny itself pleasure, ease, even sleep and comfort.",
    "Imagination is the only key to the future. Without it none exists -- with it all things are possible.",
    "The first and most imperative necessity in war is money, for money means everything else -- men, guns, ammunition."
];

// Invoke our application by requiring some libraries
require([ 'jquery', 'base/views/NavigationView', 'moment', 'spin' ],
function($, NavigationView, moment, Spinner) {
    // Navigation view: Use Backbone view from base app to generate nav bar
    var nav = new NavigationView({
        el: $('#header'),
        title: { label: document.title, url: '' },
    }).render();

    // Random Ida Tarbell quote generator: Simple jQuery DOM manipulation
    var getQuote = function() {
        return TARBELL_QUOTES[ Math.floor( Math.random() * TARBELL_QUOTES.length ) ];
    }
    $('#tarbell-quote').text('"' + getQuote() + '"');

    // MomentJS: Using an AMD-compatible library
    $('#moment').text(moment().format('MMMM Do YYYY, h:mm:ss a'));

    // SpinJS: Using a non-AMD-compatible library and pure Javascript
    var spinnerElement = document.getElementById('spinner');
    var spinner = new Spinner().spin(spinnerElement);
});