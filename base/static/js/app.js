/** 
 * Components for story package landing pages, requires Bootstrap's javascript
 * plugins.
 */

// Add a "fetch" event to signal start of collection AJAX call.
var oldCollectionFetch = Backbone.Collection.prototype.fetch;
Backbone.Collection.prototype.fetch = function(options) {
    this.trigger("fetch");
    return oldCollectionFetch.call(this, options);
};

// Callback for jsonp calls
function processData(data) {
  return data;
}

// Numbers with commas
function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// Numbers with commas
function formatThousands(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

/* --- Collections --- */

// Photogallery
var GalleryCollection = Backbone.Collection.extend({
    url: '',
    sync: function(method, model, options) {
        var params = _.extend({
            type: 'GET',
            dataType: 'jsonp',
            url: this.url,
            jsonp: false,
            jsonpCallback: 'processData',
            processData: false
        }, options);
        return $.ajax(params);
    }
});

/* --- Collections --- */

// Photo gallery built with Bootstrap carousel
var GalleryView = Backbone.View.extend({
    initialize: function(options) {
        _.extend(this, options);

        var collection_url_parts = this.collection.url.split('/');
        collection_url_parts.pop();
        this.gallery_url = collection_url_parts.join('/');

        this.template = _.template($('#photo-template').html());
        this.carousel_template = _.template($('#carousel-template').html());
        this.$el
            .addClass('carousel slide')
            .html(this.carousel_template({ carousel_id: this.$el.attr('id')}));

        this.collection.bind('reset', this.render, this);
    },
    render: function() {
        var gallery = this;
        this.$el.find('.carousel-inner').html('');
        this.collection.each(function(photo, i) {
            var photo_json = photo.toJSON();
            photo_json.link = gallery.gallery_url + '/#' + photo_json.slug;
            var rendered = $(gallery.template(photo_json));
            if (i === 0) {
                rendered.addClass('active');
            }
            gallery.$el.find('.carousel-inner').append(rendered);
        });
        this.$el.carousel({
            interval: false
        });

        var set_height = _.bind(this.set_height, this);
        this.$el.find('img').imagesLoaded(set_height);
        $(window).resize(set_height);

        return this;
    },
    set_height: function() {
        var maxHeight = Math.max.apply(null, this.$el.find('.item').map(function () {
            return $(this).height();
        }).get());
        this.$el.height(maxHeight);
        return this;
    }
});

// Travelling nav
// Requires target as option
var TravelerView = Backbone.View.extend({
    initialize: function(options) {
        this.testMobileDevice();

        var target = options.target || false,
            traveler = options.traveler || false;
        this.align = options.align || 'left';

        if (target && traveler) {
            this.offset = options.offset || 0;
            this.$traveler = traveler;
            this.$target = target;
            this.$target.parent().addClass('traveler-parent');
            this.$traveler.wrap('<div class="traveler-wrapper">');

            if (this.align == 'right') {
                this.$end = $('<div class="span12 container-bottom">').insertAfter(this.$traveler.parent());
            } else {
                this.$end = $('<div class="span12 container-bottom">').insertAfter(this.$target);
            }

            var render = _.bind(this.render, this);
            this.render();
            var lazy_render = _.debounce(render, 500); 
            //$(window).resize(lazy_render);
        }
    },
    render: function() {
        var traveler = this;

        traveler.$traveler.removeClass('affix');
        //this.$traveler.css('width', 'auto');
        //this.$traveler.css('height', 'auto');
        //this.$traveler.parent().css('height', 'auto');

        this.$end.waypoint('destroy');
        this.$target.waypoint('destroy');
        traveler.trigger('traveler:destroy', traveler)

        // Calculate width and height
        this.$traveler.width(this.$traveler.parent().width());
        this.$traveler.height(this.$traveler.outerHeight());
        this.$traveler.parent().height(this.$traveler.outerHeight());

        // End waypoint
        this.$end.waypoint({
            handler: function(event, direction) {
                if (direction =='down') {
                    traveler.$traveler.addClass('affix-bottom').removeClass('affix'); 
                } else {
                    traveler.$traveler.removeClass('affix-bottom').addClass('affix'); 
                }
                traveler.trigger('traveler:end', event, traveler, direction)
                event.stopPropagation();
            },
            offset: traveler.$traveler.height() + this.offset 
        });

        // Top waypoint
        this.$target.waypoint({
            handler: function(event, direction) {
                $('body').toggleClass('affix-' + traveler.$traveler.attr('id'), direction=='down');
                traveler.$traveler.toggleClass('affix', direction=='down');

                traveler.$traveler.css({
                    top: traveler.offset + 'px'
                });

                if (traveler.align == 'right') {
                    traveler.$traveler.css({
                        left: traveler.$traveler.parent().offset().left + 'px'
                    });
                }
                traveler.trigger('traveler:start', event, traveler, direction)

                event.stopPropagation();
            },
            offset: this.offset
        });
    },
    testMobileDevice: function() {
        var mobile = ( navigator.userAgent.match(/(Android|iPad|iPhone|iPod)/gi) ? true : false );
        if (mobile) { 
            $('body').append($( '<link rel="stylesheet" type="text/css" media="all" href="/css/mobile.css" />' ));
        }
    }
});

// Adverts
var AdvertView = Backbone.View.extend({
    template: '#advert_template',
    initialize: function(options) {
        this.template = _.template($('#advert-template').html());
        this.$el.html(this.template({width: 0, height: 0}));
        this.$iframe = this.$el.find('iframe');
        this.iframe = this.$iframe.get(0);
        this.path = options.path;
        this.ad_type = this.$el.data('ad-type') || 'leaderboard';
        this.old_width = false;
        this.render();
        $(window).resize(_.bind(this.render, this));

        // Did the ad really load?
        this.$iframe.load(_.bind(this.hide, this)); 
    },
    render: function() {
        var width = $(window).width();
        if ( !this.old_width || (width > 767 && this.old_width < 768) || (width < 768 && this.old_width > 767) ) {

            if (width > 768) {
                if (this.ad_type == 'cube') {
                    this.width = 300;
                    this.height = 250;
                } else {
                    this.width = 728;
                    this.height = 90;
                }
            } else {
                this.width = 320;
                this.height = 50;
            }

            // Render the ad
            this.$iframe.attr('width', this.width);
            this.$iframe.attr('height', this.height);
            var rand = Math.random() * 1000000000000000;
            var ad_url = "/ad-iframe.html?iu=7184%2Ftrb.touch.chicagotribune.com%2F" + encodeURIComponent(this.path) + "&sz=" + this.width + "x" + this.height + "&ord=" + rand; 
            this.$iframe.attr('src', ad_url);
            this.iframe.contentWindow.location.replace(ad_url);
        }
        this.old_width = width;
        return this;
    },
    hide: function() {
        if (this.$iframe.contents().find('#div-gpt-ad').height()) {
            this.$el.removeClass('hidden');
        } else {
            this.$el.addClass('hidden');
        }
    }
});

// Document Cloud
var DocCloudView = Backbone.View.extend({
    el: '#page-body',
    initialize: function(options) {
        this.prefix = (options.preview_mode) ? 'https://' : 'http://';
        this.id = options.id;

        $('<div id="DV-viewer-' + this.id + '" class="DV-container" />').appendTo(this.$el);

        this.load_document();
        var load_document = _.bind(this.load_document, this);
        var lazy_load_document = _.debounce(load_document, 250);
        $(window).resize(lazy_load_document);
    },
    load_document: function() {
        var opts = {
            width: this.$el.width() * 0.8,
            height: $(window).height() * 0.75,
            sidebar: true,
            container: "#DV-viewer-" + this.id
        };

        if ($(window).width() < 940) {
            opts.sidebar = false;
        }

        if ($(window).height() < 481) {
            opts.width = this.$el.width();
            opts.height = 300;
        }

        DV.load(this.prefix + "www.documentcloud.org/documents/" + this.id + ".js", opts);
    }
});

