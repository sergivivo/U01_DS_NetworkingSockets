# A message will contain the following info:
# - expTime: time at which the message will expire
# - msg: text with message content

class Message:

    def __init__(self, expTime=None, msg=''):
        self.expTime = expTime
        self.msg = msg
