# coding: utf-8


def get_text_message(text):
    return {"type": "text", "text": text}


def get_carousel_message(column_list, alt_text):
    return {"type": "template", "altText": alt_text,
                    "template": {
                        "type": "carousel",
                        "columns": column_list
                    }}


def get_carousel_column(image_url, title, text, actions):
    title_cut = title[:37] + "..." if len(title) >= 41 else title
    return {
        "thumbnailImageUrl": image_url,
        "title": title_cut,
        "text": text,
        "actions": actions
    }


