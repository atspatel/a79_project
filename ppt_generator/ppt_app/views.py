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


def process_presentation_obj(presentation_obj):
    if presentation_obj.status in ['in_progress', 'completed']:
        return False
    
    presentation_obj.status = "in_progress"
    presentation_obj.save()
    try:
        topic = presentation_obj.topic
        description = presentation_obj.description
        num_slides = presentation_obj.num_slides

        slides = generate_pptx_from_openai(topic, description, num_slides)

        PresentationSlide.objects.filter(presentation=presentation_obj).delete()

        for i, slide in enumerate(slides):
            slide_obj = PresentationSlide.objects.create(
                presentation=presentation_obj,
                layout_id=slide.get("layout_id"),
                layout_name=slide.get("layout_name"),
                content=slide.get("content"),
                index=i,
            )
            logging.info(
                f"slide content saved to db, presentatin_id: {presentation_obj.id}, index:{i}"
            )
        presentation_obj.status = "completed"
        presentation_obj.save()
        return True
    except Exception as e:
        # Log the exception and update the status to 'failed'
        logging.error(f"Error processing PPT for presentation_id: {presentation_obj.id}, Error: {e}")
        presentation_obj.status = "failed"
        presentation_obj.save()
        return False


class PPTCreateResponseThen(Response):
    def __init__(self, data, then_callback, obj, **kwargs):
        super().__init__(data, **kwargs)
        self.obj = obj
        self.then_callback = then_callback

    def close(self):
        super().close()
        self.then_callback(self.obj)
        
class PresentationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        if id:
            try:
                presentation = Presentation.objects.get(id=id, user=request.user)
            except Presentation.DoesNotExist:
                return Response({"detail": "Not found."}, 404)
            return Response(PresentationSerializer(presentation).data, 200)
        
        presentations = Presentation.objects.filter(user=request.user).order_by('-create_time')
        serializer = PresentationSerializer(presentations, many=True)
        return Response(serializer.data, 200)

    def post(self, request):
        # Ensure the request context is passed to the serializer
        serializer = PresentationSerializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            presentation = serializer.save()
            return PPTCreateResponseThen(
                    serializer.data,
                    process_presentation_obj,
                    presentation
                )

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

        # Only allow 'topic', 'description', 'num_slides', and 'theme' fields to be updated
        valid_fields = ['topic', 'description', 'num_slides', 'theme']
        filtered_data = {key: value for key, value in request.data.items() if key in valid_fields}

        # If no valid fields are provided, return a bad request response
        if not filtered_data:
            return Response(
                {"detail": "Only 'topic', 'description', 'num_slides', and 'theme' fields can be updated."}, 400
            )

        # Check if 'topic', 'description', or 'num_slides' are being updated
        update_content = False
        if 'topic' in filtered_data and presentation.topic != filtered_data['topic']:
            update_content = True
        if 'description' in filtered_data and presentation.description != filtered_data['description']:
            update_content = True
        if 'num_slides' in filtered_data:
            current_num_slides = presentation.num_slides
            new_num_slides = filtered_data['num_slides']
            if current_num_slides != new_num_slides:
                update_content = True    

        # Update the fields
        serializer = PresentationSerializer(
            presentation, data=filtered_data, partial=True
        )  # Allow partial updates
        if serializer.is_valid():
            presentation = serializer.save()
            if update_content:
                presentation.status = 'pending'
                presentation.save()
                return PPTCreateResponseThen(
                    serializer.data,
                    process_presentation_obj,
                    presentation
                )
            return Response(PresentationSerializer(presentation).data, 200)
        return Response(serializer.errors, 400)


class PresentationDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            presentation = Presentation.objects.get(id=id, user=request.user)
            if presentation.status != "completed":
                return Response({"detail": "Presentation status is not completed"}, 404)
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
