from odoo import http
from odoo.exceptions import UserError, AccessError, ValidationError


class WSDControllerMixin(http.Controller):
    def _id_to_record(self, model, record_id, no_raise=False):
        safe_errors = (
            UserError, AccessError, ValidationError, TypeError, ValueError
        )
        if record_id:
            try:
                record = http.request.env[model].browse(
                    int(record_id)).exists()
                record.check_access_rights('read')
                record.check_access_rule('read')
            except safe_errors:
                if no_raise:
                    return http.request.env[model].browse()
                raise
            return record
        return http.request.env[model].browse()

    def _is_view_active(self, xmlid):
        """ Check if view is active or not
            :param str xmlid: external ID of view
            :return bool: True if view is active, otherwise False
        """
        return http.request.env(su=True).ref(xmlid).active
