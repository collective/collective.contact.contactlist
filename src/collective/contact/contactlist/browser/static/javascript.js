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
        jQuery(overlay).find('#formfield-form-widgets-contacts').each(contactcontactlist.populate_hidden_field)
     });
};

contactcontactlist.facetednav_addtolist = function(){
    var url = portal_url + '/@@contactlist.add-to-list'
    jQuery("<a href='" + url + "'>Add to list</a>'").prepOverlay({
        subtype:'ajax',
        filter: common_content_filter,
        formselector: '#form',
        closeselector: '[name="form.buttons.cancel"]',
        noform: function(el, pbo){
            var messages = jQuery(el).find('.portalMessage');
            jQuery('#contacts-facetednav-batchactions').prepend(messages);
            return 'close';
            }
    }).click();
}

contactcontactlist.populate_hidden_field = function(field){
    var pathes = contactfacetednav.contacts.selection_pathes();
    var field = jQuery('#formfield-form-widgets-contacts')
    for(var num in pathes){
        var path = pathes[num];
        var input = jQuery('<input type="hidden" value="' + path + '" class="hidden-widget" name="form.widgets.contacts:list" originalvalue="' + path +'"/>');
        field.append(input);
    }
}

jQuery(document).ready(contactcontactlist.init);