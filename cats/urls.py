from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter

from cats.views import CatsView, MissionView, TargetView

router = DefaultRouter()
router.register('cats', CatsView, basename='cats')
router.register('missions', MissionView, basename="missions")
router.register('targets', TargetView, basename='target')
