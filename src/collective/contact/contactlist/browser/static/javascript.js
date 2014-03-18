var contactcontactlist = {};

contactcontactlist.init = function(){
    jQuery('#plone-contentmenu-actions-contactlist-addtolist').prepOverlay({
        subtype: 'ajax',
        filter: common_content_filter,
        formselector: '#form',
        closeselector: '[name="form.buttons.cancel"]',
        noform: function(el, pbo) {return 'reload';}
    });
};

jQuery(document).ready(contactcontactlist.init);