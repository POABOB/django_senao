from rest_framework import throttling

# SimpleRateThrottle的歷史紀錄是存在Django中的內置緩存裡
class VisitThrottle(throttling.SimpleRateThrottle):  # 只要實現這樣就能得到一個訪問節流器了
    # 作為key，到時要到settings.py裡取我們設定的頻率
    scope = 'ip'

    # get_cache_key表示訪問紀錄的key，這要我們自己覆寫
    def get_cache_key(self, request, view):
        # 使用用戶IP當作key
        return self.get_ident(request)  # 父類的get_ident(request)方法可以直接取IP