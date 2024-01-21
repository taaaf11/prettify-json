import json
import requests
import flet as ft


def main(page: ft.Page):
    page.title = "Json Prettifier"

    page.fonts = {
        "JetBrainsMono-Regular": "https://github.com/JetBrains/JetBrainsMono/raw/master/fonts/ttf/JetBrainsMono-Regular.ttf"
    }
    page.theme = ft.Theme(font_family="JetBrainsMono-Regular")
    page.update()

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def add_prettify_json(e):
        default_indent_level = 4
        if indent_level_field.value:
            default_indent_level = indent_level_field.value

        if url_field.value:
            r = requests.get(url_field.value)
            json_data = json.dumps(json.loads(r.content), indent=default_indent_level)
        if json_text_field.value:
            json_data = json.dumps(json.loads(r.content), indent=default_indent_level)

        prettified_json = ft.TextField(value=json_data, multiline=True, max_lines=15)

        if isinstance(page.controls[-1], ft.TextField):
            page.controls[-1] = prettified_json
            page.update()
        else:
            page.add(prettified_json)

    def reset_controls(e):
        url_field.value = ""
        json_text_field.value = ""
        indent_level_field.value = ""

        if isinstance(page.controls[-1], ft.TextField):
            del page.controls[-1]

        page.update()

    url_field = ft.TextField(
        hint_text="Url", text_align=ft.TextAlign.CENTER, width=page.width / 4
    )
    # if the user wants to input as text
    json_text_field = ft.TextField(
        hint_text='JSON "text"',
        text_align=ft.TextAlign.CENTER,
        width=page.width / 4,
        multiline=True,
        max_lines=5,
    )
    indent_level_field = ft.TextField(hint_text="4")

    # grouping text and text field
    url_controls = ft.Row(
        [ft.Text("Url:"), url_field], alignment=ft.MainAxisAlignment.CENTER
    )
    json_text_controls = ft.Row(
        [ft.Text("JSON text:"), json_text_field], alignment=ft.MainAxisAlignment.CENTER
    )
    indent_level_controls = ft.Row(
        [ft.Text("Indent level:"), indent_level_field],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    prettify_btn = ft.TextButton(
        text="Prettify", icon=ft.icons.PALETTE, on_click=add_prettify_json
    )
    reset_btn = ft.TextButton(
        text="Reset", icon=ft.icons.RESTART_ALT, on_click=reset_controls
    )

    page.add(
        url_controls,
        ft.Text("OR"),  # OR,
        json_text_controls,
        ft.Container(
            ft.Divider(thickness=1),
            width=page.width / 4,
            margin=ft.margin.symmetric(10),
        ),
        indent_level_controls,
        ft.Row([prettify_btn, reset_btn], alignment=ft.MainAxisAlignment.CENTER),
    )


ft.app(main)
