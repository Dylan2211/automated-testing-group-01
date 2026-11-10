from playwright.sync_api import Page, expect

# Define the missing URL variable globally
URL = "https://demo.playwright.dev/todomvc/"

def add_task(page: Page, task_name: str):
    task_input = page.get_by_placeholder(
        "What needs to be done?",
        exact=True,
    )
    task_input.fill(task_name)
    task_input.press("Enter")

def test_recorded_task(page: Page):
    page.goto(URL)

    task_input = page.get_by_placeholder(
        "What needs to be done?",
        exact=True,
    )
    task_input.fill("Try the recorder")
    task_input.press("Enter") 

    task_labels = page.locator(".todo-list li label")
    expect(task_labels).to_have_text(["Try the recorder"])

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


from playwright.sync_api import Page, expect

URL = "https://playwright.dev"

def add_task(page: Page, task_name: str):
    task_input = page.get_by_placeholder(
        "What needs to be done?",
        exact=True,
    )
    task_input.fill(task_name)
    task_input.press("Enter")
    page.screenshot(
    path="docs/evidence/member-2/extra-test-1-active-filter.png",
    full_page=True,
)

def test_recorded_task(page: Page):
    page.goto(URL)

    task_input = page.get_by_placeholder(
        "What needs to be done?",
        exact=True,
    )
    task_input.fill("Try the recorder")
    task_input.press("Enter")

    task_labels = page.locator(".todo-list li label")
    expect(task_labels).to_have_text(["Try the recorder"])
    page.screenshot(
    path="docs/evidence/member-2/extra-test-2-delete-task.png",
    full_page=True,
)

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

def test_mark_all_complete(page: Page):
    page.goto(URL)
    task_items = page.locator(".todo-list li")
    
    # 1. Prepare tasks
    add_task(page, "Task One")
    add_task(page, "Task Two")
    
    # 2. Click the whole-list control to mark all complete
    # In TodoMVC, this is the "toggle-all" arrow icon next to the input field
    page.get_by_label("Mark all as complete").click()
    
    # 3. Assert all prepared tasks are completed
    # Completed tasks gain the "completed" class in TodoMVC
    expect(task_items).to_have_class(["completed", "completed"])

def test_mark_all_active_again(page: Page):
    page.goto(URL)
    task_items = page.locator(".todo-list li")
    toggle_all = page.get_by_label("Mark all as complete")
    
    # 1. Prepare tasks and complete them
    add_task(page, "Task One")
    add_task(page, "Task Two")
    toggle_all.click()
    expect(task_items).to_have_class(["completed", "completed"])
    
    # 2. Click the control again to reverse whole-list completion
    toggle_all.click()
    
    # 3. Assert checkboxes are no longer selected (classes should be completely empty)
    expect(task_items).to_have_class(["", ""])
