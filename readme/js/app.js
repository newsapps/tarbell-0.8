/* 
 * The commented code shows how to load a new Javascript library and then
 * invoke it
 */

/*require.config( {
  paths: {
    highlight: '//cdnjs.cloudflare.com/ajax/libs/highlight.js/7.3/highlight.min',
  },
  shim: {
    highlight: { exports: 'hljs' }
  }
});*/

require([ 'jquery', /* 'highlight' */ ],
function($, /* hljs */) {
  // Write javascript here!!

  /*$('.doc-section pre code').each(function() {
    hljs.highlightBlock(this);
  });*/
});
