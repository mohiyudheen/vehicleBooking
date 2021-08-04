from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from .models import Vehicle,bookingDate,UserProfile
from rest_framework.response import Response
from datetime import timedelta,datetime
import time

# Create your views here.

def Diff(li1, li2):
    return list(set(li1) - set(li2)) + list(set(li2) - set(li1))
def check_availabe(vehicleRegNumber,bookingUptoDate):
    bookingData=list(bookingDate.objects.filter(vehicle__vehicleRegNumber=vehicleRegNumber).values_list('datetimeFrom','datetimeTo'))
    bookedDates=[]
    ###################### list all booked dates ##################################
    for dt in bookingData:
        sdate = dt[0].replace(tzinfo=None)
        edate=dt[1].replace(tzinfo=None)+timedelta(days=1)
        a=[(sdate+timedelta(days=x)).strftime('%Y-%m-%d') for x in range((edate-sdate).days)]
        bookedDates+=a
    ##################### list all date ##########################################
    sdate = datetime.now().replace(tzinfo=None)
    edate=bookingUptoDate.replace(tzinfo=None)+timedelta(days=1)
    allDays=[(sdate+timedelta(days=x)).strftime('%Y-%m-%d') for x in range((edate-sdate).days)]
    ##################### list all unbooked Date #################################
    remaingDays=Diff(allDays,bookedDates)
    ############ to sort date #######################################################
    dates = [datetime.strptime(ts, "%Y-%m-%d") for ts in remaingDays]
    dates.sort()
    sorteddates = [datetime.strftime(ts, "%Y-%m-%d") for ts in dates]
    return sorteddates
    

class availability(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request, *args, **kwargs):
        vehicleDetails=Vehicle.objects.filter(availability=True)
        result=[]
        try:
            for data in vehicleDetails:
                sorteddates=check_availabe(data.vehicleRegNumber,data.bookingUpto)
                result.append({'vehicle':data.vehicleName,'vehicleRegNumber':data.vehicleRegNumber,'available':sorteddates})
        except Exception as e:
                return Response({'status':400,'error':str(e)})
        return Response(result)
    
class book(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        sdate=request.data.get('datefrom')
        edate=request.data.get('dateto')
        vehicleRegNumber=request.data.get('vehicleRegNumber')
        vehData=Vehicle.objects.get(vehicleRegNumber=vehicleRegNumber)
        sorteddates=check_availabe(vehicleRegNumber,vehData.bookingUpto)
        sdate=datetime.strptime(sdate, '%Y-%m-%d')
        edate=datetime.strptime(edate, '%Y-%m-%d')
        dateUpto=edate+timedelta(days=1)
        allDays=[(sdate+timedelta(days=x)).strftime('%Y-%m-%d') for x in range((dateUpto-sdate).days)]
        for i in allDays:
            if i not in sorteddates:
                return Response({'status':404,'message':'this day already booked.please try another'})
        userData=UserProfile.objects.get(user=request.user)
        bookingDate.objects.create(customer=userData,vehicle=vehData,datetimeFrom=sdate,datetimeTo=edate,bookingStatus=True)
        return Response({'status':200,'message':'success'})
        