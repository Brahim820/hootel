# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, fields
from odoo.addons.queue_job.job import job
from odoo.addons.component.core import Component


class ChannelOtaInfo(models.Model):
    _name = 'channel.ota.info'
    _inherit = 'channel.binding'
    _description = 'Channel OTA Info'

    ota_id = fields.Char("Channel OTA ID", required=True)
    name = fields.Char("OTA Name", required=True)
    ical = fields.Boolean("ical", default=False)

    @job(default_channel='root.channel')
    @api.model
    def import_otas_info(self, backend):
        with backend.work_on(self._name) as work:
            importer = work.component(usage='ota.info.importer')
            return importer.import_otas_info()

class HotelRoomTypeAdapter(Component):
    _name = 'channel.ota.info.adapter'
    _inherit = 'wubook.adapter'
    _apply_on = 'channel.ota.info'

    def fetch_rooms(self):
        return super(HotelRoomTypeAdapter, self).fetch_rooms()
