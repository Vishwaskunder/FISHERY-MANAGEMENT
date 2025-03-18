from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import User
from .models import FishDetails
from .models import Orders
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_admin:
                return redirect('admin_dashboard')  
            elif user.is_user:
                return redirect('user_dashboard') 
        else:
            return render(request, 'login.html')
    return render(request, 'login.html')



@login_required
def admin_dashboard(request):
    
    fishes=FishDetails.objects.all()
    users = User.objects.filter(is_admin=False)
    # users=User.objects.all()
    return render(request,'home_warehouse.html',{'fishes':fishes,'users':users})
    if fishes:
        if users:
            
            
            return render(request, 'admin_dashboard.html',{'fishes':fishes,'users':users})
    if fishes:
        return render(request, 'admin_dashboard.html',{'fishes':fishes})
    if users:
        return render(request,'admin_dashboard.html',{'users':users})
@login_required
def user_dashboard(request):
    fishes=FishDetails.objects.all()
    
    if fishes:
        
        return render(request, 'user_all_fish.html',{'fishes':fishes})
    else:
        
        return render(request,'user_dashboard.html')
    


from django.contrib import messages


@login_required
def add_users_view(request):
    if request.user.is_admin:
        if request.method == "POST":
            name = request.POST.get("name")
            email = request.POST.get("email")
            pass1 = request.POST.get("pass1")
            pass2 = request.POST.get("pass2")
            phonenumber = request.POST.get("phonenumber")
            
            if pass1 == pass2:
                try:
                    if User.objects.filter(username=name).exists():
                        messages.error(request, 'Username already taken!')
                    else:
                        user = User.objects.create_user(username=name, email=email, password=pass1, phone_number=phonenumber)
                        user.is_user = True
                        user.save()
                        messages.success(request, 'Registration successful!')
                except Exception as e:
                    messages.error(request, 'Registration failed')
            else:
                messages.error(request, 'Passwords do not match!')
         
        # fishes=FishDetails.objects.all()
        # users=User.objects.all()      
        
        fishes=FishDetails.objects.all()
        users = User.objects.filter(is_admin=False) 
        return render(request, "add_users.html",{'fishes':fishes,'users':users})
    else:
        
        return render(request,"404.html")

# def add_f_view(request):
#     return render(request, 'add_fish.html') 

@login_required
def add_fish_view(request):
    if request.user.is_admin:
        if request.method == "POST":
            fish_name = request.POST.get("fish_name")
            fish_price = request.POST.get("fish_price")
            fish_quantity = request.POST.get("fish_quantity")
            try:
                if FishDetails.objects.filter(fish_name=fish_name).exists():
                    print("alrt")
                    messages.error(request,"Fish already exist")
                else:
                    print("yess")
                    fish = FishDetails.objects.create(fish_name=fish_name, fish_price=fish_price, fish_quantity=fish_quantity)
                    print("succ")
                    messages.success(request, 'Fish details added successfully!')
            except Exception as e:
                print("exc")
                messages.error(request, 'Failed to add fish details' )
        
        fishes=FishDetails.objects.all()
        users = User.objects.filter(is_admin=False)       
        
     
        return render(request, "add_fish.html",{'fishes':fishes,'users':users})
    else:
        return render(request, "404.html")



@login_required
def update_fish_view(request, fish_id):
    if request.user.is_admin:
        try:
            fish = FishDetails.objects.get(pk=fish_id)
            if request.method == "POST":
                fish.fish_name = request.POST.get("fish_name")
                fish.fish_price = request.POST.get("fish_price")
                fish.fish_quantity = request.POST.get("fish_quantity")
                fish.save()
                messages.success(request, 'Fish details updated successfully!')
                return redirect('admin_dashboard')
            else:
                
                fishes=FishDetails.objects.all()
                users = User.objects.filter(is_admin=False)
                return render(request, "update_fish.html", {'fish': fish ,'users':users})
        except FishDetails.DoesNotExist:
            return render(request, "404.html")
    else:
        return render(request, "404.html")

from django.shortcuts import get_object_or_404

@login_required
def delete_fish_view(request, fish_name):
    if request.user.is_admin:
        try:
            fish = get_object_or_404(FishDetails, fish_name=fish_name)
            fish.delete()
            messages.success(request, 'Fish details deleted successfully!')
        except FishDetails.DoesNotExist:
            messages.error(request, 'Fish details not found!')
        return redirect('admin_dashboard')
    else:
        return render(request, "404.html")






def fishes(request):
    
    
    fishes=FishDetails.objects.all()
    users = User.objects.filter(is_admin=False)     
        
    if request.method=="POST":
        fish_id = request.POST.get('fish_id')
        ob=FishDetails.objects.get(fish_id=fish_id)
        if ob:
            ob.delete()
            return HttpResponseRedirect(request.path_info)
        
        if fishes:
            return render(request,'all_fishes.html',{'fishes':fishes,'users':users})
    else:
        return render(request,'all_fishes.html',{'fishes':fishes,'users':users})

def view_users(request):
    
    fishes=FishDetails.objects.all()
    users = User.objects.filter(is_admin=False)
    
    if request.method=="POST":
        id=request.POST.get('id')
        ob=User.objects.get(id=id)
        if ob:
            ob.delete()

        if users:
            return render(request,'all_users.html',{'fishes':fishes,'users':users})
    else:
        return render(request,'all_users.html',{'fishes':fishes,'users':users})


