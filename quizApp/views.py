from django.shortcuts import render

# Create your views here.
import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Question, QuizResult
from .serializers import QuestionSerializer, QuizResultSerializer, UserRegisterSerializer, UserLoginSerializer
from django.contrib.auth.models import User

# View for user registration
class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully!", "username": user.username}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View for user login
class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(username=serializer.validated_data['username'])
            if user.check_password(serializer.validated_data['password']):
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                return Response({"access": access_token, "refresh": str(refresh)}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View for taking the quiz
class TakeQuizView(APIView):
    def get(self, request):
        # Select 5 random questions
        questions = random.sample(list(Question.objects.all()), 5)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        answers = request.data.get("answers")  # List of answers
        score = 0

        questions = Question.objects.filter(id__in=[q["id"] for q in answers])

        # Evaluate the user's answers
        for question, answer in zip(questions, answers):
            if question.correct_answer == answer["selected_option"]:
                score += 1

        percentage = (score / 5) * 100

        # Save the result to the database
        quiz_result = QuizResult.objects.create(user=user, score=score, percentage=percentage)

        # Feedback message based on score
        if score <= 2:
            message = "Please try again!"
        elif score == 3:
            message = "Good job!"
        elif score == 4:
            message = "Excellent work!"
        elif score == 5:
            message = "You are a genius!"

        return Response({
            "score": score,
            "percentage": percentage,
            "message": message
        })

# View for showing quiz results
class QuizResultsView(APIView):
    def get(self, request):
        user = request.user
        results = QuizResult.objects.filter(user=user)
        serializer = QuizResultSerializer(results, many=True)

        # Calculate average, highest, and lowest scores
        scores = [result.score for result in results]
        if scores:
            avg_score = sum(scores) / len(scores)
            highest_score = max(scores)
            lowest_score = min(scores)
        else:
            avg_score = highest_score = lowest_score = 0

        return Response({
            "results": serializer.data,
            "average_score": avg_score,
            "highest_score": highest_score,
            "lowest_score": lowest_score
        })
