from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch()
    page = browser.new_page()

    # Go to the app
    page.goto("http://localhost:3000")

    # Click the "Generate Model" button
    page.get_by_role("button", name="Generate Model").click()

    # Wait for the prediction to be displayed
    page.wait_for_selector("text=Prediction")

    # Take a screenshot
    page.screenshot(path="jules-scratch/verification/verification.png")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
