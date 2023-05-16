from rest_framework.views import APIView, Request, Response, status
from .models import Pet
from .serializers import PetSerializer
from groups.models import Group
from traits.models import Trait
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404


class PetViews(APIView, PageNumberPagination):
    def get(self, request: Request) -> Response:
        trait_param = request.query_params.get("trait", None)

        pets = Pet.objects.all()
        trait_result = Trait.objects.filter(name__iexact=trait_param)

        if trait_param is None and trait_result == []:
            pets = trait_result

        if trait_result:
            pets = Pet.objects.filter(traits=trait_result[0].id)

        result_page = self.paginate_queryset(pets, request)
        serializer = PetSerializer(instance=result_page, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = PetSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        group = serializer.validated_data.pop("group")
        traits = serializer.validated_data.pop("traits")

        group_obj = Group.objects.filter(
            scientific_name__iexact=group["scientific_name"]
        ).first()

        if not group_obj:
            group_obj = Group.objects.create(**group)

        pet_obj = Pet.objects.create(
            **serializer.validated_data,
            group=group_obj,
        )

        for trait_dict in traits:
            trait_obj = Trait.objects.filter(name__iexact=trait_dict["name"]).first()

            if not trait_obj:
                trait_obj = Trait.objects.create(**trait_dict)
            pet_obj.traits.add(trait_obj)

        serializer = PetSerializer(pet_obj)

        return Response(serializer.data, status.HTTP_201_CREATED)


class PetDetailsViews(APIView):
    def get(self, request: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)
        serializer = PetSerializer(pet)

        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, request: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)
        serializer = PetSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        group_data = serializer.validated_data.pop("group", None)

        traits_data = serializer.validated_data.pop("traits", None)

        if group_data:
            find_group = Group.objects.filter(
                scientific_name__iexact=group_data["scientific_name"]
            ).first()

            print(find_group)
            print("=" * 50)
            if find_group:
                pet.group = find_group

            if not find_group:
                created_group = Group.objects.create(**group_data)
                pet.group = created_group

        if traits_data:
            trait_list = []
            for trait in traits_data:
                trait_dict = Trait.objects.filter(name__iexact=trait["name"]).first()

                if not trait_dict:
                    trait_dict = Trait.objects.create(**trait)
                trait_list.append(trait_dict)
                pet.traits.set(trait_list)

        for key, value in serializer.validated_data.items():
            setattr(pet, key, value)

        pet.save()
        serializer = PetSerializer(pet)

        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)
        pet.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
