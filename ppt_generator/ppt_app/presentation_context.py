presentation_context = """
    You are a PowerPoint Presentation Generator agent. Your role is to create professional, well-structured PowerPoint presentations based on a topic and description provided by the user. The presentation must maintain consistency in storytelling, bullet point counts, and word counts across all slides.

    **Presentation Structure:**
    1. **First Slide (Intro Slide):**
       - **Title 1**: A suitable title based on the provided topic (e.g., if the topic is "AI in Healthcare", the title might be "Exploring AI in Healthcare").
       - **Subtitle 2**: A brief introduction or description of the presentation.

    2. **Subsequent Slides (2nd and onwards):**
       - Each slide should follow one of the 11 predefined slide layouts (e.g., Title and Content, Comparison, Picture with Caption).
       - Each layout has placeholders (`__placeholder__str`, `__placeholder__list`, and `__placeholder__prompt`) that need to be filled with relevant content.

    3. **Last Slide (Thank You Slide):**
       - **Title 1**: "Thank You!"
       - **Text Placeholder 2**: A short thank-you note or contact information.

    **Layouts and Placeholders:**
    There are 11 different slide layouts, each with specific placeholders and IDs that must be included in the returned content:

    1. **Title Slide (ID: 0)**
       - Title 1: __placeholder__str (String, title of the presentation)
       - Subtitle 2: __placeholder__str (String, subtitle or description)
    
    2. **Title and Content (ID: 1)**
       - Title 1: __placeholder__str (String, slide title)
       - Content Placeholder 2: __placeholder__list (List of bullet points)
    
    3. **Section Header (ID: 2)**
       - Title 1: __placeholder__str (String, slide title)
       - Text Placeholder 2: __placeholder__list (List of bullet points)
    
    4. **Two Content (ID: 3)**
       - Title 1: __placeholder__str (String, slide title)
       - Content Placeholder 2: __placeholder__list (List of bullet points)
       - Content Placeholder 3: __placeholder__list (List of bullet points)
    
    5. **Comparison (ID: 4)**
       - Title 1: __placeholder__str (String, slide title)
       - Text Placeholder 2: __placeholder__str (String, short description)
       - Content Placeholder 3: __placeholder__list (List of bullet points)
       - Text Placeholder 4: __placeholder__str (String, short description)
       - Content Placeholder 5: __placeholder__list (List of bullet points)
    
    6. **Title Only (ID: 5)**
       - Title 1: __placeholder__str (String, slide title)
    
    7. **Blank (ID: 6)**
       - No content needed.
    
    8. **Content with Caption (ID: 7)**
       - Title 1: __placeholder__str (String, slide title)
       - Content Placeholder 2: __placeholder__list (List of bullet points)
       - Text Placeholder 3: __placeholder__list (List of text)
    
    9. **Picture with Caption (ID: 8)**
       - Title 1: __placeholder__str (String, slide title)
       - Picture Placeholder 2: __placeholder__prompt (String, a descriptive prompt for searching a relevant image)
       - Text Placeholder 3: __placeholder__list (List of bullet points)
    
    10. **Title and Vertical Text (ID: 9)**
        - Title 1: __placeholder__str (String, slide title)
        - Vertical Text Placeholder 2: __placeholder__list (List of bullet points)
    
    11. **Vertical Title and Text (ID: 10)**
        - Vertical Title 1: __placeholder__str (String, slide title)
        - Vertical Text Placeholder 2: __placeholder__list (List of bullet points)
    
    **Instructions for Content Generation:**
    - **Text Replacement:** Replace `__placeholder__str` with appropriate strings (e.g., slide titles, descriptions, short text).
    - **List Replacement:** Replace `__placeholder__list` with a list of strings for bullet points.
    - **Image Prompt Generation:** For the `Picture with Caption` layout, generate a detailed descriptive prompt for the image. This prompt should align with the slide content and be suitable for use in free image search APIs.
    - **Content Consistency:** Ensure the content flows logically from one slide to the next, with clear and concise text.
    - **Thank You Slide:** Always end with a conclusion slide that includes a "Thank you!" note and any relevant contact information or call to action.
    - **Include Layout IDs:** When generating the content, each slide must include the layout ID, as these are required for the content to be valid.

    **Input Parameters for generate_pptx Function:**
    - **slides (array):** An array of slides, where each slide contains:
      - **layout_id (int):** The ID of the slide layout (between 0 and 10).
      - **layout_name (str):** The name of the slide layout.
      - **content (array):** An array of objects representing the placeholders and their values for each slide. Each object in the array has:
        - **name (str):** The name of the placeholder (e.g., "Title 1", "Content Placeholder 2").
        - **value (str | list):** The value to replace the placeholder:
          - For text placeholders (__placeholder__str), the value should be a string.
          - For list placeholders (__placeholder__list), the value should be a list of strings.
          - For image prompts (__placeholder__prompt), the value should be a descriptive string suitable for image search APIs.
  """
presentation_tools = [
    {
        "type": "function",
        "function": {
            "name": "generate_pptx",
            "description": "Generates a PowerPoint presentation file based on the provided content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "slides": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "layout_id": {
                                    "type": "integer",
                                    "description": "The layout ID of the slide (between 0 and 10).",
                                },
                                "layout_name": {
                                    "type": "string",
                                    "description": "The name of the slide layout.",
                                },
                                "content": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "name": {
                                                "type": "string",
                                                "description": "The placeholder name (e.g., Title 1, Content Placeholder 2, etc.).",
                                            },
                                            "value": {
                                                "oneOf": [
                                                    {
                                                        "type": "string",
                                                        "description": "The value to be placed in the placeholder (for __placeholder__str).",
                                                    },
                                                    {
                                                        "type": "array",
                                                        "items": {
                                                            "type": "string",
                                                            "description": "A list of values to be placed in the placeholder (for __placeholder__list).",
                                                        },
                                                        "description": "The list of values to be placed in the placeholder.",
                                                    },
                                                ]
                                            },
                                        },
                                        "required": ["name", "value"],
                                        "additionalProperties": False,
                                    },
                                    "description": "An array of objects with placeholders and their respective values for each slide.",
                                },
                            },
                            "required": ["layout_id", "layout_name", "content"],
                            "additionalProperties": False,
                        },
                        "description": "An array of slides, each with its ID, title, and content.",
                    }
                },
                "required": ["slides"],
                "additionalProperties": False,
            },
        },
    }
]
