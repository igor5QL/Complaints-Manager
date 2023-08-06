from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, CreateTicketForm, UpdateForm, CloseForm
from .models import Ticket, TicketUpdate
from django.db.models import Q, Count, Avg, FloatField, Max
import pandas as pd
from plotly.offline import plot
import plotly.express as px
import datetime



def home(request):


    if request.user.is_authenticated:
        return redirect ('search')
    # Handle login first
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('search')
        else:
            messages.error(request, 'If you do not have the permissions to create tickets, click on "search" above for readonly')
            return redirect('home')
    
    return render(request, 'pages/home.html')

# @login_required(login_url='home')
def search(request):
    searched_ticket = None

    if request.method == 'POST':
        # Ticket search for homepage
        complaint_id = request.POST['complaint_id_search']
        account_number = request.POST['account_number_search']
        company = request.POST['company_search']
        state = request.POST['state_search']
        agent_id_name = request.POST['agent_id_search']

        # Constructing the query dynamically
        query = Q()

        if complaint_id:
            query &= Q(id=complaint_id)
        if account_number:
            query &= Q(account_number=account_number)
        if company:
            query &= Q(company__contains=company)
        if state:
            query &= Q(customer_state__contains=state)
        if agent_id_name:
            agent = User.objects.filter(username=agent_id_name).first()
            if agent:
                query &= Q(agent_id=agent)
            
            # If an agent doesn't exist, None will return and the AND statement will not apply to agent. Meaning, if a valid complaint id is 
            # searched with a bogus agent_id, there will still be a return because the filter will be &= None. So if agent does not exist,
            # populate nothing.
            else:
                searched_ticket = Ticket.objects.none()
                context = {'tickets': tickets, 'searched_ticket': searched_ticket}
                return render(request, 'pages/search.html', context)
        
        # Filter tickets based on the constructed query
        searched_ticket = Ticket.objects.filter(query)
    context = {'tickets': tickets, 'searched_ticket': searched_ticket}
    return render(request, 'pages/search.html', context)


# @login_required(login_url='home')
def tickets(request, pk):
    # closeform = CloseForm()
    ticket = Ticket.objects.get(id=pk)
    agent_id = ticket.agent_id
    # The most recent tickets made by the agent, not including the current one open. This is to be displayed on the left
    most_recent = Ticket.objects.filter(Q(agent_id=agent_id) & ~Q(id=pk)).order_by('-updated_at')[:5]

    # Get all updates for the current ticket. List descending order
    updates = ticket.updates.all().order_by('-updated_at')  # Use the 'updates' related_name from TicketUpdate model

    context = {
        'ticket': ticket,
        'most_recent': most_recent,
        'updates': updates,
 
    }
    return render(request, 'pages/tickets.html', context)

@login_required(login_url='home')
def update_ticket(request, pk):
    ticket = Ticket.objects.get(id=pk)

    form = UpdateForm()
    if request.method == 'POST':
        form = UpdateForm(request.POST, request.FILES)
        if form.is_valid():
            ticket_update = form.save(commit=False)
            ticket_update.ticket = ticket
            ticket_update.updated_by = request.user
            ticket_update.save()
            return redirect('tickets', pk)
        else:
            print(form.errors)

    context = {'form':form}
    return render(request, 'pages/update.html', context)



@login_required(login_url='home')
def create_ticket(request):
    form = CreateTicketForm()

    if request.method == 'POST':
        form = CreateTicketForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.agent_id = User.objects.get(username=request.user)
            instance.save()
            redirect_ticket = instance.id
            messages.success(request, f'Ticket {redirect_ticket} has been created.')
            return redirect('tickets', redirect_ticket)
        else:
            print(form.errors)

    context = {'form':form}
    return render(request, 'pages/create.html', context)

def logout_user(request):
    logout(request)
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # login the user after sign up
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'welcome')
                return redirect('home')
            else:
                messages.success(request, 'oh oh something went wrong.')
                return redirect('home')
        else:
            messages.success(request, 'sorry, something went wrong')
            return redirect('register')
    context = {'form': form}
    return render(request, 'pages/register.html', context)

@login_required(login_url='home')
def close(request, pk):
    ticket = Ticket.objects.get(id=pk)
    form = CloseForm(initial={'status': ticket.status})

    if request.method == 'POST':
        form = CloseForm(request.POST, request.FILES)
        if form.is_valid():
            ticket_update = form.save(commit=False)
            ticket_update.ticket = ticket
            ticket_update.updated_by = request.user
            ticket_update.save()
            ticket.status = ticket_update.status
            ticket.save()
            return redirect('tickets', pk)

    context = {'form': form, 'pk': pk}
    return render(request, 'pages/close.html', context)


