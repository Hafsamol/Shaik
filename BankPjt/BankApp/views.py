from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Register
# Create your views here.
def Login(request):
    return render(request,'Login.html')
def home(request):
    return render(request,'registation.html')

def Registeration(request):
    if request.method=='POST':
        a=int(request.POST['accno'])
        e = request.POST['uname']
        flag = 0
        details = Register.objects.all()
        for i in details:
            if i.accno == int(a)  or i.uname==e :
                flag = 1
            else:
                print("No match")
        if flag==0:
            b = request.POST['name']
            c = request.POST['addr']
            d = request.POST['bal']
            f = request.POST['pwd']
            if int(d) >= 1000:
                if int(d)%100==0:
                    data = Register.objects.create(accno=a, name=b, addr=c, bal=d,uname=e,pwd=f)
                    data.save()
                    #alert("Saved")
                    return redirect(login)
                else:
                    return HttpResponse("Amount must be multiple of 100")
            else:
                return HttpResponse("Min Deposit Amount 1000")
        else:
            return HttpResponse("Already Exist Account Number")
    else:
        return render(request, 'BankRegister.html')


from django.contrib import messages
def login(request):
    if request.method=='POST':
        u=request.POST['uname']
        p=request.POST['pwd']
        print("hxgasfdsaghd", u)
        print("hxgasfdsaghd", p)
        try:
            print("try1")
            data=Register.objects.get(uname=u)
            print("try2")
            if data.pwd==p:
                request.session['id']=u
                print("data.pwd", data.pwd)
                return redirect(home)
            else:
                return HttpResponse("Wrong Password")
        except Exception:
            #return HttpResponse("<script>alert('Wrong UserName')</script>")
            messages.info(request,"Wrong Username")
            return redirect(home)

        #request.session['id'] = u
        return render(request, 'Login.html')
    else:
        return render(request, 'Login.html')



def home(request):
    if 'id' in request.session:
        u = request.session['id']
        print("session profile", u)
        data = Register.objects.filter(uname=u)
        return render(request, 'profile.html', {'d': data})
    else:
        return redirect(login)

def update(request):
    if request.method=='POST':
        u = request.session['id']
        n=request.POST['name']
        a=request.POST['addr']
        print("session after update", u)
        Register.objects.filter(uname=u).update(name=n,addr=a)
        return redirect(home)
    else:
        u = request.session['id']
        print("session before update", u)
        data = Register.objects.filter(uname=u)
        return render(request, 'update.html', {'d': data})

def depositupdate(request):
    if request.method == 'POST':
        u = request.session['id']
        a = request.POST['amt']
        if int(a)%100==0:
            try:
                details = Register.objects.get(uname=u)
                details.bal = details.bal + int(a)
                print(details.bal)
                Register.objects.filter(uname=u).update(bal=details.bal)
                return redirect(home)
            except Exception:
                return HttpResponse("No Details")
        else:
            return HttpResponse("Amount must be multiples of 100")
        #return redirect(home)
    else:
        u = request.session['id']
        print("session before update", u)
        data = Register.objects.filter(uname=u)
        return render(request, 'deposit.html', {'d': data})


def withdrawupdate(request):
    if request.method == 'POST':
        u = request.session['id']
        a = request.POST['amt']
        if int(a)%100==0 :
            try:
                details = Register.objects.get(uname=u)
                details.bal = details.bal - int(a)
                if details.bal>=1000:
                    Register.objects.filter(uname=u).update(bal=details.bal)
                    return redirect(home)
                else:
                    return HttpResponse("You cannot withdraw")
            except Exception:
                return HttpResponse("No Details")
        else:
            return HttpResponse("Enter multiples of 100")
        #return redirect(home)
    else:
        u = request.session['id']
        print("session before update", u)
        data = Register.objects.filter(uname=u)
        return render(request, 'withdraw.html', {'d': data})

def transfer(request):
    if request.method == 'POST':
        u = request.session['id']
        tname = request.POST['tname']
        a = request.POST['amt']
        if u!=tname:
            if int(a) % 100 == 0:
                try:
                    owner = Register.objects.get(uname=u)
                    tfr = Register.objects.get(uname=tname)
                    owner.bal = owner.bal - int(a)
                    tfr.bal = tfr.bal + int(a)
                    if owner.bal >= 1000:
                        Register.objects.filter(uname=u).update(bal=owner.bal)
                        Register.objects.filter(uname=tname).update(bal=tfr.bal)
                        return redirect(home)
                    else:
                        return HttpResponse("You cannot Transfer")
                except Exception:
                    return HttpResponse("No Details")
            else:
                return HttpResponse("Amount must be multiples of 100")
        else:
            return HttpResponse("You are trying to transfer same account")
    else:
        u = request.session['id']
        data = Register.objects.filter(uname=u)
        return render(request, 'transfer.html', {'d': data})


def balance(request):
        u = request.session['id']
        data = Register.objects.filter(uname=u)
        return render(request, 'balance.html', {'d': data})


def logout(request):
    if 'id' in request.session:
        request.session.flush()
    return redirect(home)
