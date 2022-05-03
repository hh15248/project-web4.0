from django.shortcuts import render
from .models import Wait, Table, Config, WaitlistHistory, TableHistory
from .forms import WaitForm, ConfigForm
from .assignment import assign_tables, assign_server
from datetime import datetime, timedelta
from django.utils import timezone


tz = timezone.get_default_timezone()

def estimate_wait(formW):
    # Assume average turnover is 90 min
    party_size = formW["party_size"].value()
    # Find other eligible party sizes competing for same primary table
    if int(party_size)%2 == 0:
        elig = int(party_size)-1
    else:
        elig = int(party_size)+1
    tables = Table.objects.filter(seats__in = [party_size,elig]).order_by("time_seated")
    # If no one is seated, wait 0 min
    if len(tables) == 0:
        return 0
    # See if there is an empty table, if so, wait 0 min
    for table in tables:
        print("I found an empty table")
        if table.party == "Empty":
            return 0
    competing = Wait.objects.filter(party_size__in = [party_size, elig])
    print(competing)
    print(tables)
    # If people on waitlist for each table already, estimate 90 minute wait
    if len(competing) >= len(tables):
        print("More competing people than people tables")
        return 90
    # If competing with other people, estimate wait
    print("I made it too far")
    place_in_line = len(competing)
    table_dine_time = list(tables)[place_in_line].dining_time
    estimated_wait = 90 - table_dine_time
    return estimated_wait



def waitlist_view(request):
    waitlist = Wait.objects.all()
    formW = WaitForm(request.POST or None)
    open_tables_list = [table.number for table in Table.objects.filter(party__in = ["Empty","Pending"])]
    if formW.is_valid():
        obj = formW.save(commit=False)
        obj.est_wait = estimate_wait(formW)
        obj.save()
        formW = WaitForm()
        assign_tables()
    context = {
        'waitlist' : waitlist,
        'formW' : formW,
        'open_tables': sorted(open_tables_list)
    }
    returned_num = (request.POST or None)
    if returned_num is not None:
        if "accept_sugg" in returned_num:
            cust = Wait.objects.filter(assign_sugg= returned_num['accept_sugg']).first()
            table = Table.objects.filter(number= returned_num['accept_sugg']).first()
            n = cust.name
            ps = cust.party_size
            at = cust.arrival_time
            wt = cust.wait_time
            wait_done = WaitlistHistory(name = n, party_size = ps, arrival_time = at, wait_time = wt)
            wait_done.save()
            table.party = cust.name
            table.party_size = cust.party_size
            table.time_seated = datetime.now(tz)
            table.server = assign_server()
            table.save()
            cust.delete()
        elif "manual_submit" in returned_num:
            cust = Wait.objects.filter(name= returned_num['guest_name']).first()
            table = Table.objects.filter(number= returned_num['table_num']).first()
            n = cust.name
            ps = cust.party_size
            at = cust.arrival_time
            wt = cust.wait_time
            wait_done = WaitlistHistory(name = n, party_size = ps, arrival_time = at, wait_time = wt)
            wait_done.save()
            table.party = cust.name
            table.party_size = cust.party_size
            table.time_seated = datetime.now(tz)
            table.server = assign_server()
            table.save()
            cust.delete()
        elif "removal" in returned_num:
            print("Removed guest name: ", returned_num['guest_name'])
            cust = Wait.objects.filter(name= returned_num['guest_name']).first()
            if cust.assign_sugg:
                print("IM SUPPOSED TO UPDATE TO EMPTY")
                table = Table.objects.filter(number = cust.assign_sugg).first()
                table.party = "Empty"
                table.save()
                print("Set table {} to empty".format(table.number))
            cust.delete()
        assign_tables()
    return render(request, "waitlist.html", context)

def tables_view(request):
    tables = Table.objects.all()
    tablehistory = TableHistory.objects.all()
    context = {'tables' : tables}
    returned_num = (request.POST or None)
    if returned_num is not None:
        table = Table.objects.filter(number= returned_num['table_num']).first()
        p = table.party
        ps = table.party_size
        s = table.server
        ts = table.time_seated
        dt = table.dining_time
        if p != "Empty" and p != "Pending":
            table_done = TableHistory(party = p, party_size = ps, server = s, time_seated = ts, dining_time = dt)
            table_done.save()
        table.party = "Empty"
        table.server = "None"
        table.save()
        assign_tables()
    print(returned_num)
    return render(request, "tables.html", context)

def config_view(request):
    config = Config.objects.all()
    formC = ConfigForm(request.POST or None)
    if formC.is_valid():
        Config.objects.all().delete()
        formC.save()
        formC = ConfigForm()
        if config:
            setup = Config.objects.last()
            names_list = setup.server_names.split(',')
            num = len(names_list)
            table2 = setup.tables_for_2
            table4 = setup.tables_for_4
            table6 = setup.tables_for_6
            table8 = setup.tables_for_8
            table_size_list = []
            total_tables = table2 + table4 + table6 + table8
            for i in range(table2):
                table_size_list.append(2)
            for i in range(table4):
                table_size_list.append(4)
            for i in range(table6):
                table_size_list.append(6)
            for i in range(table8):
                table_size_list.append(8)
            Table.objects.all().delete()
            for i in range(1, total_tables + 1):
                table = Table(number = i, party = "Empty", seats = table_size_list[i-1], party_size = 0, time_seated = datetime.now(tz), server = "None")
                table.save()
    context = {
        'config' : config,
        'formC' : formC,
    }
    return render(request, "config.html", context)

