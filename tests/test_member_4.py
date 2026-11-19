import pytest
from playwright.sync_api import Page, expect

URL = "https://demo.playwright.dev/todomvc/"


def test_add_task(page: Page):
    page.goto(URL)

    task_input = page.get_by_placeholder(
        "What needs to be done?",
        exact=True,
    )
    task_items = page.locator(".todo-list li")
    task_labels = task_items.locator("label")

    expect(task_items).to_have_count(0)

    task_input.fill("Read testing notes")
    task_input.press("Enter")

    expect(task_items).to_have_count(1)
    expect(task_labels).to_have_text(["Read testing notes"])
    expect(task_input).to_have_value("")
    
    

## second test 

def test_complete_task(page: Page):
    page.goto(URL)

    task_input = page.get_by_placeholder(
        "What needs to be done?",
        exact=True,
    )
    task_items = page.locator(".todo-list li")

    expect(task_items).to_have_count(0)

    task_input.fill("Practise automated testing")
    task_input.press("Enter")

    expect(task_items).to_have_count(1)

    checkbox = task_items.first.get_by_role("checkbox")
    checkbox.check()
    expect(checkbox).to_be_checked()

    page.get_by_role("link", name="Completed", exact=True).click()

    expect(task_items).to_have_count(1)
    expect(task_items.locator("label")).to_have_text(
        ["Practise automated testing"]
    )
    
    
    
# appended test 
    
@pytest.mark.parametrize(
    "task_text",
    ["", " ", "   "],
    ids=["empty", "one-space", "three-spaces"],
)
def test_blank_task_is_not_added(page: Page, task_text: str):
    page.goto(URL)

    task_input = page.get_by_placeholder(
        "What needs to be done?",
        exact=True,
    )
    task_items = page.locator(".todo-list li")

    expect(task_items).to_have_count(0)

    task_input.fill(task_text)
    task_input.press("Enter")

    expect(task_items).to_have_count(0)
    
    
    
# login test

def test_login_with_correct_details(page: Page):
    page.goto("https://the-internet.herokuapp.com/login")

    page.get_by_label("Username").fill("tomsmith")
    page.get_by_label("Password").fill("SuperSecretPassword!")
    page.get_by_role("button", name="Login").click()

    expect(
        page.get_by_role(
            "heading",
            name="Secure Area",
            exact=True,
        )
    ).to_be_visible()
    
    
# incorrect password test

def test_login_with_incorrect_password(page: Page):
    page.goto("https://the-internet.herokuapp.com/login")

    page.get_by_label("Username").fill("tomsmith")
    page.get_by_label("Password").fill("WrongPassword123")
    page.get_by_role("button", name="Login").click()

    expect(
        page.get_by_text("Your password is invalid!")
    ).to_be_visible()

    expect(
        page.get_by_role("button", name="Login")
    ).to_be_visible()
    
    
    
#

def add_task(page: Page, task_name: str):
    task_input = page.get_by_placeholder(
        "What needs to be done?",
        exact=True,
    )
    task_input.fill(task_name)
    task_input.press("Enter")
    
    
    
#

def test_add_two_tasks(page: Page):
    page.goto(URL)
    task_items = page.locator(".todo-list li")

    expect(task_items).to_have_count(0)

    add_task(page, "Read the instructions")
    add_task(page, "Practise the examples")

    expect(task_items).to_have_count(2)
    expect(task_items.locator("label")).to_have_text(
        ["Read the instructions", "Practise the examples"]
    )
    

# additional test 1
# Scenario: deleting an active task removes only that task.
# Condition: fresh session, empty list.
# Values: "Buy printer paper" and "Email the tutor".
# Description: add both, hover the first row and click its delete button.
# Expected outcome: only "Email the tutor" remains and the counter shows 1 item left.

def test_delete_active_task(page: Page):
    page.goto(URL)
    task_items = page.locator(".todo-list li")

    expect(task_items).to_have_count(0)

    add_task(page, "Buy printer paper")
    add_task(page, "Email the tutor")
    expect(task_items).to_have_count(2)

    first_task = task_items.filter(has_text="Buy printer paper")
    first_task.hover()
    first_task.get_by_role("button", name="Delete").click()

    expect(task_items).to_have_count(1)
    expect(task_items.locator("label")).to_have_text(["Email the tutor"])
    expect(page.get_by_test_id("todo-count")).to_have_text("1 item left")

    page.screenshot(
        path="docs/evidence/member-4/extra-test-1-delete-active-task.png",
        full_page=True,
    )


# additional test 2
# Scenario: "Clear completed" removes finished tasks from a mixed list.
# Condition: fresh session, empty list.
# Values: "Water the plants", "Pay the phone bill", "Pack the lunch box".
# Description: add three, complete the first and third, click "Clear completed".
# Expected outcome: only "Pay the phone bill" remains, unchecked, and the button is gone.

def test_clear_completed_from_mixed_list(page: Page):
    page.goto(URL)
    task_items = page.locator(".todo-list li")

    expect(task_items).to_have_count(0)

    add_task(page, "Water the plants")
    add_task(page, "Pay the phone bill")
    add_task(page, "Pack the lunch box")
    expect(task_items).to_have_count(3)

    task_items.nth(0).get_by_role("checkbox").check()
    task_items.nth(2).get_by_role("checkbox").check()
    expect(page.get_by_test_id("todo-count")).to_have_text("1 item left")

    clear_button = page.get_by_role("button", name="Clear completed")
    clear_button.click()

    expect(task_items).to_have_count(1)
    expect(task_items.locator("label")).to_have_text(["Pay the phone bill"])
    expect(task_items.first.get_by_role("checkbox")).not_to_be_checked()
    expect(clear_button).to_be_hidden()

    page.screenshot(
        path="docs/evidence/member-4/extra-test-2-clear-completed.png",
        full_page=True,
    )
