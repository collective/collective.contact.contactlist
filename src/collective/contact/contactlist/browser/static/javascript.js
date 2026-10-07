var contactcontactlist = {};

/* Faceted navigation integration */

contactcontactlist.facetednav_addtolist = function () {
    contactcontactlist._facetednav_open_modal('@@contactlist.add-to-list', false);
};

contactcontactlist.facetednav_replacelist = function () {
    contactcontactlist._facetednav_open_modal('@@contactlist.replace-list', true);
};

contactcontactlist._facetednav_open_modal = function (view_name, select_checked_list) {
    var link = $('<a class="pat-plone-modal"></a>')
        .attr('href', $('body').data('portal-url') + '/' + view_name + '?ajax_load=1')
        .attr('data-pat-plone-modal', '{"actionOptions": {"displayInModal": false, "reloadWindowOnClose": false}}');
    // the link is not in the page: modal events don't bubble to document, listen on it
    link.one('after-render.plone-modal.patterns', function () {
        var modal = link.data('pattern-plone-modal').$modal;
        var pathes = contactfacetednav.contacts.selection_pathes();
        modal.find('#formfield-form-widgets-contacts').each(function () {
            contactcontactlist.populate_hidden_field(this, pathes);
        });
        // in replace list modal, select checked list in eea contact list
        if (select_checked_list) {
            $('.faceted-contactlist-widget input:checked').first().each(function () {
                modal.find('#form-widgets-contact_list').val($(this).val());
            });
        }
    });
    link.on('formActionSuccess.plone-modal.patterns', function (e, response) {
        contactfacetednav.store_overlay_messages($('<div>').append($.parseHTML(response)));
        Faceted.Form.do_form_query();
        $('.faceted-contactlist-widget').each(function () {
            var widget = $(this);
            var sortcountable = widget.hasClass('faceted-sortcountable');
            Faceted.Widgets[this.id.split('_')[0]].count(sortcountable);
        });
    });
    window.__patternslib_registry['plone-modal'].init(link);
    link.trigger('click');
};

contactcontactlist.populate_hidden_field = function (field, pathes) {
    var elt = jQuery(field);
    for (var num in pathes) {
        if (pathes.hasOwnProperty(num)) {
            var path = pathes[num];
            var input = jQuery('<input type="hidden" value="' + path + '" class="hidden-widget" name="form.widgets.contacts:list" originalvalue="' + path + '"/>');
            elt.append(input);
        }
    }
};
