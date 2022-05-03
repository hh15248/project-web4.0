from django.utils import timezone
from django.db.models import Count

tz = timezone.get_default_timezone()

# RETURNS BEST PERSON IN LIST OF WAITING PEOPLE FOR A GIVEN TABLE
def find_best_person(table, waiting_people):
    """
    Function finds the best party in list of waiting people to assign to a given empty table 
    inputs: Table object, list of Wait objects
    return: Wait object
    """
    
    for people in waiting_people:
        capacity = int(table.seats)
        party_size = int(people.party_size)
        if 0 <= capacity - party_size <= 1:
            new_party = people
            return new_party
        elif 2<= capacity - party_size <=3  and people.wait_time >= 15:
            new_party = people
            return new_party
        elif 4 <= capacity - party_size <= 5 and people.wait_time >= 30:
            new_party = people
            return new_party
        elif capacity - party_size >= 6 and people.wait_time >= 45:
            new_party = people
            return new_party
        if people == waiting_people[-1]:
            return None 

def assign_server():
    """
    Function finds the server that is working the least number of tables
    return: server name str
    """
    from .models import Table, Config
    servers_list = list(Config.objects.last().server_names.split(','))
    current_servers = [table.server for table in Table.objects.exclude(server = "None")]
    for server in servers_list:
        if server not in current_servers:
            return server
    min_server = Table.objects.exclude(party = "Empty").exclude(server = "None").values("server").annotate(count = Count("server")).order_by("count").first()["server"]
    return min_server

def assign_tables():
    """
    Function loops through every open table and makes assignment suggestion
    """
    from .models import Wait, Table
    # Check that table assignment suggestions are only for empty tables
    full_tables = [table.number for table in list(Table.objects.exclude(party__in = ["Empty","Pending"]))]
    print("full_tables_list: ", full_tables)
    for person in list(Wait.objects.all()):
        if person.assign_sugg in full_tables:
            print("Person with assign_sugg in full tables: ", person.name)
            person.assign_sugg = 0
            person.save()
    # Find empty tables and sort to balance servers
    empty_tables = Table.objects.filter(party = "Empty")
    # Loop through empty tables
    for table in empty_tables:
        # Get list of people on waitlist, ordered by longest to shortest wait time
        waiting_people = list(Wait.objects.filter(assign_sugg = 0).order_by("arrival_time"))
        # Check if anyone is waiting on the waitlist
        if len(waiting_people) == 0:
            print("Nobody on waitlist")
            break
        else:
            # Get best party for the table
            new_party = find_best_person(table, waiting_people)
            if new_party is not None:
                # Change assignment suggestion
                new_party.assign_sugg = table.number
                new_party.save()
                # Change table party to pending until user accepts or rejects
                table.party = "Pending"
                table.save()

