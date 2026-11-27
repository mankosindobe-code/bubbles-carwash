
import flet as ft
import os
from datetime import datetime

PASSWORD_FILE = "bubbles_password.txt"


def load_password():
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, "r") as f:
            code = f.read().strip()
            if code:
                return code
    return "bubbles123"


def save_password(new_code):
    with open(PASSWORD_FILE, "w") as f:
        f.write(new_code)


def main(page: ft.Page):
    page.title = "BUBBLES CAR WASH"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 400
    page.window_height = 780
    page.scroll = ft.ScrollMode.AUTO
    page.bgcolor = "#E0F7FA"
    page.padding = 0

    boss_password = [load_password()]
    business_name = ["BUBBLES CAR WASH"]
    prices = {"small": 80, "big": 150, "taxi": 200}
    counts = {"small": 0, "big": 0, "taxi": 0}
    total_money = [0]
    selected_car = [None]
    server_name = [""]

    today = datetime.now().strftime("%Y-%m-%d")
    file_name = f"bubbles_washes_{today}.txt"

    if not os.path.exists(file_name):
        with open(file_name, "w") as f:
            f.write(f"=== {business_name[0]} - {today} ===\n")

    TEAL = "#00796B"
    BLUE = "#0288D1"
    WHITE = "white"
    DARK = "#004D40"

    def header(title_text, subtitle=""):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "🫧 BUBBLES 🫧",
                        size=12,
                        weight=ft.FontWeight.BOLD,
                        color=WHITE,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        title_text,
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=WHITE,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        subtitle,
                        size=13,
                        color=WHITE,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=2,
            ),
            bgcolor=TEAL,
            padding=ft.padding.all(20),
            border_radius=ft.border_radius.only(
                bottom_left=20,
                bottom_right=20,
            ),
            width=400,
        )

    def big_button(text, color, on_click):
        return ft.ElevatedButton(
            text=text,
            bgcolor=color,
            color=WHITE,
            on_click=on_click,
            width=340,
            height=52,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=14)
            ),
        )

    def card(child):
        return ft.Container(
            content=child,
            bgcolor=WHITE,
            padding=15,
            border_radius=14,
            margin=ft.margin.symmetric(horizontal=15),
            shadow=ft.BoxShadow(
                blur_radius=8,
                color="#00000022",
            ),
            width=370,
        )

    msg = ft.Text(
        "",
        size=14,
        color=DARK,
        text_align=ft.TextAlign.CENTER,
    )

    content = ft.Column(
        [],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=12,
    )

    def show_msg(text, color=DARK):
        msg.value = text
        msg.color = color
        page.update()

    def clear():
        content.controls.clear()

    def go_login():
        clear()
        content.controls.append(
            header("CAR WASH", "Durban • Wash • Shine • Go")
        )

        server_input = ft.TextField(
            label="Server name",
            hint_text="e.g. Sipho",
            prefix_icon=ft.Icons.PERSON,
        )

        boss_pass = ft.TextField(
            label="Boss password (if boss)",
            password=True,
            can_reveal_password=True,
            prefix_icon=ft.Icons.LOCK,
        )

        def start_till():
            if not server_input.value or not server_input.value.strip():
                show_msg("Please type server name first!", "red")
                return

            server_name[0] = server_input.value.strip()

            with open(file_name, "a") as f:
                f.write(f"\n--- Server: {server_name[0]} ---\n")

            go_till()

        def try_boss():
            if not server_input.value or not server_input.value.strip():
                show_msg("Please type server name first!", "red")
                return

            server_name[0] = server_input.value.strip()

            if boss_pass.value == boss_password[0]:
                show_boss_menu()
            elif not boss_pass.value:
                start_till()
            else:
                show_msg("Wrong password! Starting as staff.", "red")
                start_till()

        content.controls.append(
            card(
                ft.Column(
                    [
                        ft.Text(
                            "Who is serving today?",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                        ),
                        server_input,
                        ft.Text(
                            "Are you the boss?",
                            size=14,
                            weight=ft.FontWeight.BOLD,
                        ),
                        boss_pass,
                        big_button(
                            "LOGIN AS BOSS 👑",
                            TEAL,
                            lambda e: try_boss(),
                        ),
                        big_button(
                            "START AS STAFF 🧽",
                            BLUE,
                            lambda e: start_till(),
                        ),
                        msg,
                    ],
                    spacing=10,
                )
            )
        )
        page.update()

    def show_boss_menu():
        clear()

        content.controls.append(
            header("Welcome Boss!", f"Server: {server_name[0]}")
        )

        name_field = ft.TextField(
            label="New business name",
            prefix_icon=ft.Icons.STORE,
        )

        small_field = ft.TextField(
            label="Small car price",
            keyboard_type=ft.KeyboardType.NUMBER,
            value=str(prices["small"]),
        )

        big_field = ft.TextField(
            label="Big car price",
            keyboard_type=ft.KeyboardType.NUMBER,
            value=str(prices["big"]),
        )

        taxi_field = ft.TextField(
            label="Taxi price",
            keyboard_type=ft.KeyboardType.NUMBER,
            value=str(prices["taxi"]),
        )

        old_field = ft.TextField(label="Wrong name")
        new_field = ft.TextField(label="Correct name")
        new_code = ft.TextField(label="New boss code", password=True)
        confirm_code = ft.TextField(label="Confirm new code", password=True)

        def change_name(e):
            if name_field.value and name_field.value.strip():
                business_name[0] = name_field.value.strip().upper()
                show_msg(
                    f"Name changed to: {business_name[0]}",
                    "green",
                )
            page.update()

        def change_prices(e):
            try:
                new_prices = {
                    "small": int(small_field.value),
                    "big": int(big_field.value),
                    "taxi": int(taxi_field.value),
                }

                if any(price < 0 for price in new_prices.values()):
                    raise ValueError

                prices.update(new_prices)
                show_msg("Prices updated!", "green")

            except (ValueError, TypeError):
                show_msg("Please type valid positive numbers!", "red")

            page.update()

        def fix_name(e):
            try:
                if not old_field.value or not new_field.value:
                    show_msg("Enter both names!", "red")
                    return

                with open(file_name, "r") as f:
                    data = f.read()

                pos = data.rfind(old_field.value)

                if pos == -1:
                    show_msg("Name not found!", "red")
                else:
                    data = (
                        data[:pos]
                        + new_field.value
                        + data[pos + len(old_field.value):]
                    )

                    with open(file_name, "w") as f:
                        f.write(data)

                    show_msg(
                        f"Fixed! {old_field.value} -> {new_field.value}",
                        "green",
                    )

            except OSError:
                show_msg("No file for today yet.", "red")

            page.update()

        def change_code(e):
            if not new_code.value:
                show_msg("Type a code!", "red")
            elif len(new_code.value) < 4:
                show_msg("Code must be 4+ characters", "red")
            elif new_code.value != confirm_code.value:
                show_msg("Codes don't match!", "red")
            else:
                boss_password[0] = new_code.value
                save_password(new_code.value)
                show_msg("DONE! New code SAVED!", "green")

            page.update()

        content.controls.append(
            card(
                ft.Column(
                    [
                        ft.Text("🏪 1. Business Name", weight=ft.FontWeight.BOLD),
                        name_field,
                        big_button("Change Name", TEAL, change_name),
                        ft.Divider(),

                        ft.Text("💰 2. Prices", weight=ft.FontWeight.BOLD),
                        small_field,
                        big_field,
                        taxi_field,
                        big_button("Update Prices", TEAL, change_prices),
                        ft.Divider(),

                        ft.Text(
                            "✏️ 3. Fix Last Customer Name",
                            weight=ft.FontWeight.BOLD,
                        ),
                        old_field,
                        new_field,
                        big_button("Fix Name", BLUE, fix_name),
                        ft.Divider(),

                        ft.Text("🔐 4. Change Boss Code", weight=ft.FontWeight.BOLD),
                        new_code,
                        confirm_code,
                        big_button("Change Code", BLUE, change_code),
                        ft.Divider(),

                        big_button(
                            "START TILL → GO TO WORK",
                            "#FF6F00",
                            lambda e: go_till(),
                        ),
                        msg,
                    ],
                    spacing=8,
                )
            )
        )
        page.update()

    def go_till():
        clear()

        content.controls.append(
            header(
                business_name[0],
                f"Today: {today} • Server: {server_name[0]}",
            )
        )

        name_input = ft.TextField(
            label="Customer name",
            hint_text="e.g. Thando",
            prefix_icon=ft.Icons.PERSON,
        )

        paid_input = ft.TextField(
            label="How much did they pay? R",
            keyboard_type=ft.KeyboardType.NUMBER,
            prefix_icon=ft.Icons.ATTACH_MONEY,
        )

        result_text = ft.Text(
            "",
            size=16,
            weight=ft.FontWeight.BOLD,
            color=TEAL,
            text_align=ft.TextAlign.CENTER,
        )

        total_text = ft.Text(
            f"Total so far: R{total_money[0]} | Cars: 0",
            size=14,
            weight=ft.FontWeight.BOLD,
        )

        def pick_car(car_type):
            selected_car[0] = car_type
            result_text.value = (
                f"Selected: {car_type.upper()} - R{prices[car_type]}"
            )
            page.update()

        def save_customer(e):
            if not selected_car[0]:
                show_msg("Choose a car first!", "red")
                return

            if not name_input.value or not name_input.value.strip():
                show_msg("Type customer name!", "red")
                return

            try:
                paid = int(paid_input.value)
            except (ValueError, TypeError):
                show_msg("Type how much they paid!", "red")
                return

            price = prices[selected_car[0]]

            if paid < price:
                show_msg(
                    f"Not enough! Still need R{price - paid}",
                    "red",
                )
                return

            change = paid - price
            counts[selected_car[0]] += 1
            total_money[0] += price

            now = datetime.now().strftime("%H:%M")

            with open(file_name, "a") as f:
                f.write(
                    f"{now} - Name: {name_input.value.strip()} "
                    f"- {selected_car[0]} - Price: R{price} "
                    f"- Paid: R{paid} - Change: R{change}\n"
                )

            result_text.value = (
                f"Thanks {name_input.value.strip()}! Give back R{change}"
            )

            total_text.value = (
                f"Total so far: R{total_money[0]} "
                f"| Cars: {sum(counts.values())}"
            )

            show_msg("Saved! ✅", "green")

            name_input.value = ""
            paid_input.value = ""
            selected_car[0] = None
            page.update()

        def close_till(e):
            pw = ft.TextField(
                label="Boss password to close",
                password=True,
            )

            def do_close(ev):
                if pw.value != boss_password[0]:
                    show_msg("Wrong password!", "red")
                    page.close(dlg)
                    return

                total_cars = sum(counts.values())

                report = (
                    f"\n===== CLOSE REPORT {today} =====\n"
                    f"Server: {server_name[0]}\n"
                    f"Small: {counts['small']} | "
                    f"Big: {counts['big']} | Taxi: {counts['taxi']}\n"
                    f"Total cars: {total_cars}\n"
                    f"Total money: R{total_money[0]}\n"
                )

                with open(file_name, "a") as f:
                    f.write(report)

                page.close(dlg)
                clear()

                content.controls.append(
                    header("TILL CLOSED!", "See you tomorrow!")
                )

                content.controls.append(
                    card(
                        ft.Column(
                            [
                                ft.Text(report, size=15),
                                big_button(
                                    "START NEW DAY",
                                    TEAL,
                                    lambda e: go_login(),
                                ),
                            ]
                        )
                    )
                )

                page.update()

            dlg = ft.AlertDialog(
                title=ft.Text("Close Till - Boss Only"),
                content=pw,
                actions=[
                    ft.TextButton("CLOSE", on_click=do_close),
                    ft.TextButton(
                        "CANCEL",
                        on_click=lambda e: page.close(dlg),
                    ),
                ],
            )

            page.open(dlg)

        content.controls.append(
            card(
                ft.Column(
                    [
                        ft.Text(
                            f"🚗 Small: R{prices['small']}  |  "
                            f"🚙 Big: R{prices['big']}  |  "
                            f"🚕 Taxi: R{prices['taxi']}",
                            size=13,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER,
                        ),

                        ft.Text("Choose car type:", weight=ft.FontWeight.BOLD),

                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    "🚗 Small",
                                    bgcolor=BLUE,
                                    color="white",
                                    height=50,
                                    on_click=lambda e: pick_car("small"),
                                ),
                                ft.ElevatedButton(
                                    "🚙 Big",
                                    bgcolor=TEAL,
                                    color="white",
                                    height=50,
                                    on_click=lambda e: pick_car("big"),
                                ),
                                ft.ElevatedButton(
                                    "🚕 Taxi",
                                    bgcolor="#FF6F00",
                                    color="white",
                                    height=50,
                                    on_click=lambda e: pick_car("taxi"),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),

                        result_text,
                        name_input,
                        paid_input,

                        big_button(
                            "SAVE CUSTOMER + GIVE CHANGE ✅",
                            TEAL,
                            save_customer,
                        ),

                        total_text,
                        msg,

                        big_button(
                            "CLOSE TILL (Boss Only) 🔒",
                            "red",
                            close_till,
                        ),
                    ],
                    spacing=10,
                )
            )
        )

        page.update()

    page.add(content)
    go_login()


ft.run(main)
