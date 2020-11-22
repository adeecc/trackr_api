import json

from rest_framework import renderers


class InventoryItemRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''

        if 'ErrorDetail' in str(data):
            response = json.dumps({
                'errors': data["detail"]
            })

        else:
            response = json.dumps({
                'data': data
            })

        return response