from playwright.sync_api import Page, expect


def test_recorded_task(page: Page):
    page.goto("https://demo.playwright.dev/todomvc/")

    task_input = page.get_by_placeholder(
        "What needs to be done?",
        exact=True,
    )
    task_input.fill("Try the recorder")
    task_input.press("Enter")

    task_labels = page.locator(".todo-list li label")
    expect(task_labels).to_have_text(["Try the recorder"])


#python -m pytest recordings/member-3/recorded_task.py --browser-channel %TEST_BROWSER% --headed --slowmo 300 --output test-results/member-3/recording-run --screenshot on --junitxml=reports/member-3/recording.xml --html=reports/member-3/recording.html --self-contained-html
#python -m pytest tests/test_member_3.py --browser-channel %TEST_BROWSER% --headed --output test-results/member-3/current-run --screenshot on --junitxml=reports/member-3/results.xml --html=reports/member-3/results.html --self-contained-html