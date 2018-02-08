from rest_framework import serializers
from apps.workflow.models import Workflow, State, Transition


class WorkflowSerializer(serializers.ModelSerializer):
    gmt_created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    gmt_modified = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = Workflow
        fields = ('id', 'name', 'desc', 'flowchart', 'initial_state_id', 'notice_type', 'display_form', 'creator', 'gmt_created', 'gmt_modified',
                  'is_deleted')


class WorkflowStateSerializer(serializers.ModelSerializer):
    gmt_created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    gmt_modified = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = State
        fields = ('id', 'name', 'is_end_state', 'participant', 'distribute_type', 'state_field_str',
                  'task_dict_info', 'creator', 'gmt_created', 'gmt_modified', 'is_deleted')
