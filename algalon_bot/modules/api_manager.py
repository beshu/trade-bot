from datetime import datetime

class APIManager:
    def __init__(self):
        self.order = None
        self.order_state = None
        self.token = None
        self.token_expires = None
        self.refresh_token = None
        self.switch = False

    async def process_response(self, response):
        #buy & sell
        if response['id'] == 5275 or response['id'] == 2148:
            self.order_state = response['result']['order']['order_state']
            self.order = response
        #cancel all
        elif response['id'] == 4122:
            self.order = None
            self.order_state = None
        #order status
        elif response['id'] == 4316:
            self.order_state = response['result']['order_state']
        #auth
        elif response['id'] == 9929:
            self.token = response['result']['access_token']
            self.token_expires = self.calculate_expire(
                response['result']['expires_in']
            )
            self.refresh_token = response['result']['refresh_token']
    
    @staticmethod
    def calculate_expire(expires_in, safe_gap=10):
        return datetime.utcnow().timestamp() + expires_in - safe_gap



    


