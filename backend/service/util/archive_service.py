import json
import time

from django.forms.models import model_to_dict

from service.base_service import BaseService
from apps.util.models import Archive


class ArchiveService(BaseService):
    """
    archive service
    """
    @classmethod
    def archive_record(cls, model_name, record, operator_id):
        """
        archive record
        :param model_name:
        :param record:
        :param operator_id:
        :return:
        """
        data = json.dumps(record.get_dict())
        archived_obj = Archive(data=data, model_name=model_name, creator_id=operator_id)
        archived_obj.save()
        record.delete()
        return True, ""

    @classmethod
    def archive_record_list(cls, model_name, record_queryset, operator_id):
        """
        archive record list
        :param model_name:
        :param record_queryset:
        :param operator_id:
        :return:
        """
        archive_list = []
        for record in record_queryset:
            data = json.dumps(record.get_dict())
            archive_list.append(Archive(data=data, model_name=model_name, creator_id=operator_id))
        Archive.objects.bulk_create(archive_list)

        record_queryset.delete()
        return True, ""


archive_service_ins = ArchiveService()
