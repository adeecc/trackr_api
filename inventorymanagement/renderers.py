import json

from rest_framework import renderers


class InventoryItemRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''

        if 'ErrorDetail' in str(data):
            key = list(data.keys())[0]
            response = json.dumps({
                'errors': f"Error ({key}): " + data[key][0]
            })

        else:
            response = json.dumps({
                'data': data
            })

        return response