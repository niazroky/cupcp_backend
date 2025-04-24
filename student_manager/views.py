# student_manager/views.py

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ExamRegistration
from .serializers import ExamRegistrationSerializer

class MyExamRegistration(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_data = {
            "full_name": request.user.full_name,
            "varsity_id": request.user.varsity_id,
            "session": request.user.session,
        }
        try:
            reg = ExamRegistration.objects.get(user=request.user)
            return Response({
                "registered": True,
                "registration": ExamRegistrationSerializer(reg).data,
                "user": user_data
            })
        except ExamRegistration.DoesNotExist:
            return Response({
                "registered": False,
                "user": user_data
            })


    def post(self, request):
        if ExamRegistration.objects.filter(user=request.user).exists():
            return Response(
                {"detail": "You have already registered."},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = ExamRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                {"registered": True, "registration": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            reg = ExamRegistration.objects.get(user=request.user)
        except ExamRegistration.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ExamRegistrationSerializer(reg, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"registered": True, "registration": serializer.data},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExamRegistrationSummary(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # only teachers may view this
        if request.user.role != "teacher":
            return Response(
                {"detail": "You do not have permission to view this."},
                status=status.HTTP_403_FORBIDDEN
            )

        # pull in all registrations
        regs = ExamRegistration.objects.select_related("user").all()
        data = ExamRegistrationSerializer(regs, many=True).data
        return Response(data, status=status.HTTP_200_OK)