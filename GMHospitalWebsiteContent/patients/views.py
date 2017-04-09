from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from patients.models import Data, Appointments
import datetime

def index(request):
    return HttpResponse("Hello World!")

def patientRegistration(request):
    return render(request, "pateintRegistration.html")

def opGenerationForm(request):
    return render(request, "generateOP.html")

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
            data['patinetToken'] = "0"
            data['color'] = "green"
            return JsonResponse(data)
        else:
            data['message'] = "Patient record not found please register the user first"
            data['color'] = "red"
            return JsonResponse(data)
    else:
        return