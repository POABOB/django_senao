# Custom Render Response
from rest_framework.renderers import JSONRenderer

# 客製化 Response 格式
class custom_renderer(JSONRenderer):
    def is_success(self, status_code=200):
        if status_code >= 200 and status_code < 300 :
            return True
        else:
            return False

    # Build my custom renderer function
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context:
            success = self.is_success(renderer_context["response"].status_code)
            reason = ""
            if not success:
                print(data)
                reason = data["error"]

            #自定义返回的格式
            ret = {
                'success': success,
                'reason': reason,
                # 'data': data,
            }
            # return JSON data
            return super().render(ret, accepted_media_type, renderer_context)
        else:
            return super().render(data, accepted_media_type, renderer_context)