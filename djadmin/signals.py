import geocoder
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in

from djadmin.models import Visitor


def visitor(sender, user, request, **kwargs):
    if request.user.is_authenticated():
        if request.user_agent.is_mobile:
            device_type = "Mobile"
        elif request.user_agent.is_tablet:
            device_type = "Tablet"
        elif request.user_agent.is_touch_capable:
            device_type = "Touch"
        elif request.user_agent.is_pc:
            device_type = "PC"
        elif request.user_agent.is_bot:
            device_type = "Bot"
        else:
            device_type = "Unknown"

        browser = request.user_agent.browser.family  # returns Browser(family=u'Mobile Safari', version=(5, 1), version_string='5.1')
        browser_version = request.user_agent.browser.version_string  # returns Browser(family=u'Mobile Safari', version=(5, 1), version_string='5.1')

        # Operating System properties
        os_info = request.user_agent.os.family  # returns OperatingSystem(family=u'iOS', version=(5, 1), version_string='5.1')
        os_info_version = request.user_agent.os.version_string  # returns OperatingSystem(family=u'iOS', version=(5, 1), version_string='5.1')

        # Device properties
        device_name = request.user_agent.device.family  # returns Device(family='iPhone')
        device_name_brand = request.user_agent.device.brand
        device_name_model = request.user_agent.device.model

        ipaddress = request.META.get("HTTP_X_FORWARDED_FOR", None)
        if ipaddress:
            ipaddress = ipaddress.split(", ")[0]
        else:
            ipaddress = request.META.get("REMOTE_ADDR", "")
        if not request.POST['latitude'] == '':
            latitude = request.POST['latitude']
            longitude = request.POST['longitude']
            g = geocoder.google([latitude, longitude], method='reverse')
            city = g.city
            state = g.state_long
            country = g.country_long
        else:
            location = geocoder.ipinfo(ipaddress)
            # if not location.city:
            #     location = geocoder.maxmind(ipaddress)
            # http://www.maxmind.com/geoip/v2.0/city_isp_org/144.48.249.231?demo=1
            if location:
                city = location.city
                state = location.state
                country = location.country
            else:
                city = "Unknown"
                state = "Unknown"
                country = "Unknown"
        username = request.user
        unique_computer = request.META.get("PROCESSOR_IDENTIFIER", None)
        visitor = Visitor(device_type=device_type, name=username, ipaddress=ipaddress, browser=browser,
                          browser_version=browser_version, os_info_version=os_info_version, os_info=os_info,
                          device_name=device_name, city=city, state=state, country=country,
                          device_name_brand=device_name_brand, device_name_model=device_name_model,
                          unique_computer_processor=unique_computer)
        visitor.save()


user_logged_in.connect(visitor, sender=User, dispatch_uid="visitor")
