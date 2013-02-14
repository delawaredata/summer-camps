from myproject.camps.models import *
from django.contrib import admin


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('organization', 'contact_person', 'user_email', 'phone')

    def user_email(self, instance):
        return instance.user.email

    def contact_person(self, instance):
        return instance.user.get_full_name()


class CampAdmin(admin.ModelAdmin):
    list_display = ('camp_name', 'organization', 'category', 'start_date', 'end_date', 'last_updated')
    list_filter = ['category', 'county', 'last_updated', 'start_date', 'end_date']
    date_hierarchy = 'last_updated'
    search_fields = ['camp_name', 'info']
    ordering = ['-last_updated']
    raw_id_fields = ('organization', )

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Camp, CampAdmin)
