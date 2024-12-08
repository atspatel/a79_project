import logging
from openai import OpenAI
import json

import config


def get_completion(prompt=None, context=[], model="gpt-4", tools=None):
    try:
        # Prepare the message history
        messages = context[:]
        if prompt:
            messages.append({"role": "user", "content": prompt})

        # Make the OpenAI API call to get the completion response
        client = OpenAI(api_key=config.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=model, messages=messages, temperature=0, tools=tools
        )
        return response
    except Exception as e:
        logging.error(f"Error in getting completion: {e}")
        return None


def get_gpt_response(context, message, tools=[], thread=[]):
    response = get_completion(
        prompt=message,
        context=context + thread,
        tools=None if not tools or len(tools) == 0 else tools,
    )
    try:
        return response.choices[0].message
    except:
        return response
