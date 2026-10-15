/* Faceted navigation integration: "Add to list" and "Replace list" batch actions of collective.contact.facetednav.
 * Classic script: contactfacetednav, Faceted and the plone-modal pattern are only used when a button is clicked. */
var contactcontactlist = {};

contactcontactlist.facetednav_addtolist = function () {
    contactcontactlist._facetednav_open_modal('@@contactlist.add-to-list', false);
};

contactcontactlist.facetednav_replacelist = function () {
    contactcontactlist._facetednav_open_modal('@@contactlist.replace-list', true);
};

contactcontactlist._facetednav_open_modal = function (view_name, select_checked_list) {
    // the modal is built next to its link: the link must be in the page (the faceted refresh removes it).
    // Options in its own attribute: the parser merges the body's data-pat-plone-modal over patPloneModal(options)
    var link = jQuery('<a hidden></a>')
        .attr('href', jQuery('body').data('portal-url') + '/' + view_name + '?ajax_load=1')
        .attr('data-pat-plone-modal', JSON.stringify({
            actionOptions: {displayInModal: false, reloadWindowOnClose: false}
        }))
        .appendTo('#contacts-facetednav-batchactions');
    // first render only: a form redrawn with errors keeps the posted contacts
    link.one('after-render.plone-modal.patterns', function () {
        var modal = link.data('pattern-plone-modal').$modal;
        contactcontactlist.populate_hidden_field(
            modal.find('#formfield-form-widgets-contacts'),
            contactfacetednav.contacts.selection_paths()
        );
        // in the replace list modal, select the list checked in the "Contact lists" filter
        if (select_checked_list) {
            var checked = jQuery('.faceted-contactlist-widget input:checked').first();
            if (checked.length) {
                modal.find('#form-widgets-contact_list').val(checked.val());
            }
        }
    });
    // saved: no page reload, the status message goes to the batch actions, results and list counts are refreshed
    link.on('formActionSuccess.plone-modal.patterns', function (e, response) {
        contactfacetednav.store_overlay_messages(jQuery('<div>').append(jQuery.parseHTML(response)));
        Faceted.Form.do_form_query();
        jQuery('.faceted-contactlist-widget').each(function () {
            Faceted.Widgets[this.id.split('_')[0]].count(jQuery(this).hasClass('faceted-sortcountable'));
        });
    });
    link.patPloneModal().trigger('click');
};

contactcontactlist.populate_hidden_field = function (field, paths) {
    jQuery.each(paths, function (num, path) {
        jQuery('<input type="hidden" class="hidden-widget" name="form.widgets.contacts:list" />')
            .attr('value', path)
            .attr('originalvalue', path)
            .appendTo(field);
    });
};
