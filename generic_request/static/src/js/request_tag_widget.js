odoo.define('generic_request.request_tag_widget', function (require) {
    "use strict";

    var AbstractField = require('web.AbstractField');
    var KanbanTagWidget = require(
        'web.relational_fields').KanbanFieldMany2ManyTags;
    var RequestTagWidget = KanbanTagWidget.extend({
        events: AbstractField.prototype.events,
        start: function () {
            var self = this;
            this.$el.empty().addClass('o_field_many2manytags o_kanban_tags');
            _.each(this.value.data, function (m2m) {
                if (self.colorField in m2m.data && !m2m.data[self.colorField]) {
                    // Skip tags with colorField not set
                    return;
                }

                $('<span>', {
                    class: 'o_tag o_tag_color_' +
                        (m2m.data[self.colorField] || 0),
                    title: m2m.data.display_name,
                }).prepend('<span>').appendTo(self.$el);
            });
        },
    });

    require('web.field_registry').add('request_tag', RequestTagWidget);

    return RequestTagWidget;
});
