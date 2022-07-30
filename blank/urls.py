from django.urls import path
from .views import home, blank_detail, blank_list, delete_blank, GeneratePdf, BlankCreateView, blank_update
from django.contrib import admin

urlpatterns = [
    path('', home, name='home-page'),
    path('add_blank/', BlankCreateView.as_view(), name='add-blank'),
    path('blanks_list/', blank_list, name='blanks-list'),
    path('blank_delete/<blank_id>', delete_blank, name='blank-delete'),
    path('blank/<blank_id>', blank_detail, name='blank-detail'),
    # path('blank_pdf/<blank_id>', blank_pdf, name='blank-pdf'),
    path('pdf/<blank_id>', GeneratePdf.as_view(), name='blank-pdf'),
    path('blank_update/<blank_id>/', blank_update, name='blank-update'),
]

admin.site.site_header = "Administration Panel"
admin.site.site_url = "http://127.0.0.1:8000/blank"
# admin.site.site_title = ''
# admin.site.index_title = ""
