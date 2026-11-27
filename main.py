
import flet as ft
import json
import os
from datetime import datetime

# ==========================================
# BUBBLES CAR WASH
# ==========================================

PASSWORD_FILE = "bubbles_password.txt"
SETTINGS_FILE = "bubbles_settings.json"
DATA_FOLDER = "bubbles_daily_data"

DEFAULT_PASSWORD = "bubbles123"

DEFAULT_SETTINGS = {
    "business_name": "BUBBLES CAR WASH",
    "prices": {
        "small": 80,
        "big": 150,
        "taxi": 200
    }
}


def read_json(path, fallback):
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)
                if isinstance(data, dict):
                    return data
    except (OSError, json.JSONDecodeError):
        pass
    return fallback.copy()


def write_json(path, data):
    temp = path + ".tmp"
    with open(temp, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)
    os.replace(temp, path)


def load_password():
    try:
        if os.path.exists(PASSWORD_FILE):
            with open(PASSWORD_FILE, "r", encoding="utf-8") as file:
                password = file.read().strip()
                if password:
                    return password
    except OSError:
        pass
    return DEFAULT_PASSWORD


def save_password(password):
    with open(PASSWORD_FILE, "w", encoding="utf-8") as file:
        file.write(password)


def main(page: ft.Page):

    page.title = "BUBBLES CAR WASH"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#E0F7FA"
    page.padding = 0
    page.scroll = ft.ScrollMode.AUTO

    # LOAD BUSINESS SETTINGS
    settings = read_json(SETTINGS_FILE, DEFAULT_SETTINGS)

    business_name = [
        str(settings.get("business_name", "BUBBLES CAR WASH"))
    ]

    saved_prices = settings.get("prices", {})

    prices = {
        "small": int(saved_prices.get("small", 80)),
        "big": int(saved_prices.get("big", 150)),
        "taxi": int(saved_prices.get("taxi", 200))
    }

    boss_password = [load_password()]

    # DAILY RECORDS
    today = datetime.now().strftime("%Y-%m-%d")

    os.makedirs(DATA_FOLDER, exist_ok=True)

    file_name = os.path.join(
        DATA_FOLDER,
        f"bubbles_washes_{today}.txt"
    )

    summary_file = os.path.join(
        DATA_FOLDER,
        f"bubbles_summary_{today}.json"
    )

    saved_summary = read_json(
        summary_file,
        {
            "counts": {
                "small": 0,
                "big": 0,
                "taxi": 0
            },
            "total_money": 0
        }
    )

    counts = {
        "small": int(saved_summary.get("counts", {}).get("small", 0)),
        "big": int(saved_summary.get("counts", {}).get("big", 0)),
        "taxi": int(saved_summary.get("counts", {}).get("taxi", 0))
    }

    total_money = [
        int(saved_summary.get("total_money", 0))
    ]

    if not os.path.exists(file_name):
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(
                f"=== {business_name[0]} - {today} ===\n"
            )

    # COLOURS
    TEAL = "#00796B"
    BLUE = "#0288D1"
    WHITE = "#FFFFFF"
    DARK = "#004D40"
    ORANGE = "#FF6F00"
    RED = "#C62828"
    GREEN = "#2E7D32"

    message = ft.Text(
        "",
        size=14,
        color=DARK,
        text_align=ft.TextAlign.CENTER
    )

    content = ft.Column(
        [],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=12
    )

    selected_car = [None]
    server_name = [""]

    # SAVE SETTINGS
    def save_settings():
        write_json(
            SETTINGS_FILE,
            {
                "business_name": business_name[0],
                "prices": prices
            }
        )

    # SAVE DAILY TOTALS
    def save_daily_summary():
        write_json(
            summary_file,
            {
                "counts": counts,
                "total_money": total_money[0]
            }
        )

    # HEADER
    def header(title_text, subtitle=""):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "🫧 BUBBLES 🫧",
                        size=12,
                        weight=ft.FontWeight.BOLD,
                        color=WHITE
                    ),
                    ft.Text(
                        title_text,
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=WHITE,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        subtitle,
                        size=13,
                        color=WHITE,
                        text_align=ft.TextAlign.CENTER
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=2
            ),
            bgcolor=TEAL,
            padding=20,
            border_radius=ft.border_radius.only(
                bottom_left=20,
                bottom_right=20
            ),
            width=400
        )

    # BUTTON
    def big_button(label, color, on_click):
        return ft.ElevatedButton(
            text=label,
            bgcolor=color,
            color=WHITE,
            on_click=on_click,
            width=340,
            height=52,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=14)
            )
        )

    # CARD
    def card(child):
        return ft.Container(
            content=child,
            bgcolor=WHITE,
            padding=15,
            border_radius=14,
            margin=ft.margin.symmetric(horizontal=15),
            shadow=ft.BoxShadow(
                blur_radius=8,
                color="#00000022"
            ),
            width=370
        )

    # MESSAGE
    def show_message(text, color=DARK):
        message.value = text
        message.color = color
        page.update()

    def clear_content():
        content.controls.clear()
        message.value = ""

    # ==========================================
    # LOGIN SCREEN
    # ==========================================

    def go_login():

        clear_content()

        content.controls.append(
            header(
                "CAR WASH",
                "Durban • Wash • Shine • Go"
            )
        )

        server_input = ft.TextField(
            label="Server name",
            hint_text="e.g. Sipho",
            prefix_icon=ft.Icons.PERSON
        )

        boss_pass = ft.TextField(
            label="Boss password (boss only)",
            password=True,
            can_reveal_password=True,
            prefix_icon=ft.Icons.LOCK
        )

        def check_server_name():
            name = (server_input.value or "").strip()

            if not name:
                show_message(
                    "Please type the server name first!",
                    RED
                )
                return False

            server_name[0] = name
            return True

        def login_as_boss(e):
            if not check_server_name():
                return

            if (boss_pass.value or "") != boss_password[0]:
                show_message(
                    "Wrong boss password. Please try again.",
                    RED
                )
                return

            show_boss_menu()

        def start_as_staff(e):
            if not check_server_name():
                return

            with open(file_name, "a", encoding="utf-8") as file:
                file.write(
                    f"\n--- Server: {server_name[0]} ---\n"
                )

            go_till()

        content.controls.append(
            card(
                ft.Column(
                    [
                        ft.Text(
                            "Who is serving today?",
                            size=16,
                            weight=ft.FontWeight.BOLD
                        ),
                        server_input,
                        ft.Text(
                            "Are you the boss?",
                            size=14,
                            weight=ft.FontWeight.BOLD
                        ),
                        boss_pass,
                        big_button(
                            "LOGIN AS BOSS 👑",
                            TEAL,
                            login_as_boss
                        ),
                        big_button(
                            "START AS STAFF 🧽",
                            BLUE,
                            start_as_staff
                        ),
                        message
                    ],
                    spacing=10
                )
            )
        )

        page.update()

    # ==========================================
    # BOSS MENU
    # ==========================================

    def show_boss_menu():

        clear_content()

        content.controls.append(
            header(
                "Welcome Boss!",
                f"Server: {server_name[0]}"
            )
        )

        name_field = ft.TextField(
            label="New business name",
            prefix_icon=ft.Icons.STORE
        )

        small_field = ft.TextField(
            label="Small car price (R)",
            keyboard_type=ft.KeyboardType.NUMBER,
            value=str(prices["small"])
        )

        big_field = ft.TextField(
            label="Big car price (R)",
            keyboard_type=ft.KeyboardType.NUMBER,
            value=str(prices["big"])
        )

        taxi_field = ft.TextField(
            label="Taxi price (R)",
            keyboard_type=ft.KeyboardType.NUMBER,
            value=str(prices["taxi"])
        )

        old_field = ft.TextField(
            label="Customer name to correct"
        )

        new_field = ft.TextField(
            label="Correct customer name"
        )

        new_code = ft.TextField(
            label="New boss code",
            password=True,
            can_reveal_password=True
        )

        confirm_code = ft.TextField(
            label="Confirm new boss code",
            password=True,
            can_reveal_password=True
        )

        # CHANGE BUSINESS NAME
        def change_name(e):

            new_name = (name_field.value or "").strip()

            if not new_name:
                show_message(
                    "Please type the new business name.",
                    RED
                )
                return

            business_name[0] = new_name.upper()

            save_settings()

            show_message(
                f"Business name saved: {business_name[0]}",
                GREEN
            )

        # CHANGE PRICES
        def change_prices(e):

            try:
                new_prices = {
                    "small": int(small_field.value),
                    "big": int(big_field.value),
                    "taxi": int(taxi_field.value)
                }

                if any(value < 0 for value in new_prices.values()):
                    raise ValueError

                prices.update(new_prices)

                save_settings()

                show_message(
                    "Prices updated and saved!",
                    GREEN
                )

            except (TypeError, ValueError):
                show_message(
                    "Please enter valid prices using numbers only.",
                    RED
                )

        # CORRECT CUSTOMER NAME
        def fix_customer_name(e):

            old_name = (old_field.value or "").strip()
            corrected_name = (new_field.value or "").strip()

            if not old_name or not corrected_name:
                show_message(
                    "Enter both the old name and the correct name.",
                    RED
                )
                return

            try:
                with open(file_name, "r", encoding="utf-8") as file:
                    data = file.read()

                position = data.rfind(old_name)

                if position == -1:
                    show_message(
                        "That name was not found in today's records.",
                        RED
                    )
                    return

                data = (
                    data[:position]
                    + corrected_name
                    + data[position + len(old_name):]
                )

                with open(file_name, "w", encoding="utf-8") as file:
                    file.write(data)

                show_message(
                    f"Customer name corrected: {old_name} → {corrected_name}",
                    GREEN
                )

            except OSError:
                show_message(
                    "Could not open today's sales file.",
                    RED
                )

        # CHANGE BOSS PASSWORD
        def change_code(e):

            first_code = new_code.value or ""
            second_code = confirm_code.value or ""

            if not first_code:
                show_message("Please type a new boss code.", RED)

            elif len(first_code) < 4:
                show_message(
                    "The boss code must have at least 4 characters.",
                    RED
                )

            elif first_code != second_code:
                show_message(
                    "The two codes do not match.",
                    RED
                )

            else:
                try:
                    save_password(first_code)
                    boss_password[0] = first_code

                    new_code.value = ""
                    confirm_code.value = ""

                    show_message(
                        "New boss code saved successfully!",
                        GREEN
                    )

                except OSError:
                    show_message(
                        "Could not save the new boss code.",
                        RED
                    )

            page.update()

        content.controls.append(
            card(
                ft.Column(
                    [
                        ft.Text(
                            "🏪 1. Business Name",
                            weight=ft.FontWeight.BOLD
                        ),
                        name_field,
                        big_button(
                            "CHANGE NAME",
                            TEAL,
                            change_name
                        ),

                        ft.Divider(),

                        ft.Text(
                            "💰 2. Prices",
                            weight=ft.FontWeight.BOLD
                        ),
                        small_field,
                        big_field,
                        taxi_field,
                        big_button(
                            "UPDATE PRICES",
                            TEAL,
                            change_prices
                        ),

                        ft.Divider(),

                        ft.Text(
                            "✏️ 3. Correct Last Customer Name",
                            weight=ft.FontWeight.BOLD
                        ),
                        old_field,
                        new_field,
                        big_button(
                            "FIX CUSTOMER NAME",
                            BLUE,
                            fix_customer_name
                        ),

                        ft.Divider(),

                        ft.Text(
                            "🔐 4. Change Boss Code",
                            weight=ft.FontWeight.BOLD
                        ),
                        new_code,
                        confirm_code,
                        big_button(
                            "CHANGE BOSS CODE",
                            BLUE,
                            change_code
                        ),

                        ft.Divider(),

                        big_button(
                            "START TILL → GO TO WORK",
                            ORANGE,
                            lambda e: go_till()
                        ),

                        message
                    ],
                    spacing=8
                )
            )
        )

        page.update()

    # ==========================================
    # CAR WASH TILL
    # ==========================================

    def go_till():

        clear_content()

        content.controls.append(
            header(
                business_name[0],
                f"Today: {today} • Server: {server_name[0]}"
            )
        )

        name_input = ft.TextField(
            label="Customer name",
            hint_text="e.g. Thando",
            prefix_icon=ft.Icons.PERSON
        )

        paid_input = ft.TextField(
            label="How much did they pay? (R)",
            keyboard_type=ft.KeyboardType.NUMBER,
            prefix_icon=ft.Icons.ATTACH_MONEY
        )

        result_text = ft.Text(
            "Choose a car type below.",
            size=16,
            weight=ft.FontWeight.BOLD,
            color=TEAL,
            text_align=ft.TextAlign.CENTER
        )

        total_text = ft.Text(
            f"Total sales: R{total_money[0]} | Cars washed: {sum(counts.values())}",
            size=14,
            weight=ft.FontWeight.BOLD
        )

        # SELECT CAR
        def pick_car(car_type):

            selected_car[0] = car_type

            result_text.value = (
                f"Selected: {car_type.upper()} — R{prices[car_type]}"
            )

            page.update()

        # SAVE CUSTOMER AND PAYMENT
        def save_customer(e):

            car_type = selected_car[0]
            customer_name = (name_input.value or "").strip()

            if not car_type:
                show_message(
                    "Choose a car type first.",
                    RED
                )
                return

            if not customer_name:
                show_message(
                    "Please type the customer's name.",
                    RED
                )
                return

            try:
                paid = int(paid_input.value)

                if paid < 0:
                    raise ValueError

            except (TypeError, ValueError):
                show_message(
                    "Enter a valid amount paid using numbers only.",
                    RED
                )
                return

            price = prices[car_type]

            if paid < price:
                show_message(
                    f"Not enough money. The customer still owes R{price - paid}.",
                    RED
                )
                return

            change = paid - price

            now = datetime.now().strftime("%H:%M:%S")

            try:
                with open(file_name, "a", encoding="utf-8") as file:

                    file.write(
                        f"{now} - Server: {server_name[0]} "
                        f"- Name: {customer_name} "
                        f"- Car: {car_type} "
                        f"- Price: R{price} "
                        f"- Paid: R{paid} "
                        f"- Change: R{change}\n"
                    )

                counts[car_type] += 1
                total_money[0] += price

                save_daily_summary()

            except OSError:
                show_message(
                    "Could not save this sale. Please try again.",
                    RED
                )
                return

            result_text.value = (
                f"Thank you, {customer_name}! Give back R{change}."
            )

            total_text.value = (
                f"Total sales: R{total_money[0]} "
                f"| Cars washed: {sum(counts.values())}"
            )

            name_input.value = ""
            paid_input.value = ""
            selected_car[0] = None

            show_message(
                "Customer saved successfully! ✅",
                GREEN
            )

            page.update()

        # CLOSE TILL
        def close_till(e):

            password_field = ft.TextField(
                label="Boss password to close till",
                password=True,
                can_reveal_password=True
            )

            dialog_message = ft.Text(
                "Only the boss can close the till.",
                color=DARK
            )

            def do_close(ev):

                if (password_field.value or "") != boss_password[0]:

                    dialog_message.value = "Incorrect boss password."
                    dialog_message.color = RED

                    page.update()
                    return

                total_cars = sum(counts.values())

                report = (
                    f"\n===== CLOSE REPORT {today} =====\n"
                    f"Business: {business_name[0]}\n"
                    f"Server closing till: {server_name[0]}\n"
                    f"Small cars: {counts['small']}\n"
                    f"Big cars: {counts['big']}\n"
                    f"Taxis: {counts['taxi']}\n"
                    f"Total cars: {total_cars}\n"
                    f"Total sales: R{total_money[0]}\n"
                    f"==============================\n"
                )

                try:
                    with open(file_name, "a", encoding="utf-8") as file:
                        file.write(report)

                except OSError:
                    dialog_message.value = (
                        "Could not save the closing report."
                    )
                    dialog_message.color = RED
                    page.update()
                    return

                page.close(dialog)

                clear_content()

                content.controls.append(
                    header(
                        "TILL CLOSED!",
                        "Today's closing report"
                    )
                )

                content.controls.append(
                    card(
                        ft.Column(
                            [
                                ft.Text(report, size=15),

                                big_button(
                                    "BACK TO LOGIN",
                                    TEAL,
                                    lambda event: go_login()
                                )
                            ],
                            spacing=12
                        )
                    )
                )

                page.update()

            dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Close Till — Boss Only"),
                content=ft.Column(
                    [
                        password_field,
                        dialog_message
                    ],
                    tight=True
                ),
                actions=[
                    ft.TextButton(
                        "CLOSE TILL",
                        on_click=do_close
                    ),
                    ft.TextButton(
                        "CANCEL",
                        on_click=lambda ev: page.close(dialog)
                    )
                ]
            )

            page.open(dialog)

        # TILL SCREEN
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
                            text_align=ft.TextAlign.CENTER
                        ),

                        ft.Text(
                            "Choose car type:",
                            weight=ft.FontWeight.BOLD
                        ),

                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    f"🚗 Small\nR{prices['small']}",
                                    bgcolor=BLUE,
                                    color=WHITE,
                                    height=55,
                                    on_click=lambda e: pick_car("small")
                                ),

                                ft.ElevatedButton(
                                    f"🚙 Big\nR{prices['big']}",
                                    bgcolor=TEAL,
                                    color=WHITE,
                                    height=55,
                                    on_click=lambda e: pick_car("big")
                                ),

                                ft.ElevatedButton(
                                    f"🚕 Taxi\nR{prices['taxi']}",
                                    bgcolor=ORANGE,
                                    color=WHITE,
                                    height=55,
                                    on_click=lambda e: pick_car("taxi")
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            wrap=True
                        ),

                        result_text,
                        name_input,
                        paid_input,

                        big_button(
                            "SAVE CUSTOMER + GIVE CHANGE ✅",
                            TEAL,
                            save_customer
                        ),

                        total_text,
                        message,

                        big_button(
                            "CLOSE TILL (BOSS ONLY) 🔒",
                            RED,
                            close_till
                        )
                    ],
                    spacing=10
                )
            )
        )

        page.update()

    # START APPLICATION
    page.add(content)
    go_login()


# IMPORTANT: FLET APPLICATION START
ft.run(main)

