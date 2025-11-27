import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Gestor_DMFX.settings')
django.setup()

from GDMFX.models import Leads
from GDMFX.forms import LeadsForm
from django.contrib.auth.models import User

try:
    # Assuming user is the one who owns the lead. We'll pick the first user found or specific one.
    # The view uses request.user. Let's try to find the lead with ID 1 and see who owns it.
    lead = Leads.objects.get(pk=1)
    print(f"Lead ID: {lead.id}")
    print(f"Lead Name: '{lead.name}'")
    print(f"Lead Source: '{lead.source}'")
    print(f"Lead User: {lead.user}")

    form = LeadsForm(instance=lead)
    print(f"Form Initial: {form.initial}")
    print(f"Form Name Value: {form['name'].value()}")
    
    # Check if widgets are messing up
    print(f"Form Name Widget Attrs: {form.fields['name'].widget.attrs}")

except Leads.DoesNotExist:
    print("Lead with ID 1 does not exist.")
except Exception as e:
    print(f"Error: {e}")
