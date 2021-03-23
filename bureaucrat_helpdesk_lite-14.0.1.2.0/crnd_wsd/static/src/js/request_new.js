odoo.define('crnd_wsd.new_request', function (require) {
    'use strict';

    // Require Trumbowyg to be loaded.
    var trumbowyg = require('crnd_wsd.trumbowyg');
    var snippet_animation = require('website.content.snippets.animation');
    var snippet_registry = snippet_animation.registry;

    var blockui = require('crnd_wsd.blockui');

    var RequestCreateWidget = snippet_animation.Class.extend({
        selector: '#form_request_text',

        start: function () {
            this.load_editor();
            this.visual_characters_left_textarea();
            this.$target.submit(function () {
                blockui.blockUI();
            });

        },

        visual_characters_left_textarea: function () {
            var self = this;
            var req_max_size = self.$target.find('#request_text')[0]
                .dataset.max_text_size;
            if (req_max_size) {
                var request_body = self.$target.find('#request-body');
                self.check_textarea();
                request_body.on('keydown', 'div', self.check_textarea);
                request_body.on('keyup', 'div', self.check_textarea);
                request_body.on('paste', 'div', self.check_textarea);
            }
        },

        check_textarea: function () {
            var max_size = $('#request_text')[0].dataset.max_text_size;
            var request_text_size = $('#request_text').val().length;
            var $span_label = $('#characters_left_label');
            var left_input = max_size - request_text_size;
            var percent = left_input / max_size;
            $span_label.tooltip();
            if (left_input < 0) {
                left_input = 0;
            }

            if (percent >= 0.2) {

                $span_label.removeClass("label-warning label-danger");
                $span_label.addClass("label-primary");

            } else if (percent < 0.2 && percent > 0.1) {

                $span_label.removeClass("label-primary label-danger");
                $span_label.addClass("label-warning");

            } else {

                $span_label.removeClass("label-primary label-warning");
                $span_label.addClass("label-danger");
            }

            $span_label.html(left_input + " / " + max_size);
        },

        load_editor: function () {
            this.$form_request_text = this.$target.find('#request_text');
            this.$form_request_text.trumbowyg(trumbowyg.trumbowygOptions);
        },
    });

    snippet_registry.RequestCreateWidget = RequestCreateWidget;

    return {
        RequestCreateWidget: RequestCreateWidget,
    };

});
