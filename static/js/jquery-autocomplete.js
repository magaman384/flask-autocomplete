(function($) {

    var menuPrototype = '<ul class="autocomplete dropdown-menu"></ul>';
    var itemPrototype = '<li><a href="#"></a></li>';
    var minLength = 1;

    var Autocomplete = function (element) {
        this.element = $(element);
        this.lastValue = this.element.val();
        this.menu = $(menuPrototype).appendTo('body');
        this.shown = false;
        this.errorsDisabled = $(element)
            .closest('.control-group').hasClass('error');
        this.listen();
    }

    Autocomplete.prototype = {
        constructor: Autocomplete,

        listen: function () {
            var self = this;
            this.element
                .on('blur', $.proxy(this.blur, this))
                .on('keypress', $.proxy(this.keypress, this))
                .on('keyup', $.proxy(this.keyup, this));
            if ($.browser.chrome || $.browser.webkit || $.browser.msie) {
                this.element.on('keydown', $.proxy(this.keydown, this));
            }
            this.menu
                .on('click', $.proxy(this.click, this))
                .on('mousedown', $.proxy(this.mousedown, this))
                .on('mouseenter', 'li', $.proxy(this.mouseenter, this));

            // override submitted data with ID
            this.element.closest('form').submit(function() {
                if (!self.element.closest('html').length) return;
                var input = $('<input type="hidden" />')
                    .attr('name', self.element.attr('name'))
                    .val(self.element.attr('data-value') || self.element.val());
                $(this).append(input);
                self.element.removeAttr('name');
            });
        },

        blur: function (e) {
            var self = this;
            // the timeout prevents from hiding the menu, since after we click it, the input is blured
            // the only problem that remains is when user doesn't release the mouse button on the menu
            // the solution won't be easy
            // TODO solve that problem somehow!
            setTimeout(function () {
                self.hide();
                if (!self.element.attr('data-value') && self.element.val() != '') {
                    self.wrongValue();
                }
            }, 300);
        },

        wrongValue: function() {
            if (this.errorsDisabled) return;
            this.element
                .closest('.control-group')
                .addClass('error');
        },

        neutralValue: function() {
            if (this.errorsDisabled) return;
            this.element
                .closest('.control-group')
                .removeClass('error');
        },

        keydown: function (e) {
            this.suppressKeyPressRepeat = !~$.inArray(e.keyCode, [40, 38, 9, 13, 27]);
            this.move(e);
        },

        keypress: function (e) {
            if (this.suppressKeyPressRepeat) return;
            this.move(e);
        },

        keyup: function (e) {
            switch(e.keyCode) {
                case 40: // down arrow
                case 38: // up arrow
                    break;

                case 9: // tab
                case 13: // enter
                    if (!this.shown) return;
                    this.select();
                    break;

                case 27: // escape
                    if (!this.shown) return;
                    this.hide();
                    break;

                default:
                    this.lookup();
            }
            e.stopPropagation();
            e.preventDefault();
        },

        click: function (e) {
            e.stopPropagation()
            e.preventDefault()
            this.select();
        },

        mousedown: function(e) {
            e.stopPropagation();
            e.preventDefault();
        },

        mouseenter: function (e) {
            this.menu.find('.active').removeClass('active');
            $(e.currentTarget).addClass('active');
        },

        hide: function () {
            this.menu.hide();
            this.shown = false;
            return this;
        },

        next: function (event) {
            var active = this.menu.find('.active').removeClass('active');
            var next = active.next();
            if (!next.length) next = $(this.menu.find('li')[0]);
            next.addClass('active');
        },

        prev: function (event) {
            var active = this.menu.find('.active').removeClass('active');
            var prev = active.prev();
            if (!prev.length) prev = this.menu.find('li').last();
            prev.addClass('active');
        },

        move: function (e) {
            if (!this.shown) return;
            switch(e.keyCode) {
                case 9: // tab
                case 13: // enter
                case 27: // escape
                    e.preventDefault();
                    break;

                case 38: // up arrow
                    e.preventDefault();
                    this.prev();
                    break;

                case 40: // down arrow
                    e.preventDefault();
                    this.next();
                    break;
            }
            e.stopPropagation()
        },

        select: function () {
            var active = this.menu.find('.active');
            this.element
                .attr('data-value', active.attr('data-value'))
                .val(active.attr('data-title'))
                .change();
            // actually the change event is fired twice (we don't want that!)
            // first time automatically by blur of input
            this.lastValue = this.element.val();
            return this.hide();
        },

        lookup: function (event) {
            // fire only when value of field changed
            this.query = this.element.val();
            if (this.query == this.lastValue) return;
            this.lastValue = this.query;
            this.element.removeAttr('data-value');
            this.neutralValue();

            // too short
            if (!this.query || this.query.length < minLength) {
                return this.shown ? this.hide() : this;
            }

            // fetch with AJAX
            var url = this.element.attr('data-autocomplete-url');
            $.getJSON(url, {query: this.query}, $.proxy(this.process, this));
            return this;
        },

        process: function (items) {
            if (!items.length) {
                return this.shown ? this.hide() : this;
            }
            return this.render(items).show();
        },

        show: function () {
            var pos = $.extend({}, this.element.offset(), {
                height: this.element[0].offsetHeight
            });
            this.menu.css({
                top: pos.top + pos.height, left: pos.left
            }).show();
            this.shown = true;
            return this;
        },

        render: function (items) {
            var self = this;
            var items = $(items).map(function (i, item) {
                i = $(itemPrototype)
                    .attr('data-value', item.id)
                    .attr('data-title', item.title);
                i.find('a').html(item.html);
                return i[0];
            });
            items.first().addClass('active');
            this.menu.html(items);
            return this;
        }

    }

    $.fn.extend({
        autocomplete: function() {
            return this.each(function() {
                if (!$(this).data('__autocomplete')) {
                    $(this).data('__autocomplete', new Autocomplete(this));
                }
            });
        }
    });

})(jQuery);
