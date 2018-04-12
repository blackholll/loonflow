from django.contrib import admin


class LoonModelBaseAdmin(admin.ModelAdmin):
    list_display = ('creator', 'is_deleted', 'gmt_created', 'gmt_modified')
    readonly_fields = ['creator']

    def save_model(self, request, obj, form, change):
        if not obj.creator:
            obj.creator = request.user.username
        obj.save()
