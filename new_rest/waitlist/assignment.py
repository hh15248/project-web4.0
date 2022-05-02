from datetime import datetime
from django.utils import timezone
import pandas as pd

tz = timezone.get_default_timezone()

# RETURNS BEST PERSON IN LIST OF WAITING PEOPLE FOR A GIVEN TABLE
# ATTRIBUTES TO ACCESS: table.seats, table.server, 
# for person in waiting_people
# person.party_size, person.wait_time, person.arrival_time
def find_best_person(table, waiting_people):
    """
    Function finds the best party in list of waiting people to assign to a given empty table 
    inputs: Table object, list of Wait objects
    return: Wait object
    """
    # Get new party from top of waitlist
    new_party = waiting_people.pop()
    return new_party

def find_best_table(reviewed_table_nums):
    from .models import Table
    dfTables = pd.DataFrame(Table.objects.all().values())

    servers_list = list(dfTables['server'].unique())
    dfFilled = dfTables[dfTables['party'] != "Empty"]
    empty_servers_list = list(dfTables['server'].unique())

    cust_count = {}
    for server in servers_list:
        dfServer = dfFilled[dfFilled['server'] == server]
        cust_count[server] = len(dfServer.index)
    servers_sort = dict(sorted(cust_count.items(), key = lambda item: item[1]))
    for i in range(len(list(servers_sort.keys()))):
        min_server = list(servers_sort.keys()).pop(i)
        if min_server in empty_servers_list:
            break

    for table in list(Table.objects.filter(server = min_server, party = "Empty")):
        if table.number not in reviewed_table_nums:
            return table
    return None


def assign_tables():
    from .models import Wait, Table
    # Get list of people on waitlist, ordered by longest to shortest wait time
    waiting_people = list(Wait.objects.filter(assign_sugg = 0).order_by("arrival_time"))
    # Find empty tables and sort to balance servers
    table = find_best_table([])
    reviewed_table_nums = []
    # Loop through empty tables
    while table is not None:
        # Check if anyone is waiting on the waitlist
        if len(waiting_people) == 0:
            print("Nobody on waitlist")
            break
        else:
            # Get best party for the table
            new_party = find_best_person(table, waiting_people)
            if find_best_person is None:
                reviewed_table_nums += table.number
            else:
                # Change assignment suggestion
                new_party.assign_sugg = table.number
                new_party.save()
                # Change table party to pending until user accepts or rejects
                table.party = "Pending"
                table.save()
        # Find empty tables and sort to balance servers
        table = find_best_table(reviewed_table_nums)
