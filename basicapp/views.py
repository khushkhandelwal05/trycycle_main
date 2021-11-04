from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import userinfo, Bookings, accessories, contact_us, discount, cycles
from collections import deque, namedtuple
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from django.contrib.auth import update_session_auth_hash

# Create your views here.
def index(request):
    return render(request,'TryCycle.html')

def register(request):

    if request.method == 'POST':
        username=request.POST['username']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        phone_no=request.POST['phone_no']
        reg_no=request.POST['reg_no']
        room_no=request.POST['room_no']
        password1=request.POST['password1']
        password2=request.POST['password2']
        email=request.POST['email']
        if password1==password2:
            if User.objects.filter(username=username).exists():
                print("username taken")
            elif User.objects.filter(email=email).exists():
                print('email taken')
            else:
                user = User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
                userinfos = userinfo(email=email,first_name=first_name,last_name=last_name,reg_no=reg_no,room_no=room_no,phone_no=phone_no)
                user.save()
                userinfos.save()
                messages.info(request,'user created')
                print("user created")
            return redirect('/')
        else:
            messages.info(request,'Password does not match')
            return redirect('/')
            print("Password does not match")

    else:
        print("NOT POST")
        return redirect('/')

def logout(request):
    auth.logout(request)
    return redirect('/')

def login(request):

    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return redirect("/")
        else:
            messages.error(request,'invalid cedentials')
            return redirect('/')
    else:
        return redirect('/')

def fare(request):
        return render(request,'/fare')


def rent_now(request):
    if request.method == 'POST':
        username = None
        username = request.user.username
        date=request.POST['date']
        cht=request.POST['cht']
        startpt=request.POST['check']
        lastpt=request.POST['end']
        dis_code = request.POST['dis_code']
        inf = float('inf')
        Edge = namedtuple('Edge', 'start, end, cost')
        discount_list = discount.objects.order_by('code')


        def make_edge(start, end, cost=1):
            return Edge(start, end, cost)


        class Graph:
            def __init__(self, edges):
                wrong_edges = [i for i in edges if len(i) not in [2, 3]]
                if wrong_edges:
                    raise ValueError('Wrong edges data: {}'.format(wrong_edges))

                self.edges = [make_edge(*edge) for edge in edges]

            @property
            def vertices(self):
                return set(
                    sum(
                        ([edge.start, edge.end] for edge in self.edges), []
                    )
                )

            def get_node_pairs(self, n1, n2, both_ends=True):
                if both_ends:
                    node_pairs = [[n1, n2], [n2, n1]]
                else:
                    node_pairs = [[n1, n2]]
                return node_pairs

            def remove_edge(self, n1, n2, both_ends=True):
                node_pairs = self.get_node_pairs(n1, n2, both_ends)
                edges = self.edges[:]
                for edge in edges:
                    if [edge.start, edge.end] in node_pairs:
                        self.edges.remove(edge)

            def add_edge(self, n1, n2, cost=1, both_ends=True):
                node_pairs = self.get_node_pairs(n1, n2, both_ends)
                for edge in self.edges:
                    if [edge.start, edge.end] in node_pairs:
                        return ValueError('Edge {} {} already exists'.format(n1, n2))

                self.edges.append(Edge(start=n1, end=n2, cost=cost))
                if both_ends:
                    self.edges.append(Edge(start=n2, end=n1, cost=cost))

            @property
            def neighbours(self):
                neighbours = {vertex: set() for vertex in self.vertices}
                for edge in self.edges:
                    neighbours[edge.start].add((edge.end, edge.cost))

                return neighbours

            def dijkstra(self, source, dest):
                assert source in self.vertices, 'Such source node doesn\'t exist'
                distances = {vertex: inf for vertex in self.vertices}
                previous_vertices = {
                    vertex: None for vertex in self.vertices
                }
                distances[source] = 0
                vertices = self.vertices.copy()

                while vertices:
                    current_vertex = min(
                        vertices, key=lambda vertex: distances[vertex])
                    vertices.remove(current_vertex)
                    if distances[current_vertex] == inf:
                        break
                    for neighbour, cost in self.neighbours[current_vertex]:
                        alternative_route = distances[current_vertex] + cost
                        if alternative_route < distances[neighbour]:
                            distances[neighbour] = alternative_route
                            previous_vertices[neighbour] = current_vertex

                path, current_vertex = deque(), dest
                while previous_vertices[current_vertex] is not None:
                    path.appendleft(current_vertex)
                    current_vertex = previous_vertices[current_vertex]
                if path:
                    path.appendleft(current_vertex)
                return path

        graph = Graph([
            ("Main Building", "SMV", 3),  ("Main Building", "Technology Tower", 5),  ("Main Building", "Health Center", 3), ("SMV", "Technology Tower", 3),
            ("SMV","SJT", 10), ("Technology Tower", "SJT", 5), ("Technology Tower", "Health Center", 6),  ("SJT", "Men's Hostel", 10),
            ("Men's Hostel", "Health Center", 10), ("Technology Tower", "Main Building", 5)])

        graphdat=([
            ("Main Building", "SMV", 3),  ("Main Building", "Technology Tower", 5),  ("Main Building", "Health Center", 3), ("SMV", "Technology Tower", 3),
            ("SMV","SJT", 10), ("Technology Tower", "SJT", 5), ("Technology Tower", "Health Center", 6),  ("SJT", "Men's Hostel", 10),
            ("Men's Hostel", "Health Center", 10), ("Technology Tower", "Main Building", 5)])
        tot=0
        tab=graph.dijkstra(startpt,lastpt)
        for i in range(0,len(tab)-1):
            for j in graphdat:
                if(tab[i]==j[0] and tab[i+1]==j[1]):
                    tot=tot+j[2]
        dis = 0
        for disc in discount_list:
            if disc.code == dis_code:
                if disc.offer == True:
                    dis = disc.dis_amt
        tot = tot - (tot*0.01*dis)
        tot = str(tot)

        booked=Bookings(user=username,date=date,startpt=startpt,lastpt=lastpt,cht=cht,tot=tot)
        booked.save()
        return redirect('/')

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        feed=request.POST['feed']
        contacted=contact_us(name=name,email=email,subject=subject,feed=feed)

        contacted.save()
        return redirect('/')

def mybookings(request):
    booking_list = Bookings.objects.order_by('id')
    date_dict = {'bookings':booking_list}
    return render(request,'mybookings.html',context=date_dict)

def bicycle(request):
    cycle_list = cycles.objects.order_by('name')
    return render(request,'bicycle.html', context = { 'cycle' : cycle_list })

def mydiscount(request):
    discount_list = discount.objects.order_by('code')
    return render(request,'discount.html',context = { 'discount' : discount_list})

def myaccessories(request):
    accessories_list = accessories.objects.order_by('name')
    return render(request,'accessory.html',context = { 'accessories' : accessories_list })


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return render(request, 'change-password-done.html')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })

def search(request):
    if request.method == 'POST':
        name = request.POST['name']
    user_list = userinfo.objects.order_by('first_name')
    gname = str(name)
    tot_dict = {'users': user_list, 'uname': gname}
    print(name)
    print(user_list)
    return render(request, 'user_search.html', context=tot_dict)
