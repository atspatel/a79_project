# ppt_app/views.py
import json
import uuid
import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import FileResponse
from django.utils.timezone import now


from utils.openai_utils import get_gpt_response
from utils.ppt_utils import generate_pptx_strem
from utils.pexels_utils import search_pexels_best_match_url

from .models import Presentation, PresentationSlide
from .serializers import PresentationSerializer
from .presentation_context import presentation_tools, presentation_context

logging.getLogger().setLevel("INFO")


def post_process_slides(slides):
    for slide in slides:
        for placeholder in slide["content"]:
            placeholder["id"] = str(uuid.uuid4())
            # Check if 'name' contains 'picture' (case-insensitive) and if image_url exists
            if "picture" in placeholder["name"].lower():
                if "image_url" not in placeholder or not placeholder["image_url"]:
                    # If image_url does not exist, search for the best match and add it to the content item
                    placeholder["image_url"] = search_pexels_best_match_url(
                        placeholder["value"]
                    )
    return slides


def generate_pptx_from_openai(topic, description, num_slides=4):
    prompt = f"""
    Topic: {topic}
    Description: {description}
    Number of slides: {num_slides}
    """

    # Call OpenAI API to get content for the presentation
    context = presentation_context
    response = get_gpt_response(
        context=[{"role": "assistant", "content": context}],
        message=prompt,
        tools=presentation_tools,
    )
    if response:
        args = json.loads(response.tool_calls[0].function.arguments)
        slides = post_process_slides(**args)
        return slides
    else:
        return "Error generating PowerPoint content."


def process_ppt_obj(ppt_obj):
    ppt_obj.status = "in_progress"
    ppt_obj.save()

    topic = ppt_obj.topic
    description = ppt_obj.description
    num_slides = ppt_obj.num_slides

    slides = generate_pptx_from_openai(topic, description, num_slides)

    PresentationSlide.objects.filter(presentation=ppt_obj).delete()

    for i, slide in enumerate(slides):
        slide_obj = PresentationSlide.objects.create(
            presentation=ppt_obj,
            layout_id=slide.get("layout_id"),
            layout_name=slide.get("layout_name"),
            content=slide.get("content"),
            index=i,
        )
        logging.info(
            f"slide content saved to db, presentatin_id: {ppt_obj.id}, index:{i}"
        )
    ppt_obj.status = "completed"
    ppt_obj.save()
    return True


class PresentationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        if id:
            try:
                presentation = Presentation.objects.get(id=id, user=request.user)
            except Presentation.DoesNotExist:
                return Response({"detail": "Not found."}, 404)
            return Response(PresentationSerializer(presentation).data, 200)
        return Response(
            {"detail": "Bad request. Presentation ID is required for GET."}, 400
        )

    def post(self, request):
        # Ensure the request context is passed to the serializer
        serializer = PresentationSerializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            ppt_obj = serializer.save()
            process_ppt_obj(ppt_obj)
            return Response(serializer.data, 201)

        return Response(serializer.errors, 400)

    def put(self, request, id=None):
        if not id:
            return Response(
                {"detail": "Bad request. Presentation ID is required for PUT."}, 400
            )

        # Retrieve the presentation to update
        try:
            presentation = Presentation.objects.get(id=id, user=request.user)
        except Presentation.DoesNotExist:
            return Response({"detail": "Not found."}, 404)

        # Update the fields
        serializer = PresentationSerializer(
            presentation, data=request.data, partial=True
        )  # Allow partial updates
        if serializer.is_valid():
            presentation = serializer.save()
            return Response(PresentationSerializer(presentation).data, 200)
        return Response(serializer.errors, 400)


class PresentationDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            presentation = Presentation.objects.get(id=id, user=request.user)
            slides = PresentationSlide.objects.filter(
                presentation=presentation
            ).order_by("index")
            theme = presentation.theme

            # Prepare slide data to pass to the ppt generation function
            slide_data = [
                {"layout_id": slide.layout_id, "content": slide.content}
                for slide in slides
            ]
            pptx_stream = generate_pptx_strem(slides=slide_data, theme=theme)

            # Return the PPTX file as a response
            title = presentation.topic[:50]
            current_datetime = now().strftime("%Y/%m/%d_%H-%M-%S")
            filename = f"{title}_{current_datetime}.pptx"

            response = FileResponse(
                pptx_stream,
                content_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            )
            response["Content-Disposition"] = f'attachment; filename="{filename}"'
            return response

        except Presentation.DoesNotExist:
            return Response({"detail": "Presentation not found"}, 404)
        except PresentationSlide.DoesNotExist:
            return Response({"detail": "Slides not found for the presentation"}, 404)
