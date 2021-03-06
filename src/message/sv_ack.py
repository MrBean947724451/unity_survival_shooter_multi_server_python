from message.sv_response_base import SvResponseBase
from server_resource.resource_manager import ResourceManager
import struct

class SvAck(SvResponseBase):
    def __init__(self, cl_request):
        super(SvAck, self).__init__(cl_request)
        self.message_id = 200

    def payload(self):
        new_message_id = ResourceManager.instance().create_new_message_id()
        return struct.pack("<BHH", self.message_id, new_message_id, self.cl_request.message_unique_id)
