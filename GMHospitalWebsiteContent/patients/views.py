from django.http import HttpResponse
from django.http import JsonResponse
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from patients.models import Data, Appointments, Logins, AdminLogin
import datetime
import string
import random

def index(request):   #test view
    return HttpResponse("Hello World!")

def patientRegistration(request): #view to return patient registration form
    if 'uname' in request.session:
        return render(request, "pateintRegistration.html", {"user":request.session['uname']})
    else:
        return redirect("userLogin")

def opGenerationForm(request):
    if 'uname' in request.session:
        return render(request, "generateOP.html", {"user":request.session['uname']})
    else:
        return redirect("userLogin")

def adminLoginForm(request):
    return render(request, "adminLogin.html")

def logPatientDetailsToDB(request):
    if request.method == "POST":
        aadharNo = request.POST.get('aadharNo')
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d %H:%M:%S")
        instance = Data(aadharNumber = aadharNo, surname= surname, name= name, sex= gender, Age= age, Address= address, mobile= mobile, dateOfRegister= date)
        instance.save()
        resultSet = Data.objects.filter(aadharNumber= aadharNo)
        patientId = resultSet.values_list()[0][0]
        return render(request,'patientDetails.html',{'patientId': patientId, 'aadharNo': aadharNo, 'surname': surname, 'name': name, 'gender': gender, 'age': age, 'address': address, 'mobile': mobile, 'DOR': date})
    else:
        return


def patientDetails(request):
    if request.method == "POST":
        aadharNo = request.POST.get('aadharNo')
        patientId = request.POST.get('patiendId')

        if(aadharNo):
            resultSet = Data.objects.filter(aadharNumber= aadharNo)
        else:
            resultSet = Data.objects.filter(patinetID= patientId)

        patientId = resultSet.values_list()[0][0]
        aadharNo = resultSet.values_list()[0][1]
        surname = resultSet.values_list()[0][2]
        name = resultSet.values_list()[0][3]
        gender = resultSet.values_list()[0][4]
        age = resultSet.values_list()[0][5]
        address = resultSet.values_list()[0][6]
        mobile = resultSet.values_list()[0][7]
        date = resultSet.values_list()[0][8]
        return render(request,'patientDetails.html',{'patientId': patientId, 'aadharNo': aadharNo, 'surname': surname, 'name': name, 'gender': gender, 'age': age, 'address': address, 'mobile': mobile, 'DOR': date})
    else:
        return


def generateOP(request):
    if request.method == "POST":
        resultSet = None
        data = {}
        type = request.POST.get('type')
        identifier = request.POST.get('identifier')
        problems = request.POST.get('problems')
        if(type == "1"):
            resultSet = Data.objects.filter(patientID= identifier)
        elif(type == "2"):
            resultSet = Data.objects.filter(mobile= identifier)
        elif(type == "3"):
            resultSet = Data.objects.filter(aadharNumber= identifier)

        if(resultSet):
            patientId = resultSet.values_list()[0][0]
            now = datetime.datetime.now()
            date = now.strftime("%Y-%m-%d %H:%M:%S")
            appointment = Appointments(patientID= patientId, dateOfAppointment= date, Problems= problems)
            appointment.save()
            data['message'] = "Op Generated successfully"
            data['patientToken'] = "0"
            data['color'] = "green"
            return JsonResponse(data)
        else:
            data['message'] = "Patient record not found please register the user first"
            data['color'] = "red"
            return JsonResponse(data)
    else:
        return

def userLoginForm(request):
    if 'uname' in request.session:
        return redirect("opGenerationForm")
    else:
        return render(request, "login.html")

def userManagement(request):
    return render(request, "userManagement.html")

def adminManagement(request):
    if 'aname' in request.session:
        return render(request, "adminPage.html", {"aname": request.session['aname']})
    else:
        return redirect("adminLogin")

def userVerification(request):
    data = {}
    email = request.POST.get("email")
    password = request.POST.get("passwd")
    resultSet = Logins.objects.filter(email= email)
    if(resultSet):
        if(resultSet.values_list()[0][1] == password):
            request.session["uname"] = resultSet.values_list()[0][0]
            return redirect("opGenerationForm")
        else:
            data["message"] = "Please enter the correct password"
            return JsonResponse(data)
    else:
        data["message"] = "User does not exists"
        return JsonResponse(data)

def adminVerification(request):
    if request.method == "POST":
        data = {}
        userName = request.POST.get("adminEmail")
        password = request.POST.get("passwd")
        resultSet = AdminLogin.objects.filter(email= userName)
        if (resultSet):
            if (resultSet.values_list()[0][1] == password):
                request.session["aname"] = resultSet.values_list()[0][0]
                return redirect("adminManagement")
            else:
                data["flag"] = "0"
                data["message"] = "Please enter the correct password"
                return JsonResponse(data)
        else:
            data["message"] = "Admin does not exists"
            return JsonResponse(data)
    else:
        return HttpResponseNotFound('<h1>No Page Here</h1>')

