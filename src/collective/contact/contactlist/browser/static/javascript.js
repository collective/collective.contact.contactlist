var contactcontactlist = {};

contactcontactlist.init = function(){
    jQuery('#plone-contentmenu-actions-contactlist-addtolist').prepOverlay({
        subtype: 'ajax',
        filter: common_content_filter,
        formselector: '#form',
        closeselector: '[name="form.buttons.cancel"]',
        noform: function(el, pbo) {return 'reload';}
    });
    jQuery(document).bind('loadInsideOverlay', function(e, el, responseText, errorText, api) {
        var overlay = $(el).closest('.overlay-ajax');
        var form = jQuery(overlay).find('#form');
        jQuery('#contacts-facetednav-batchactions').each(function(){
            var pathes = contactfacetednav.contacts.selection_pathes();
            jQuery(overlay).find('#formfield-form-widgets-contacts').each(function() {
                contactcontactlist.populate_hidden_field(this, pathes);
            });
        });
        // in replace list overlay, select checked list in eea contact list
        if(form.hasClass("kssattr-formname-contactlist.replace-list")){
            jQuery('.faceted-contactlist-widget input:checked').first().each(function(){
                var list_uid = jQuery(this).val();
                form.find('#form-widgets-contact_list').val(list_uid);
            });
        }
     });
};

/* Faceted navigation integration */

contactcontactlist.facetednav_addtolist = function(){
    var url = portal_url + '/@@contactlist.add-to-list';
    contactcontactlist._facetednav_open_overlay(url);
};

contactcontactlist.facetednav_replacelist = function(){
    var url = portal_url + '/@@contactlist.replace-list';
    contactcontactlist._facetednav_open_overlay(url);
};

contactcontactlist._facetednav_open_overlay = function(url){
    jQuery("<a href='" + url + "'>Edit</a>'").prepOverlay({
        subtype:'ajax',
        filter: common_content_filter,
        formselector: '#form',
        closeselector: '[name="form.buttons.cancel"]',
        noform: function(el, pbo){
            contactfacetednav.store_overlay_messages(el);
            Faceted.Form.do_form_query();
            jQuery('.faceted-contactlist-widget').each(function(){
                var widget = jQuery(this);
                var sortcountable = widget.hasClass('faceted-sortcountable');
                Faceted.Widgets[this.id.split('_')[0]].count(sortcountable);
            });
            return 'close';
        }
    }).click();
};

contactcontactlist.populate_hidden_field = function(field, pathes){
    var elt = jQuery('#formfield-form-widgets-contacts');
    for(var num in pathes){
        var path = pathes[num];
        var input = jQuery('<input type="hidden" value="' + path + '" class="hidden-widget" name="form.widgets.contacts:list" originalvalue="' + path +'"/>');
        elt.append(input);
    }
};

jQuery(document).ready(contactcontactlist.init);