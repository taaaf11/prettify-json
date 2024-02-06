import json
import flet as ft

GITHUB_PROFILE_URL = "https://github.com/taaaf11"


def main(page: ft.Page):
    page.title = "Json Prettifier"

    page.fonts = {
        "JetBrainsMono-NL-NF-Regular": "/fonts/JetBrainsMonoNLNerdFont-Regular.ttf"
    }
    page.theme = ft.Theme(font_family="JetBrainsMono-NL-NF-Regular")
    page.update()

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def add_prettify_json(e):
        default_indent_level = 4
        if indent_level_field.value:
            default_indent_level = int(indent_level_field.value)

        if json_text_field.value:
            json_data = json.dumps(
                json.loads(json_text_field.value), indent=default_indent_level
            )

        prettified_json = ft.TextField(
            value=json_data, height=page.height / 3, multiline=True, max_lines=15
        )

        copy_prettified_btn = ft.TextButton(
            text="Copy",
            icon=ft.icons.COPY_SHARP,
            on_click=lambda _: page.set_clipboard(prettified_json),
        )

        prettified_text_controls.append(copy_prettified_btn)

        if isinstance(page.controls[-1], ft.TextField):
            page.controls[-1] = prettified_json
            page.update()
        else:
            page.add(prettified_json)

    def reset_controls():
        json_text_field.value = ""
        indent_level_field.value = ""

        if isinstance(page.controls[-1], ft.TextField):
            del page.controls[-1]
        
        if prettified_text_controls[-1].text == "Copy":
            del prettified_text_controls[-1]

        page.update()

    def navigate_to_view(e):
        if e.control.data == "home":
            home_view.visible = True
            info_view.visible = False

            home_view_button.icon = ft.icons.HOME
            info_view_button.icon = ft.icons.INFO_OUTLINE

            page.vertical_alignment = ft.MainAxisAlignment.START  # default
        elif e.control.data == "info":
            reset_controls()
            home_view.visible = False
            info_view.visible = True

            home_view_button.icon = ft.icons.HOME_OUTLINED
            info_view_button.icon = ft.icons.INFO

            page.vertical_alignment = ft.MainAxisAlignment.CENTER

        page.update()

    def get_clipboard_content(control: ft.TextField):
        control.value = page.get_clipboard()
        page.update()

    json_text_field = ft.TextField(
        hint_text='JSON "text"',
        text_align=ft.TextAlign.CENTER,
        width=page.width / 4,
        multiline=True,
        max_lines=5,
    )
    indent_level_field = ft.TextField(hint_text="4")

    json_text_controls = ft.Row(
        [
            ft.Text("JSON text:"),
            json_text_field,
            ft.IconButton(
                icon=ft.icons.CONTENT_PASTE,
                on_click=lambda _: get_clipboard_content(json_text_field),
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )
    indent_level_controls = ft.Row(
        [ft.Text("Indent level:"), indent_level_field],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    prettify_btn = ft.TextButton(
        text="Prettify", icon=ft.icons.PALETTE, on_click=add_prettify_json
    )
    reset_btn = ft.TextButton(
        text="Reset", icon=ft.icons.RESTART_ALT, on_click=lambda _: reset_controls()
    )

    prettified_text_controls = [prettify_btn, reset_btn]

    page.appbar = ft.AppBar(
        leading=ft.Container(
            ft.Row(
                [
                    home_view_button := ft.IconButton(
                        icon=ft.icons.HOME,
                        icon_size=25,
                        on_click=navigate_to_view,
                        data="home",
                    ),
                    info_view_button := ft.IconButton(
                        icon=ft.icons.INFO_OUTLINED,
                        icon_size=25,
                        on_click=navigate_to_view,
                        data="info",
                    ),
                ],
            ),
            margin=ft.margin.only(left=10),
        ),
        leading_width=80,
        actions=[
            ft.Container(
                ft.Text("", size=25),
                margin=ft.margin.only(right=30),
                on_click=lambda _: page.launch_url(
                    f"{GITHUB_PROFILE_URL}/prettify-json"
                ),
            )
        ],
    )

    page.spacing = 5

    home_view = ft.Column(
        [
            json_text_controls,
            ft.Container(
                ft.Divider(thickness=1),
                width=page.width / 4,
                margin=ft.margin.symmetric(10),
            ),
            indent_level_controls,
            ft.Row(prettified_text_controls, alignment=ft.MainAxisAlignment.CENTER),
        ],
        visible=True,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    info_view = ft.Column(
        [
            ft.Text("Written by:", size=30),
            ft.CircleAvatar(
                foreground_image_url=f"{GITHUB_PROFILE_URL}.png?size=120px", radius=50
            ),
            ft.Text("Muhammad Altaaf", size=30),
            ft.Text(),
            ft.Text("NOTE: This is a hobby project. As it is written in", size=15),
            ft.Text("pure python, expect it to be slow.", size=15),
        ],
        visible=False,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    page.add(home_view, info_view)


ft.app(main)