def forgetPassword(request):
    if request.method == "POST" and request.is_ajax():
        resultSet = None
        data = {}
        toAddr= None
        resetEmail = request.POST.get('email')
        type = request.POST.get("type")
        if (type == "1"):
            resultSet = Logins.objects.filter(email= resetEmail)
            if(resultSet):
                toAddr = resultSet.values_list()[0][3]
        else:
            resultSet = AdminLogin.objects.filter(email= resetEmail)
            if(resultSet):
                toAddr = resultSet.values_list()[0][2]

        if (resultSet):
            chars = string.ascii_uppercase + string.digits
            msg = ''.join(random.choice(chars) for _ in range(8))
            Logins.objects.filter(email = toAddr).update(password = msg)
            send_mail(
                'hello',
                'New Password to reset Your Account is:'+msg,
                'kplphc@gmail.com',
                [toAddr],
                fail_silently=False,
            )
            data["message"] = "new password has been sent to email address "+toAddr
            return JsonResponse(data)
        else:
            data["message"] = "Please enter a vaild email"
            return JsonResponse(data)
    else:
        return

def userRegistrationForm(request):
    return render(request, "userRegistration.html")

def createUser(request):
    if request.method == "POST" and request.is_ajax():
        data = {}
        loginAlias = request.POST.get("loginAlias")
        password = request.POST.get("password")
        gmail = request.POST.get("email")
        try:
            instance = Logins(loginAlias= loginAlias, password= password, approved= "0", email= gmail)
            instance.save()
        except:
            data["message"] = "SQl Error"
            return JsonResponse(data)
        data["message"] = "user created successfully, you can login once it is approved by Admin"
        return JsonResponse(data)
    else:
        return

def promoteToAdmin(request):
    if request.method == "POST" and request.is_ajax():
        email = request.POST.get("email")
        data = {}
        resultSet = Logins.objects.filter(email= email)
        if(resultSet):
            loginAlias = resultSet.values_list()[0][1]
            password = resultSet.values_list()[0][2]
            uemail = resultSet.values_list()[0][4]
            try:
                instance = AdminLogin(loginAlias= loginAlias, password= password, email= uemail)
                instance.save()
            except:
                data["message"] = "SQL Error Occurred"
                return JsonResponse(data)
            Logins.objects.filter(email= email).delete()
            data["message"] = "pormoted to admin successfully"
            return JsonResponse(data)
        else:
            data["message"] = "User not found"
            return JsonResponse(data)
    else:
        return

def resetPassword(request):
    if request.method == "POST" and request.is_ajax():
        data = {}
        flag = 0
        email = request.POST.get("email")
        prevPassword = request.POST.get("oldPassword")
        newPassword = request.POST.get("newPassword")
        type = request.POST.get("type")
        if(type == "1"):
            resultSet = Logins.objects.filter(email= email)
            if(resultSet):
                flag =1
        if(type == "0"):
            resultSet = Logins.objects.filter(email=email)
            if(resultSet):
                flag = 1
        if(flag):
            if type == "1":
                resultSet = Logins.objects.filter(email=email)
                password = resultSet.values_list()[0][1]
                if prevPassword == password:
                    Logins.objects.filter(email= email).update(password= newPassword)
                    data["message"] = "Password updated successfully"
                    return JsonResponse(data)
                else:
                    data["message"] = "entered password is wrong, please enter the correct password"
                    return JsonResponse(data)
            if type == "0":
                resultSet = Logins.objects.filter(email=email)
                password = resultSet.values_list()[0][1]
                if prevPassword == password:
                    AdminLogin.objects.filter(email=email).update(password=newPassword)
                    data["message"] = "Password updated successfully"
                    return JsonResponse(data)
                else:
                    data["message"] = "entered password is wrong, please enter the correct password"
                    return JsonResponse(data)
        else:
            data["message"] = "email "+email+" doesn't exists, please enter a valid email"
            return JsonResponse(data)

    else:
        return

def listOfRequests(request):
    if request.method == "POST" and request.is_ajax():
        data = {}
        i = 0
        resultSet = Logins.objects.filter(approved= 0)
        if(resultSet):
            for row in resultSet:
                data["user"+i] = row.loginAlias
                data["email"+i] = row.email
                i=i+1
            data["totalCount"] = i
            return JsonResponse(data)
        else:
            data["message"]="no new requests"
            return JsonResponse(data)
    else:
        HttpResponseNotFound('<h1>No Page Here</h1>')

def logout(request):
    data = {}
    try:
        del request.session['uname']
        request.session.modified = True
        return redirect("userLogin")
    except KeyError:
        data["message"] = "session del error"
        return JsonResponse(data)

def aLogout(request):
    data = {}
    try:
        del request.session['aname']
        request.session.modified = True
        return redirect("adminLogin")
    except KeyError:
        data["message"] = "session del error"
        return JsonResponse(data)

def pendingApprovals(request):
    if request.method == "POST" and request.is_ajax():
        data = {}
        count = 1
        try:
            resultSet = Logins.objects.filter(approved=0)
            for entry in resultSet:
                name = entry.loginAlias
                email = entry.email
                data["name"+str(count)] = name
                data["email"+str(count)] =email
                count=count+1
            data["count"] = count-1
            return JsonResponse(data)
        except:
            data["message"] = "server side error"
            return JsonResponse(data)
    else:
        HttpResponseNotFound('<h1>No Page Here</h1>')