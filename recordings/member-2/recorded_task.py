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
    

    page.get_by_label("Mark all as complete").click()
    
  
    expect(task_items).to_have_class(["completed", "completed"])
    page.screenshot(
    path="docs/evidence/member-2/extra-test-1-active-filter.png",
    full_page=True,
)

def test_mark_all_active_again(page: Page):
    page.goto(URL)
    task_items = page.locator(".todo-list li")
    toggle_all = page.get_by_label("Mark all as complete")
    
    add_task(page, "Task One")
    add_task(page, "Task Two")
    toggle_all.click()
    expect(task_items).to_have_class(["completed", "completed"])
    
    toggle_all.click()
    
    
    expect(task_items).to_have_class(["", ""])
    page.screenshot(
    path="docs/evidence/member-2/extra-test-2-delete-task.png",
    full_page=True,
)
