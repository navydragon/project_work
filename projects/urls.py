# myapp/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeamViewSet, SemesterViewSet, ProjectViewSet, \
    ParticipationViewSet, TagViewSet, MemberViewSet, ListCPDSProjects

router = DefaultRouter()



router.register(r'teams', TeamViewSet)
router.register(r'semesters', SemesterViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'participation', ParticipationViewSet)
router.register(r'tags', TagViewSet)
router.register(r'teams/(?P<team_id>[-\w]+)/members', MemberViewSet, basename='team-members')



urlpatterns = [
    path('cpds_projects/', ListCPDSProjects.as_view()),
    path('', include(router.urls)),
]