def edit_fishes(request, fish_name):
    
    if request.user.is_admin:
        if request.method == "POST":
            fish = FishDetails.objects.get(fish_name=fish_name)
            fish.fish_name = request.POST.get("fish_name")
            fish.fish_price = request.POST.get("fish_price")
            fish.fish_quantity = request.POST.get("fish_quantity")
            fish.save()
            return redirect('fishes')
        else:  # Handle GET request
            # You may need to fetch the fish object and pass it to the template
            fish = FishDetails.objects.get(fish_name=fish_name)
            return render(request, "update_fish.html", {'fish': fish})
    else:
        return render(request, "update_fish.html")  # You might want to return an error page or redirect instead
    
    
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import FishDetails

#@login_required
def sell_fish(request, fish_id):
   
    
    if request.method == "POST":
        try:
            # Retrieve the fish instance
            fish = FishDetails.objects.get(pk=fish_id)
            
            users = User.objects.filter(is_admin=False)
            # Get the quantity to sell from the form
            sell_quantity_str = request.POST.get("nq")
            
            if not sell_quantity_str:
                messages.error(request, "Please enter a valid quantity to sell.")
                return render(request, 'user_all_fish.html', {'fishes': fishes,'users':users})
            
            sell_quantity = int(sell_quantity_str)
            
            # Check if the sell quantity is valid
            if sell_quantity <= 0:
                messages.error(request, "Please enter a valid quantity to sell.")
                return render(request, 'user_all_fish.html', {'fishes': fishes,'users':users})
            
            if sell_quantity > fish.fish_quantity:
                messages.error(request, "Insufficient quantity available to sell.")
                return render(request, 'user_all_fish.html', {'fishes': fishes,'users':users})
            
            # Calculate the total amount
            total_amount = sell_quantity * fish.fish_price
            
            # Update the fish quantity
            fish.fish_quantity -= sell_quantity
            fish.save()
            
            
            fishes = FishDetails.objects.all()
            # Show success message
            messages.success(request, f"Fish sold successfully. Total amount: {total_amount}")
            return render(request, 'user_all_fish.html', {'fishes': fishes,'users':users})
        
        except FishDetails.DoesNotExist:
            messages.error(request, "Fish not found.")
            return render(request, 'user_all_fish.html', {'fishes': fishes,'users':users})
        
    else:
        fishes = FishDetails.objects.all()
        messages.error(request, "Invalid request method.")
        return render(request, 'user_all_fish.html', {'fishes': fishes,'users':users})


def all_fishes(request):
    fishes=FishDetails.objects.all()
    users = User.objects.filter(is_admin=False)
    return render(request, 'user_all_fish.html', {'fishes': fishes,'users':users})




# def order(request,fish_id):
#     fish=FishDetails.objects.get(fish_id=fish_id)
#     if request.method=="POST":
#         qty=request.POST.get("quantity")
#         sell_quantity=int(qty)
#         if sell_quantity <= 0:
#             messages.error(request, "Please enter a valid quantity to sell.")
#             return render(request, 'user_all_fish.html', {'fishes': fishes})
            
#         if sell_quantity > fish.fish_quantity:
#             messages.error(request, "Insufficient quantity available to sell.")
#             return render(request, 'user_all_fish.html', {'fishes': fishes})
            
#         total=fish.fish_price*int(qty)
#         order=Orders.objects.create(ordered_by=request.user,quantity=qty,total=total)
#         fish.fish_quantity-=int(qty)
#         fish.save()
#         messages.success(request, f"Fish sold successfully. Total amount: {total}")
#     fishes = FishDetails.objects.all()
#     return render(request, 'user_all_fish.html', {'fishes': fishes})



def order(request,fish_id):
    fish=FishDetails.objects.get(fish_id=fish_id)
    
    if request.method=="POST":
        qty=request.POST.get("qty")
        total=fish.fish_price*int(qty)
        order=Orders.objects.create(ordered_by=request.user,quantity=qty,total=total,fish=fish)
        fish.fish_quantity-=int(qty)
        fish.save()
        fishes=FishDetails.objects.all()
        return render(request, 'user_all_fish.html', {'fishes': fishes})
    return render(request,'order.html',{'fish':fish})

def orderdetails(request):
    orders=Orders.objects.all()
    fishes=FishDetails.objects.all()
    users = User.objects.filter(is_admin=False)
    return render(request,"orderdetails.html",{'orders':orders,'fishes': fishes,'users':users})

def home_warehouse(request):
    fishes=FishDetails.objects.all()
    users = User.objects.filter(is_admin=False)
    return render(request,"home_warehouse.html",{'fishes': fishes,'users':users})
    
    
def view_profile(request,id):
    users=User.objects.filter(id=id)
    return render(request,"view_profile.html",{'users':users})
    
    
def view_profile_fish(request,fish_name):
    fishes=FishDetails.objects.filter(fish_name=fish_name)
    return render(request,"view_profile_fish.html",{'fishes':fishes})
    
    
def admin_dashboard_2(request):
    fishes=FishDetails.objects.all()
    users = User.objects.filter(is_admin=False)
    
    return render(request,"admin_dashboard.html",{'fishes':fishes,'users':users})