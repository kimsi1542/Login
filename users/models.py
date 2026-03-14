from django.contrib.auth.models import AbstractUser
from django.db import models

# 1. 사용자 관련 (User & Preference)
class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=100)
    name = models.CharField(max_length=50)
    profile_image = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name']

    def __str__(self):
        return self.email

class UserPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='preferences')
    preference_type = models.CharField(max_length=30)
    preference_value = models.CharField(max_length=50)

# 2. 여행 그룹 관련 (Group & Member)
class TravelGroup(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')
    group_name = models.CharField(max_length=50)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    region = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

class GroupMember(models.Model):
    group = models.ForeignKey(TravelGroup, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_memberships')
    role = models.CharField(max_length=20) # admin/member
    joined_at = models.DateTimeField(auto_now_add=True)

# 3. 장소 및 일정 관련 (Place & Itinerary)
class Place(models.Model):
    group = models.ForeignKey(TravelGroup, on_delete=models.CASCADE, related_name='places')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    category = models.CharField(max_length=30)
    memo = models.TextField(null=True, blank=True)
    priority = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class Itinerary(models.Model):
    group = models.ForeignKey(TravelGroup, on_delete=models.CASCADE, related_name='itineraries')
    title = models.CharField(max_length=100)
    generated_by_ai = models.BooleanField(default=False)
    is_final = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ItineraryDay(models.Model):
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE, related_name='days')
    day_number = models.IntegerField()
    trip_date = models.DateField()
    accommodation_name = models.CharField(max_length=50, null=True, blank=True)
    accommodation_address = models.CharField(max_length=100, null=True, blank=True)
    accommodation_latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    accommodation_longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)

# 4. 세부 일정 및 교통 (Route & Transport)
class ItineraryPlace(models.Model):
    day = models.ForeignKey(ItineraryDay, on_delete=models.CASCADE, related_name='places')
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    visit_order = models.IntegerField()

class RouteSegment(models.Model):
    day = models.ForeignKey(ItineraryDay, on_delete=models.CASCADE, related_name='segments')
    from_place = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True, related_name='starts')
    to_place = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True, related_name='ends')
    from_accommodation_flag = models.BooleanField(default=False)
    to_accommodation_flag = models.BooleanField(default=False)
    segment_order = models.IntegerField()
    duration = models.IntegerField()
    distance = models.DecimalField(max_digits=10, decimal_places=2)

class TransportOption(models.Model):
    segment = models.OneToOneField(RouteSegment, on_delete=models.CASCADE, related_name='transport')
    transport_type = models.CharField(max_length=20) # 버스, 지하철, 도보 등
    bus_number = models.CharField(max_length=20, null=True, blank=True)
    subway_line = models.CharField(max_length=20, null=True, blank=True)
    departure_time = models.DateTimeField(null=True, blank=True)
    arrival_time = models.DateTimeField(null=True, blank=True)
    estimated_duration = models.IntegerField(null=True, blank=True)
    fare = models.IntegerField(null=True, blank=True)
    route_summary = models.TextField(null=True, blank=True)

# 5. AI 추천 관련 (Recommendation)
class Recommendation(models.Model):
    day = models.ForeignKey(ItineraryDay, on_delete=models.CASCADE, related_name='recommendations')
    segment = models.ForeignKey(RouteSegment, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    category = models.CharField(max_length=30)
    selected_by_user = models.BooleanField(default=False)