import os
import time
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

machine_id = settings.MACHINE_ID
base_dir = settings.BASE_DIR


class SnowflakeIDGenerator:
    def __init__(self, machine_flag):
        self.machine_flag = machine_flag
        self.sequence = 0
        # get clock_flag from file
        clock_flag_file = os.path.join(base_dir,'clock_flag.txt')
        if os.path.exists(clock_flag_file):
            with open(clock_flag_file, 'r') as f:
                try:
                    clock_flag = int(f.read())
                    if clock_flag > 7:
                        raise Exception('clock flag larger then 7')
                except Exception as e:
                    clock_flag = 0
                    with open(clock_flag_file, 'w') as f2:
                        f2.write('0')
        else:
            clock_flag = 0
            with open(clock_flag_file, 'w') as f2:
                f2.write('0')
        self.clock_flag = clock_flag
        self.last_timestamp = -1

    def __call__(self):
        timestamp = int(time.time()*1000)
        if timestamp < self.last_timestamp:
            # clock backwards issue. 3bit for clock flag
            self.clock_flag = (self.clock_flag + 1) % 8
        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) % 4096
            # if self.sequence == 0:
            #     timestamp = self.wait_next_millis(self.last_timestamp)
        else:
            self.sequence = 0
        self.last_timestamp = timestamp
        # 3bit for clock flag, 7bit for machine id.
        return ((timestamp - 1288834974657) << 22) | (self.clock_flag << 19) | (self.machine_flag << 12) | self.sequence

    # def wait_next_millis(self, last_timestamp):
    #     timestamp = int(time.time()*1000)
    #     while timestamp <= last_timestamp:
    #         timestamp = int(time.time()*1000)
    #     return timestamp


class SnowflakeIDField(models.BigAutoField):
    def __init__(self, machine_flag, *args, **kwargs):
        self.generator = SnowflakeIDGenerator(machine_flag)
        super().__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'BigAutoField'

    def db_type(self, connection):
        return 'bigint'

    def get_db_prep_value(self, value, connection, prepared=False):
        if value is None:
            return None
        return int(value)

    def generate_value(self, *args, **kwargs):
        return self.generator()


class BaseModel(models.Model):
    """
    basic model
    """
    id = SnowflakeIDField(machine_id, primary_key=True)
    tenant_id = models.BigIntegerField(_('tenant_id'))
    creator = models.CharField(_('creator'), max_length=50)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    def get_dict(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)

        dict_result = {}
        import datetime
        for attr in fields:
            if isinstance(getattr(self, attr), datetime.datetime):
                dict_result[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(getattr(self, attr), datetime.date):
                dict_result[attr] = getattr(self, attr).strftime('%Y-%m-%d')
            else:
                dict_result[attr] = getattr(self, attr)
        return dict_result

    class Meta:
        abstract = True



