import random
import string
from django.contrib.auth.models import User
from ...models import Ticket
import json
from django.core.management.base import BaseCommand
from random import randrange
from datetime import datetime, timedelta
from random import randrange

    # Add your code here to populate the database
        

# url = "https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/?field=complaint_what_happened&frm=0&size=10&sort=relevance_desc&format=json&no_aggs=false&no_highlight=false&date_received_max=2022-12-31&date_received_min=2022-12-01"

# r = requests.get(url)
# data = r.json()
# with open('data_v2.json', 'w') as f:
#     json.dump(data, f, indent=2)


def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)

d1 = datetime.strptime('2022-01-01', '%Y-%m-%d')
d2 = datetime.strptime('2023-01-01', '%Y-%m-%d')




class Command(BaseCommand):
    help = 'Populate the database'

    def handle(self, *args, **options):

        # users_data = []
        # for i in range(20):
        #     a = [random.choice(string.ascii_lowercase) for i in range(3)]
        #     a = ''.join(a)
        #     n = [str(random.randint(0, 9)) for i in range(5)]
        #     n = ''.join(n)
        #     username = a + n
        #     password = 'BillyBob990-'
        #     user = {'username': username, 'password':password}
        #     users_data.append(user)
        #     # Create users in a loop
        # for user_data in users_data:
        #     username = user_data['username']
        #     password = user_data['password']
        #     user = User.objects.create_user(username=username, password=password)
        #     user.save()
        
        with open('app/data_v2.json') as f:
            data = json.load(f)

        all_users = User.objects.all()

        a = 1
        for i in range(3000):
            if len(data[i]['_source']['complaint_what_happened']) > 0:
                random_user = random.choice(all_users)

                ticket = Ticket (
                account_number = 355960000 + a,
                product = data[i]['_source']['product'],
                complaint_date = random_date(d1, d2),
                agent_id = random_user,
                complaint_detail = data[i]['_source']['complaint_what_happened'],
                incident_category = data[i]['_source']['issue'],
                incident_subcategory = data[i]['_source']['sub_issue'],  
                customer_zip = data[i]['_source']['zip_code'],  
                customer_state = data[i]['_source']['state'],
                status = data[i]['_source']['company_response'],
                intake_channel = data[i]['_source']['submitted_via'],
                company = data[i]['_source']['company'])
                ticket.save()
                a += 1
        
        self.stdout.write(self.style.SUCCESS('Database populated successfully'))


