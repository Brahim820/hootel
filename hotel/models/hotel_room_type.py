# Copyright 2017  Alexandre Díaz
# Copyright 2017  Dario Lodeiros
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class HotelRoomType(models.Model):
    """ Before creating a 'room type', you need to consider the following:
    With the term 'room type' is meant a sales type of residential accommodation: for
    example, a Double Room, a Economic Room, an Apartment, a Tent, a Caravan...
    """
    _name = "hotel.room.type"
    _description = "Room Type"
    _inherits = {'product.product': 'product_id'}

    # Relationship between models
    product_id = fields.Many2one('product.product', 'Product Room Type',
                                 required=True, delegate=True,
                                 ondelete='cascade')
    room_ids = fields.One2many('hotel.room', 'room_type_id', 'Rooms')
    class_id = fields.Many2one('hotel.room.type.class', 'Hotel Type Class')
    room_amenity_ids = fields.Many2many('hotel.amenity',
                                      'hotel_room_type_aminity_rel',
                                      'room_type_ids', 'amenity_ids',
                                      string='Room Type Amenities',
                                      help='List of Amenities.')

    # TODO Hierarchical relationship for parent-child tree ?
    # parent_id = fields.Many2one ...

    # Used for activate records
    active = fields.Boolean('Active', default=True,
                            help="The active field allows you to hide the \
                            category without removing it.")
    # Used for ordering
    sequence = fields.Integer('Sequence', default=0)

    code_type = fields.Char('Code')

    _order = "sequence, code_type, name"

    _sql_constraints = [('code_type_unique', 'unique(code_type)',
                         'code must be unique!')]
    # total number of rooms in this type
    total_rooms_count = fields.Integer(compute='_compute_total_rooms')

    @api.depends('room_ids')
    def _compute_total_rooms(self):
        for record in self:
            record.total_rooms_count = len(record.room_ids)

    def _check_duplicated_rooms(self):
        # FIXME Using a Many2one relationship duplicated should not been possible
        pass

    @api.multi
    def get_capacity(self):
        """
        Get the minimum capacity in the rooms of this type or zero if has no rooms
        @param self: The object pointer
        @return: An integer with the capacity of this room type
        """
        self.ensure_one()
        capacities = self.room_ids.mapped('capacity')
        return min(capacities) if any(capacities) else 0

    @api.model
    def check_availability_room_type(self, dfrom, dto,
                                        room_type_id=False, notthis=[]):
        """
        Check the avalability for an specific type of room
        @param self: The object pointer
        @param dfrom: Range date from
        @param dto: Range date to
        @param room_type_id: Room Type
        @param notthis: Array excluding Room Types
        @return: A recordset of free rooms ?
        """
        reservations = self.env['hotel.reservation'].get_reservations(dfrom, dto)
        reservations_rooms = reservations.mapped('room_id.id')
        free_rooms = self.env['hotel.room'].search([
            ('id', 'not in', reservations_rooms),
            ('room_type_id.id', 'not in', notthis)
        ])
        if room_type_id:
            rooms_linked = self.env['hotel.room.type'].search([
                ('id', '=', room_type_id)
            ]).room_ids
            free_rooms = free_rooms & rooms_linked
        return free_rooms.sorted(key=lambda r: r.sequence)

    @api.model
    def create(self, vals):
        """
        Overrides orm create method.
        @param self: The object pointer
        @param vals: dictionary of fields value.
        @return: new record set for hotel room type.
        """
        vals.update({
            'purchase_ok': False,
            'type': 'service',
        })
        return super().create(vals)

    @api.multi
    def unlink(self):
        for record in self:
            record.product_id.unlink()
        return super().unlink()
