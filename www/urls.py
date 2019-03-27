from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import TemplateView
from www import views
from www.views import *

app_name = 'www'
urlpatterns = [
    path('', IndexView.as_view(), name='www'),
    path('404/', views.error404, name='www'),
    path('team/', TeamView.as_view(), name='team'),
    path('notice/', NoticeListView.as_view(), name='notice_list'),
    path('notice/<title>', NoticeContentView.as_view(), name='notice_content'),
    path('portfolio/', PortfolioView.as_view(), name='portfolio'),
    path('assignment/<int:assignment_url>/', AssignmentGetView.as_view(), name='assignment'),
    path('assignment/<int:assignment_url>/edit/', AssignmentEditView.as_view(), name='assignment_edit'),
    path('faq/', FaqView.as_view(), name='faq'),
    # path('faq/', Faq.as_view(), name='faq'),
    # 특별한 로직없이 내용만 보여줄 때 사용
    # path('faq2/', TemplateView.as_view(template_name="www/posts.html"), name='faq'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
