from odoo import http
from odoo.addons.portal.controllers.mail import (
    _message_post_helper,
    PortalChatter,
)


class PortalRequestChatter(PortalChatter):

    # Based on /mail/chatter_post
    # implemented to avoid html escapes
    @http.route(['/mail/request_chatter_post'], type='http',
                methods=['POST'], auth='public', website=True)
    def portal_request_chatter_post(self, res_model, res_id, message,
                                    redirect=None, attachment_ids='',
                                    attachment_tokens='', **kw):
        url = redirect
        if not url and http.request.httprequest.referrer:
            url = http.request.httprequest.referrer + "#discussion"
        if not url:
            url = '/my'

        res_id = int(res_id)

        attachment_ids = [
            int(attachment_id)
            for attachment_id in attachment_ids.split(',')
            if attachment_id
        ]
        attachment_tokens = [
            attachment_token
            for attachment_token in attachment_tokens.split(',')
            if attachment_token
        ]
        self._portal_post_check_attachments(attachment_ids, attachment_tokens)

        if message or attachment_ids:
            # message is received in plaintext and saved in html
            # if message:
            #     message = plaintext2html(message)
            post_values = {
                'res_model': res_model,
                'res_id': res_id,
                'message': message,
                'send_after_commit': False,
                'attachment_ids': attachment_ids,
            }
            post_values.update(
                (fname, kw.get(fname))
                for fname in self._portal_post_filter_params()
            )
            message = _message_post_helper(**post_values)

        return http.request.redirect(url)
