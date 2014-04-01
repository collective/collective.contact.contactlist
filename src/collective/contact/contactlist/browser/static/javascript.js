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
        jQuery(overlay).find('#formfield-form-widgets-contacts').each(contactcontactlist.populate_hidden_field);

        // in replace list overlay, select checked list in eea contact list
        if(form.hasClass("kssattr-formname-contactlist.replace-list")){
            jQuery('.faceted-contactlist-widget input:checked').first().each(function(){
                var list_uid = jQuery(this).val();
                form.find('#form-widgets-contact_list').val(list_uid);
            });
        }
     });
};

contactcontactlist.facetednav_addtolist = function(){
    var url = portal_url + '/@@contactlist.add-to-list';
    contactcontactlist._open_overlay(url);
};

contactcontactlist.facetednav_replacelist = function(){
    var url = portal_url + '/@@contactlist.replace-list';
    contactcontactlist._open_overlay(url);
};

contactcontactlist._open_overlay = function(url){
    jQuery("<a href='" + url + "'>Edit</a>'").prepOverlay({
        subtype:'ajax',
        filter: common_content_filter,
        formselector: '#form',
        closeselector: '[name="form.buttons.cancel"]',
        noform: function(el, pbo){
            contactfacetednav.store_overlay_messages(el);
            Faceted.Form.do_form_query();
            return 'close';
            }
    }).click();
};

contactcontactlist.populate_hidden_field = function(field){
    var pathes = contactfacetednav.contacts.selection_pathes();
    var elt = jQuery('#formfield-form-widgets-contacts');
    for(var num in pathes){
        var path = pathes[num];
        var input = jQuery('<input type="hidden" value="' + path + '" class="hidden-widget" name="form.widgets.contacts:list" originalvalue="' + path +'"/>');
        elt.append(input);
    }
};

jQuery(document).ready(contactcontactlist.init);