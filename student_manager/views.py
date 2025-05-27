"""
Views for handling exam registration-related actions:
- Students can view, create, and update their exam registration.
- Teachers can view a summary of all registrations.
"""

# Relative Path: student_manager/views.py


from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ExamRegistration
from .serializers import ExamRegistrationSerializer


class MyExamRegistration(APIView):
    """
    Allows a logged-in student to:
    - GET: View their current exam registration (if exists)
    - POST: Submit a new exam registration (once only)
    - PUT: Update their existing registration
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Returns the student's registration status and user snapshot.
        """
        user_data = {
            "full_name": request.user.full_name,
            "varsity_id": request.user.varsity_id,
            "session": request.user.session,
            "phone_number": request.user.phone_number,
        }

        try:
            reg = ExamRegistration.objects.get(user=request.user)
            serialized = ExamRegistrationSerializer(reg)
            return Response({
                "registered": True,
                "registration": serialized.data,
                "user": user_data,
            })
        except ExamRegistration.DoesNotExist:
            return Response({
                "registered": False,
                "user": user_data,
            })

    def post(self, request):
        """
        Allows the student to create a new exam registration if one doesn't already exist.
        """
        if ExamRegistration.objects.filter(user=request.user).exists():
            return Response(
                {"detail": "You have already registered."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ExamRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            # Auto-link to user so snapshot fields populate
            serializer.save(user=request.user)
            return Response(
                {"registered": True, "registration": serializer.data},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """
        Allows the student to update an existing exam registration.
        """
        try:
            reg = ExamRegistration.objects.get(user=request.user)
        except ExamRegistration.DoesNotExist:
            return Response(
                {"detail": "No registration found to update."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ExamRegistrationSerializer(reg, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  # Triggers model's save() for snapshot update
            return Response(
                {"registered": True, "registration": serializer.data},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExamRegistrationSummary(APIView):
    """
    Returns all exam registrations — restricted to teacher users.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Allows teachers to view a summary of all student registrations.
        """
        if request.user.role != "teacher":
            return Response(
                {"detail": "You do not have permission to view this."},
                status=status.HTTP_403_FORBIDDEN
            )

        registrations = ExamRegistration.objects.select_related("user").all()
        serialized = ExamRegistrationSerializer(registrations, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
