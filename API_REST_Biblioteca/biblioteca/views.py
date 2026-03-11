from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Autor, Libro, Prestamo
from .serializers import AutorSerializer, LibroSerializer, PrestamoSerializer

class AutorViewSet(viewsets.ModelViewSet):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['nacionalidad']
    search_fields = ['nombre', 'apellido']
    ordering_fields = ['nombre', 'fecha_nacimiento']
    ordering = ['apellido', 'nombre']

class LibroViewSet(viewsets.ModelViewSet):
    queryset = Libro.objects.select_related('autor').all()
    serializer_class = LibroSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['genero', 'disponible', 'autor']
    search_fields = ['titulo', 'autor__nombre', 'autor__apellido']
    ordering_fields = ['titulo', 'fecha_publicacion']
    ordering = ['-fecha_publicacion']

    @action(detail=False, methods=['get'])
    def disponibles(self, request):
        libros_disponibles = self.get_queryset().filter(disponible=True)
        page = self.paginate_queryset(libros_disponibles)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(libros_disponibles, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def prestar(self, request, pk=None):
        libro = self.get_object()

        if not libro.disponible:
            return Response(
                {'error': 'Este libro ya se encuentra prestado.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            Prestamo.objects.create(
                libro=libro,
                usuario=request.user
            )
            libro.disponible = False
            libro.save()

        return Response({'mensaje': f'Libro "{libro.titulo}" prestado con éxito.'})

class PrestamoViewSet(viewsets.ModelViewSet):
    serializer_class = PrestamoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['devuelto']
    ordering = ['-fecha_prestamo']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Prestamo.objects.all()
        return Prestamo.objects.filter(usuario=user)

    @action(detail=True, methods=['post'])
    def devolver(self, request, pk=None):
        prestamo = self.get_object()

        if prestamo.devuelto:
            return Response(
                {'error': 'Este préstamo ya fue marcado como devuelto.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            prestamo.devuelto = True
            prestamo.save()
            
            # Actualizamos el estado del libro relacionado
            libro = prestamo.libro
            libro.disponible = True
            libro.save()

        return Response({'mensaje': 'Libro devuelto y disponibilidad actualizada.'})