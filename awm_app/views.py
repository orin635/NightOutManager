from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .models import Profile, Group
from awm_project import settings
import json
from django.http import JsonResponse
import requests
from django.shortcuts import get_object_or_404
from collections import Counter


def service_worker(request):
    response = HttpResponse(
        open(settings.PWA_SERVICE_WORKER_PATH).read(), content_type="application/javascript"
    )
    return response


def manifest(request):
    return render(
        request,
        "manifest.json",
        {
            setting_name: getattr(settings, setting_name)
            for setting_name in dir(settings)
            if setting_name.startswith("PWA_")
        },
        content_type="application/json",
    )


def offline(request):
    return render(request, "offline.html")


# Functions for map page
@login_required
def get_user_locations(request):
    if request.method == 'GET':
        try:
            # Get the groupCode from the request
            group_code = request.GET.get('group_code')
            current_user = request.GET.get('username')

            # Filter profiles based on the groupCode
            profiles = Profile.objects.filter(groupCode=group_code).exclude(user__username=current_user)

            # Serialize the profiles to JSON
            serialized_profiles = [{'lat': profile.lat, 'lon': profile.lon, 'user__username': profile.user.username,
                                    'timestamp': profile.timestamp} for profile in profiles]

            return JsonResponse(serialized_profiles, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@login_required
def get_current_user(request):
    if request.method == 'GET':
        try:
            current_user = request.GET.get('username')

            # Filter profiles based on the username
            profiles = Profile.objects.filter(user__username=current_user)

            # Check if a profile is found
            if profiles.exists():
                # Serialize the first profile to JSON
                serialized_profile = {
                    'lat': profiles[0].lat,
                    'lon': profiles[0].lon,
                    'user__username': profiles[0].user.username,
                    'timestamp': profiles[0].timestamp
                }

                return JsonResponse(serialized_profile, safe=False)
            else:
                return JsonResponse({'error': 'Profile not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@login_required
def update_location(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            groupCode = data.get('groupCode')

            profile, created = Profile.objects.get_or_create(user=request.user)

            # Update the user's profile with the new location
            profile.lat = latitude
            profile.lon = longitude
            profile.groupCode = groupCode
            profile.save()

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@login_required
def get_pubs_in_location(request):
    if request.method == 'GET':
        lat = float(request.GET.get('lat', 0.0))
        lon = float(request.GET.get('lon', 0.0))

        overpass_url = "http://overpass-api.de/api/interpreter"
        overpass_query = (
            f'[out:json];'
            f'node["amenity"="pub"]'
            f'({lat - 0.01},{lon - 0.01},{lat + 0.01},{lon + 0.01});'
            f'out center;'
        )

        params = {
            'data': overpass_query
        }

        response = requests.get(overpass_url, params=params)
        data = response.json().get('elements', [])

        pubs = [
            {
                'name': pub.get('tags', {}).get('name', 'N/A'),
                'latitude': pub.get('lat', 'N/A'),
                'longitude': pub.get('lon', 'N/A'),
            }
            for pub in data
        ]

        return JsonResponse({'pubs': pubs})

    return JsonResponse({'error': 'Invalid request method'})


@login_required
def update_group(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            group_code = data.get('groupCode')
            pub_list = data.get('pubList', [])
            # Check if the group already exists
            group, created = Group.objects.get_or_create(groupCode=group_code)

            if not created:
                print("Group Created")
                existing_pub_list = group.pubNames
                new_pub_list = existing_pub_list + pub_list

                group.pubNames = new_pub_list
            else:
                print("Group Updated")
                group.groupCode = group_code
                group.pubNames = pub_list

            group.save()

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@login_required
def get_vote_values(request):
    if request.method == 'GET':
        try:
            group_code = request.GET.get('groupCode')
            group = get_object_or_404(Group, groupCode=group_code)

            # Get the list of pub names from the Group model
            pub_names = group.pubNames if group.pubNames else []

            # Calculate the frequency of each unique pub name
            pub_name_counts = Counter(pub_names)

            # Create a list of tuples with pub name and count
            votes = [f'{pub_name} - {count}' for pub_name, count in pub_name_counts.items()]
            print(votes)
            return JsonResponse({'votes': votes})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@login_required
@require_http_methods(["DELETE"])
def delete_group(request):
    if request.method == 'DELETE':
        try:
            group_code = request.GET.get('groupCode')
            try:
                group = Group.objects.get(groupCode=group_code)
                group.delete()
                return JsonResponse({'status': 'success'})
            except Group.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Group not found'}, status=404)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