def stats(request, pk):
    curr_user = request.user
    # Set default formatting
    def update_format(fig):
        fig.update_layout(
            bargap=0.2, plot_bgcolor="#0f172a", 
            paper_bgcolor="#0f172a",
            template="plotly_dark",
            yaxis=dict(title="Complaint"),
            xaxis=dict(title="", tickformat='%Y-%m'),
            legend=dict(font=dict(color="white"), title=""))
    
        fig.update_xaxes(
            title_font_color="white",
            mirror=True,
            ticks='outside',
            color='white',
            showline=True,
            linecolor="#0f172a",
            gridcolor='#0f172a')
    
        fig.update_yaxes(
            title_font_color="white",
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor="#0f172a",
            gridcolor='#1E202E',
            color='white',
            tickmode='linear',
            dtick=1)
    
    # Histogram for ticket creation
    user_stats_hist = Ticket.objects.filter(agent_id=request.user)
    tickets_hist = user_stats_hist.values('complaint_date').annotate(complaint_id=Count('id', distinct=True))
    fig_hist = px.histogram(tickets_hist, x="complaint_date", nbins=12, width=1200, height=400,)
    
    update_format(fig_hist)
    
    count_hist = fig_hist.to_html(config={
                            'displayModeBar': False,
                            'displaylogo': False,                                       
                            'modeBarButtonsToRemove': ['zoom2d', 'hoverCompareCartesian', 'hoverClosestCartesian', 'toggleSpikelines']
                        })
    
    # Bar for closed ticket reasons
    user_stats_bar = Ticket.objects.filter(agent_id=request.user, complaint_date__gte='2022-01-01', complaint_date__lte=datetime.datetime.now().date())

    tickets_bar_2 = user_stats_bar.values('complaint_date', 'status').annotate(complaint_id=Count('id', distinct=True))
    fig_bar = px.bar(tickets_bar_2, x="complaint_date", y="complaint_id",color="status",  width=1200, height=400,template='plotly_dark')
    update_format(fig_bar)
    count_bar = fig_bar.to_html(config={
                            'displayModeBar': False,
                            'displaylogo': False,                                       
                            'modeBarButtonsToRemove': ['zoom2d', 'hoverCompareCartesian', 'hoverClosestCartesian', 'toggleSpikelines']
                        })



    today = datetime.date.today()
    today = today.replace(day=1)
    this_month = today.month
    four_mo_ago = today.replace(month= this_month - 4).strftime("%Y-%m-%d")
    one_mo_ago = today.replace(month= this_month - 1).strftime("%Y-%m-%d")
    first_of_month = today.replace(day=1)
    last_month_end = first_of_month - datetime.timedelta(days=1)
    last_month_sta = last_month_end.replace(day=1)

    # Last months numbers
    user_stats_last_mo = Ticket.objects.filter(agent_id=request.user, complaint_date__gte='2022-12-01', complaint_date__lte='2022-12-31')
    counts_last_mo = user_stats_last_mo.values('complaint_date').annotate(complaint_count_last_mo=Count('id'))
    # Returns a dictionary {'complaint_count__avg': 1.28}
    average_last_mo = round(counts_last_mo.aggregate(Avg('complaint_count_last_mo'))['complaint_count_last_mo__avg'], 2)

    # 3 months prior to last month
    user_stats_prior_3mo = Ticket.objects.filter(agent_id=request.user, complaint_date__gte='2022-09-01', complaint_date__lte='2022-12-01')
    counts_prior_3mo = user_stats_prior_3mo.values('complaint_date').annotate(complaint_count_prior_3mo=Count('id'))
    average_prior_3mo = round(counts_prior_3mo.aggregate(Avg('complaint_count_prior_3mo'))['complaint_count_prior_3mo__avg'],2)

    if (average_prior_3mo - average_last_mo) > 0:
        mo_diff = str(round(average_prior_3mo - average_last_mo, 2)) + ' increase'
    else:
        mo_diff = str(round(average_prior_3mo - average_last_mo,2)) + ' decrease'

    context = {
    'count_bar': count_bar, 
    'count_hist': count_hist,
    'curr_user':curr_user, 
    'average_last_mo':average_last_mo,
    'average_prior_3mo':average_prior_3mo,
    'mo_diff':mo_diff}
    
    return render(request, 'pages/stats.html', context)