def waitlist_history_view(request):
    waithistory = WaitlistHistory.objects.all()
    waits = Wait.objects.all()
    context = {
        'waithistory' : waithistory,
        'waits' : waits
    }
    return render(request, "wlhistory.html", context)

def table_history_view(request):
    tablehistory = TableHistory.objects.all()
    tables = Table.objects.all()
    context = {
        'tablehistory' : tablehistory,
        'tables' : tables
    }
    return render(request, "tablehistory.html", context)

def report_view(request):
    info = []
    all_waits = WaitlistHistory.objects.all()
    all_tables = TableHistory.objects.all()
    if all_waits:
        cust_count = 0
        total_wait_time = 0
        count2 = 0
        total_wait_time2 = 0
        count4 = 0
        total_wait_time4 = 0
        count6 = 0
        total_wait_time6 = 0
        count8 = 0
        total_wait_time8 = 0
        for wait in all_waits:
            wait_time = float(wait.wait_time)
            party_size = float(wait.party_size)
            cust_count += party_size
            total_wait_time += wait_time
            if party_size == 1 or party_size == 2:
                total_wait_time2 += wait_time
                count2 += 1
            if party_size == 3 or party_size == 4:
                total_wait_time4 += wait_time
                count4 += 1
            if party_size == 5 or party_size == 6:
                total_wait_time6 += wait_time
                count6 += 1
            if party_size == 7 or party_size == 8:
                total_wait_time8 += wait_time
                count8 += 1
        cc = 'Total Customers: ' + str(cust_count)
        info.append(cc)
        total_tables = len(all_waits)
        tt = 'Total Tables: ' + str(total_tables)
        info.append(tt)
        avg_wait = total_wait_time/len(all_waits)
        aw = 'Average Wait Time: ' + str("{:.2f}".format(avg_wait)) + ' minutes'
        info.append(aw)
        if count2 != 0:
            avg_wait2 = total_wait_time2/count2
            aw2 = 'Average Wait Time for Table of 2: ' + str("{:.2f}".format(avg_wait2)) + ' minutes'
            info.append(aw2)
        if count4 != 0:
            avg_wait4 = total_wait_time4/count4
            aw4 = 'Average Wait Time for Table of 4: ' + str("{:.2f}".format(avg_wait4)) + ' minutes'
            info.append(aw4)
        if count6 != 0:
            avg_wait6 = total_wait_time6/count6
            aw6 = 'Average Wait Time for Table of 6: ' + str("{:.2f}".format(avg_wait6)) + ' minutes'
            info.append(aw6)
        if count8 != 0:
            avg_wait8 = total_wait_time8/count8
            aw8 = 'Average Wait Time for Table of 8: ' + str("{:.2f}".format(avg_wait8)) + ' minutes'
            info.append(aw8)
    if all_tables:
        total_dining_time = 0
        for table in all_tables:
            dining_time = float(table.dining_time)
            total_dining_time += dining_time
        avg_dine = total_dining_time/len(all_tables)
        dt = 'Average Dining Time: ' + str("{:.2f}".format(avg_dine)) + ' minutes'
        info.append(dt)

    if all_waits:
        first_customer = WaitlistHistory.objects.first()
        first_arrival = first_customer.arrival_time + timedelta(hours = -5)
        fa = 'First customer arrived at ' + str(first_arrival.strftime("%H:%M %p"))
        info.append(fa)
        last_customer = WaitlistHistory.objects.last()
        last_arrival = last_customer.arrival_time + timedelta(hours = -5)
        la = 'Last customer arrived at ' + str(last_arrival.strftime("%H:%M %p"))
        info.append(la)
        total_time_open = last_arrival - first_arrival
        tt_sec = total_time_open.total_seconds()
        tt_hr = int(-(-tt_sec//3600))
        time_intervals = []
        arrival_list = []
        for i in range(tt_hr):
            interval = first_arrival + timedelta(hours = i + 5)
            time_intervals.append(interval)
        for j in range(tt_hr):
            arrivals = 0
            for wait in all_waits:
                if wait.arrival_time > time_intervals[j]:
                    arrivals += 1
            arrival_list.append(arrivals)
        cust_per_hour = []
        for k in range(1,len(arrival_list)):
            val = arrival_list[k-1] - arrival_list[k]
            cust_per_hour.append(val)
            if k == len(arrival_list)-1:
                val = arrival_list[k]
                cust_per_hour.append(val)
        for l in range(len(cust_per_hour)):
            arrival_info = str(cust_per_hour[l]) + ' customers in hour ' + str(l+1)
            info.append(arrival_info)
    context = {
        'info' : info,
        }
    return render(request, "report.html", context)
