define(['backbone', 'text!base/templates/nav.jst'], function(Backbone, NavTemplate) {
    var NavigationView = Backbone.View.extend({
        id: 'navigation',
        parse_selector: '#content section',
        initialize: function(options) {
            this.template = options.template || NavTemplate;
            this.parse_selector = options.parse_selector || this.parse_selector;
            this.parse_sections = options.parse_sections || this.parse_sections;
            this.context = {
                title: options.title || false
            };
            if (this.parse_sections) {
                _.extend(this.context, this.parse_sections());
            }

        },
        render: function() {
            var rendered = _.template(this.template, this.context);
            this.$el.append(rendered);
            return this;
        },
        parse_sections: function() {
            var nav = [];
            _.each($(this.parse_selector), function(section) {
                var title = $(section).data('title');
                if (!title) {
                    title = $(section).find('h1').text();
                }
                if (title && section.id) {
                    nav.push({label: title, url: '#'+ section.id});
                }
            }); 
            return { nav: nav };
        }
    });
    return NavigationView;
});
