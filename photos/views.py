# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseNotFound
from photos.models import Photo, PUBLIC
from photos.forms import PhotoForm
from django.views.generic import View, ListView
from django.db.models import Q


class PhotosQueryset(object):

    def get_photo_queryset(self, request):
        if not request.user.is_authenticated():
            photos = Photo.objects.filter(visibility=PUBLIC)
        elif request.user.is_superuser:
            photos = Photo.objects.all()
        else:
            photos = Photo.objects.filter(
                Q(owner=request.user) | Q(visibility=PUBLIC)
            )
        return photos


class HomeView(View):

    def get(self, request):
        # photos = Photo.objects.all().order_by('-created_at')
        photos = Photo.objects.filter(visibility=PUBLIC).order_by('-created_at')
        context = {"photos": photos[:5]}
        return render(request, "photos/home.html", context)


class DetailView(View, PhotosQueryset):

    def get(self, request, pk):
        """Muestra el detalle de una foto"""
        possible_photos = self.get_photo_queryset(request).filter(pk=pk).select_related('owner')
        photo = possible_photos[0] if len(possible_photos) == 1 else None
        if photo is not None:
            context = {
                "photo": photo
            }
            return render(request, "photos/detail.html", context)
        else:
            return HttpResponseNotFound('No existe la foto')


class NewPhotoView(View):

    @method_decorator(login_required())
    def get(self, request):
        """Crea una nueva foto mediante un formulario"""
        success_message = ''
        form = PhotoForm()
        context = {
            'form': form,
            'success_message': success_message
        }
        return render(request, 'photos/new_photo.html', context)

    @method_decorator(login_required())
    def post(self, request):
        """Crea una nueva foto mediante un formulario"""
        success_message = ''
        photo_with_owner = Photo()
        photo_with_owner.owner = request.user
        form = PhotoForm(request.POST, instance=photo_with_owner)
        if form.is_valid():
            new_photo = form.save()  # Guardar objeto y lo devuelves
            form = PhotoForm()
            success_message = 'Foto guardada'
            success_message += '<a href="{0}" >'.format(reverse('photos:photo_detail', args=[new_photo.pk]))
            success_message += 'Ver foto'
            success_message += '</a>'
        context = {
            'form': form,
            'success_message': success_message
        }
        return render(request, 'photos/new_photo.html', context)


class PhotoListView(View, PhotosQueryset):

    def get(self, request):
        """
        Devuelve:
        - Las fotos públicas si el usuario no está autenticado
        - Las fotos del usuario si está autenticado y las públicas de otros
        - Todas si el usuario autenticado es administrador
        """
        context = {
            'photos': self.get_photo_queryset(request)
        }
        return render(request, 'photos/photos_list.html', context)


class UserPhotosView(ListView):

        model = Photo
        template_name = 'photos/user_photos.html'

        def get_queryset(self):
            query_set = super(UserPhotosView, self).get_queryset()
            return query_set.filter(owner=self.request.user)
