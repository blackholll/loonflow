from service.base_service import BaseService


class ConstantService(BaseService):
    """一些常量"""
    def __init__(self):
        self.MAN_TYPE_PERSONAL = 1
        self.MAN_TYPE_DEPT = 2
        self.MAN_TYPE_ROLE = 3
        self.MAN_TYPE_VARIABLE = 4
        self.MAN_TYPE_MULTI = 5
        self.CURRENT_MAN_TYPE_CHOICE = ((self.MAN_TYPE_PERSONAL, '个人'),
                                        (self.MAN_TYPE_DEPT, '部门'),
                                        (self.MAN_TYPE_ROLE, '角色'),
                                        (self.MAN_TYPE_VARIABLE, '变量'),
                                        (self.MAN_TYPE_MULTI, '多人'))
        self.HANDLER_TYPE_PERSONAL = 1
        self.HANDLER_TYPE_BOT = 2
        self.HANDLER_TYPE_TIMER = 3
        self.HANDLER_TYPE_CHOICE = ((self.HANDLER_TYPE_PERSONAL, '个人'),
                                    (self.HANDLER_TYPE_BOT, '系统'),
                                    (self.HANDLER_TYPE_TIMER, '定时器'))
        self.FIELD_TYPE_CHAR = 1
        self.FIELD_TYPE_INT = 2
        self.FIELD_TYPE_FLOAT = 3
        self.FIELD_TYPE_BOOL = 4
        self.FIELD_TYPE_DATE = 5
        self.FIELD_TYPE_DATETIME = 6
        self.FIELD_TYPE_TIME = 7
        self.FIELD_TYPE_RADIO = 8
        self.FIELD_TYPE_SELECT = 9
        self.FIELD_TYPE_TEXT = 10
        self.FIELD_TYPE_CHOICE = ((self.FIELD_TYPE_CHAR, '字符型'),
                                  (self.FIELD_TYPE_INT, '整形'),
                                  (self.FIELD_TYPE_FLOAT, '浮点型'),
                                  (self.FIELD_TYPE_BOOL, '布尔型'),
                                  (self.FIELD_TYPE_DATE, '日期'),
                                  (self.FIELD_TYPE_DATETIME, '日期时间'),
                                  (self.FIELD_TYPE_TIME, '时间'),
                                  (self.FIELD_TYPE_RADIO, 'radio'),
                                  (self.FIELD_TYPE_SELECT, '下拉列表'),
                                  (self.FIELD_TYPE_TEXT, '文本域')
                                  )


CONSTANT_SERVICE = ConstantService()